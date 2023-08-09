"""Django Admin command to delete all ARKs under 
the given naan and shoulder
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from ark.models import Ark, Naan, Shoulder
from ark.utils import generate_noid
import os


class Command(BaseCommand):

    help = "Delete all ARKs for the given naan and shoulder"

    def add_arguments(self, parser):
        parser.add_argument("naan", type=int)
        parser.add_argument("shoulder", type=str)

    def handle(self, *args, **options):
        naan_id = options["naan"]
        shoulder_str = options['shoulder']
        naan = Naan.objects.get(pk=options["naan"])
        if not naan:
            print('minting naan')
            naan = Naan(naan=options['naan'])
            naan.save()

        shoulder = Shoulder.objects.get(shoulder=shoulder_str)
        arks = Ark.objects.filter(shoulder=shoulder, naan=naan)
        info = arks.delete()
        print(f"Deleted {info[0]} objects")

