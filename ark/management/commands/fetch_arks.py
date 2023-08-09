"""Django Admin command to fetch random ARKs under 
the given naan and shoulder
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from ark.models import Ark, Naan, Shoulder
from ark.utils import generate_noid
import os
import random


class Command(BaseCommand):

    help = "Fetch 50 random ARKs for the given naan and shoulder"

    def add_arguments(self, parser):
        parser.add_argument("naan", type=int)
        parser.add_argument("shoulder", type=str)

    def handle(self, *args, **options):
        shoulder_str = options['shoulder']
        naan = Naan.objects.get(pk=options["naan"])
        shoulder = Shoulder.objects.get(shoulder=shoulder_str)
        arks = Ark.objects.filter(shoulder=shoulder, naan=naan)
        possible_ids = list(arks.values_list('ark', flat=True))
        random_ids = random.choices(possible_ids, k=50)
        for id in random_ids:
            print(id)

