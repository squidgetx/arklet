"""Django Admin command to count ARKs under 
the given naan 
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from ark.models import Ark, Naan, Shoulder
from ark.utils import generate_noid
from django.db.models import Count
import json
import random


class Command(BaseCommand):

    help = "Count ARKs for the given naan by shoulder"

    def add_arguments(self, parser):
        parser.add_argument("naan", type=int)

    def handle(self, *args, **options):
        naan = Naan.objects.get(pk=options["naan"])
        arks = Ark.objects.filter(naan=naan).values('shoulder__shoulder').annotate(total=Count('ark')).order_by('shoulder__shoulder')
        print(json.dumps(list(arks), indent=4))

