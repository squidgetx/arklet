import json
import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Length
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
    HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

from ark.forms import MintArkForm, UpdateArkForm
from ark.models import Ark, Naan, Key, Shoulder
from ark.utils import generate_noid, noid_check_digit, parse_ark, gen_prefixes

logger = logging.getLogger(__name__)

def authorize(request, naan):
    bearer_token = request.headers.get("Authorization")
    if not bearer_token:
        return None

    key = bearer_token.split()[-1]

    try:
        keys = Key.objects.filter(naan=naan,active=True)
        for k in keys:
            if k.check_password(key):
                return k.naan
        return None
    except ValidationError as e:  # probably an invalid key
        return None
    

@csrf_exempt
def mint_ark(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    try:
        unsafe_mint_request = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, TypeError) as e:
        return HttpResponseBadRequest(e)

    mint_request = MintArkForm(unsafe_mint_request)

    if not mint_request.is_valid():
        return JsonResponse(mint_request.errors, status=400)

    # Pop these keys so that we can pass the cleaned data
    # dict directly to the create method later
    naan = mint_request.cleaned_data.pop("naan")
    authorized_naan = authorize(request, naan)
    if authorized_naan is None:
        return HttpResponseForbidden()

    shoulder = mint_request.cleaned_data.pop("shoulder")
    shoulder_obj = Shoulder.objects.filter(shoulder=shoulder).first()
    if shoulder_obj is None:
        return HttpResponseBadRequest(f"Shoulder {shoulder} does not exist")

    ark, collisions = None, 0
    for _ in range(10):
        # TODO this code should be moved to the ARK model 
        noid = generate_noid(8)
        base_ark_string = f"{naan}{shoulder}{noid}"
        check_digit = noid_check_digit(base_ark_string)
        ark_string = f"{base_ark_string}{check_digit}"
        try:
            ark = Ark.objects.create(
                ark=ark_string,
                naan=authorized_naan,
                shoulder=shoulder_obj,
                assigned_name=f"{noid}{check_digit}",
                **mint_request.cleaned_data
            )
            break
        except IntegrityError:
            collisions += 1
            continue

    if not ark:
        msg = f"Gave up creating ark after {collisions} collision(s)"
        logger.error(msg)
        return HttpResponseServerError(msg)
    if ark and collisions > 0:
        logger.warning("Ark created after %d collision(s)", collisions)

    return JsonResponse({"ark": str(ark)})


@csrf_exempt
def update_ark(request):
    if request.method != "PUT":
        return HttpResponseNotAllowed(permitted_methods=["PUT"])

    try:
        unsafe_update_request = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, TypeError) as e:
        return HttpResponseBadRequest(e)

    # TODO: test input data with wrong structure
    update_request = UpdateArkForm(unsafe_update_request)

    if not update_request.is_valid():
        return JsonResponse(update_request.errors, status=400)

    # The ark field is immutable, pop it out of the cleaned
    # data dictionary here so we don't try to update it later
    ark = update_request.cleaned_data.pop("ark")

    _, naan, assigned_name = parse_ark(ark)

    authorized_naan = authorize(request, naan)
    if authorized_naan is None:
        return HttpResponseForbidden()

    try:
        ark_obj = Ark.objects.get(ark=f"{naan}/{assigned_name}")
    except Ark.DoesNotExist:
        raise Http404
    
    for key in update_request.cleaned_data:
        setattr(ark_obj, key, update_request.cleaned_data[key])
    ark_obj.save()

    return HttpResponse()


def resolve_ark(request, ark: str):
    info_inflection = 'info' in request.GET
    json_inflection = 'json' in request.GET

    try:
        _, naan, identifier = parse_ark(ark)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    ark_str = f"{naan}/{identifier}"
    ark_obj = Ark.objects.filter(ark=ark_str).first()
    if ark_obj:
        if info_inflection:
            return view_ark(request, ark_obj)
        if json_inflection:
            return json_ark(request, ark_obj)
        if not ark_obj.url:
            return view_ark(request, ark_obj)
        return HttpResponseRedirect(ark_obj.url + '?' + request.META['QUERY_STRING'])
    else:
        # Ark not found. Try to find an ark that is a prefix.
        prefixes = [f"{naan}/{a}" for a in gen_prefixes(identifier)]
        # Get the one with the longest prefix
        ark_prefix = Ark.objects.filter(ark__in=prefixes).order_by(Length('ark')).first()
        if ark_prefix:
            suffix = ark_str.removeprefix(ark_prefix.ark)
            return HttpResponseRedirect(ark_prefix.url + suffix)
        else:
            if info_inflection or json_inflection:
                raise Http404
            try:
                naan_obj = Naan.objects.get(naan=naan)
                return HttpResponseRedirect(
                    f"{naan_obj.url}/ark:/{ark_str}"
                )
            except Naan.DoesNotExist:
                resolver = "https://n2t.net"
                # TODO: more robust resolver URL creation
                return HttpResponseRedirect(f"{resolver}/ark:/{ark_str}")


"""
Return HTML human readable webpage information about the Ark object
"""
def view_ark(request: HttpRequest, ark: Ark):

    context = {
        'ark': ark.ark,
        'url': ark.url,
        'label': ark.title,
        'type': ark.type,
        'commitment': ark.commitment,
        'identifier': ark.identifier,
        'format': ark.format,
        'relation': ark.relation,
        'source': ark.source,
        'metadata': ark.metadata
    }

    return render(request, 'info.html', context)

"""
Return the Ark object as JSON
"""
def json_ark(request: HttpRequest, ark: Ark):
    data = {
        'ark': ark.ark,
        'url': ark.url,
        'title': ark.title,
        'type': ark.type,
        'commitment': ark.commitment,
        'identifier': ark.identifier,
        'format': ark.format,
        'relation': ark.relation,
        'source': ark.source,
        'metadata': ark.metadata
    }
    obj = {}
    for key in data:
        obj[key] = Ark.COLUMN_METADATA.get(key, {})
        obj[key]['value'] = data[key]


    # Return the JSON response
    return JsonResponse(obj)