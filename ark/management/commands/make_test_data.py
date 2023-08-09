"""Django Admin command to mint a test ARK 
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from ark.models import Ark, Naan, Shoulder
from ark.utils import generate_noid
import os


class Command(BaseCommand):
    """Mint ark_count ARKs for the given naan and shoulder."""

    help = "Mint ARKs in bulk"

    def add_arguments(self, parser):
        parser.add_argument("ark_count", type=int)
        parser.add_argument("naan", type=int)
        parser.add_argument("shoulder", type=str)

    def handle(self, *args, **options):
        n_arks = options['ark_count']
        naan = Naan.objects.get(pk=options["naan"])
        if not naan:
            print('minting naan')
            naan = Naan(naan=options['naan'])
            naan.save()

        shoulder = Shoulder.objects.get(shoulder=options['shoulder'])
        if not shoulder:
            print('minting shoulder')
            shoulder = Shoulder(shoulder=options['shoulder'], naan=Naan)
            shoulder.save
        batch_size = 10000

        for i in range(0, n_arks, batch_size):
            objs = []
            for _ in range(batch_size):
                a = Ark.create(naan, shoulder)
                a.url = f"https://google.com?q={a.ark}",
                objs.append(a)

            with transaction.atomic():
                Ark.objects.bulk_create(objs)

            print(f"Created {i} arks")
