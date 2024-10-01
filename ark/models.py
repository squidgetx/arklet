import uuid
import os
import hashlib

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import models


from ark.forms import UpdateArkForm, validate_shoulder
from ark.utils import generate_noid, noid_check_digit

class Naan(models.Model):
    naan = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.naan}"


class User(AbstractUser):
    naan = models.ForeignKey(Naan, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.username


class Key(models.Model):
    key = models.CharField(max_length=4096, primary_key=True)

    def generate_api_key(self):
        api_key = uuid.uuid4()
        self.set_password(str(api_key))
        return self, api_key

    @classmethod
    def create_for_naan(cls, naan_id):
        try:
            naan_instance = Naan.objects.get(naan=naan_id)
        except Naan.DoesNotExist:
            raise ValueError("Naan instance with the provided ID does not exist.")

        key_inst = Key(active=True, naan=naan_instance)
        key_inst, api_key = key_inst.generate_api_key()
        key_inst.save()
        return key_inst, api_key

    def set_password(self, raw_password):
        # Hash the raw password before storing it in the database
        self.key = make_password(raw_password)

    def check_password(self, raw_password):
        # Check if the provided raw password matches the hashed password in the database
        return check_password(raw_password, self.key)

    naan = models.ForeignKey(Naan, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Key-{self.naan.naan}-{self.key[:8]}..."


class Shoulder(models.Model):
    shoulder = models.CharField(max_length=50, validators=[validate_shoulder])
    naan = models.ForeignKey(Naan, on_delete=models.DO_NOTHING)

    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        unique_together = ('shoulder', 'naan')

    def __str__(self):
        return f"{self.naan.naan}{self.shoulder}"


class Ark(models.Model):
    ark = models.CharField(primary_key=True, max_length=200, editable=False)
    naan = models.ForeignKey(Naan, on_delete=models.DO_NOTHING, editable=False)
    shoulder = models.ForeignKey(Shoulder, on_delete=models.DO_NOTHING, editable=False)
    assigned_name = models.CharField(max_length=100, editable=False)
    url = models.URLField(default="", blank=True)
    metadata = models.TextField(default="", blank=True)
    commitment = models.TextField(default="", blank=True)

    # Frick specific fields here:
    title = models.TextField(default="", blank=True)
    type = models.TextField(default="", blank=True)
    identifier = models.TextField(default="", blank=True)
    format = models.TextField(default="", blank=True)
    relation = models.TextField(default="", blank=True)
    source = models.TextField(default="", blank=True)

    COLUMN_METADATA = {
        'title': {
            'property': "http://purl.org/dc/elements/1.1/title",
            'type': "xsd:string",
        },
        'type': {
            'property': 'http://purl.org/dc/elements/1.1/type',
            'type': "xsd:string",
        },
        'commitment': {
            'type': "xsd:string",
        },
        'identifier': {
            'property': 'http://purl.org/dc/elements/1.1/identifier',
            'type': "xsd:string",
        },
        'format': {
            'property': 'http://purl.org/dc/elements/1.1/format',
            'type': "xsd:string",
        },
        'relation': {
            'property': 'http://purl.org/dc/elements/1.1/relation',
            'type': 'xsd:anyURI'
        },
        'source': {
            'property': 'http://purl.org/dc/elements/1.1/source',
            'type': 'xsd:anyURI'
        },
        'url': {
            'property': 'https://schema.org/url',
            'type': 'xsd:anyURI'
        }
    }

    def clean(self):
        expected_ark = f"{self.naan.naan}{self.shoulder}{self.assigned_name}"
        if self.ark != expected_ark:
            raise ValidationError(f"expected {expected_ark} got {self.ark}")
    
    @classmethod
    def create(cls, naan: Naan, shoulder: Shoulder):
        noid = generate_noid(int(os.environ.get("ARKLET_NOID_LENGTH", 8)))
        ark_prefix = f"{naan.naan}{shoulder.shoulder}"
        base_ark_string = f"{ark_prefix}{noid}"
        check_digit = noid_check_digit(base_ark_string)
        assigned_name = f"{noid}{check_digit}"
        ark_string = f"{ark_prefix}{assigned_name}"

        return Ark(
            ark=ark_string,
            naan=naan,
            shoulder=shoulder,
            assigned_name=assigned_name
        )
    
    def set_fields(self, data: dict):
        permitted_fields = set(UpdateArkForm.base_fields)
        permitted_fields.remove('ark')
        for key, val in data.items():
            if key in permitted_fields:
                setattr(self, key, val)

    def __str__(self):
        return f"ark:/{self.ark}"
