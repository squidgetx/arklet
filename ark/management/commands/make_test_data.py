"""Django Admin command to mint a test ARK 

"""

from django.core.management.base import BaseCommand
from django.db import transaction
from ark.models import Ark, Naan
from ark.utils import generate_noid
import os


class Command(BaseCommand):
    """Mint ark_count ARKs for the given naan and shoulder."""

    help = "Mint ARKs in bulk"

    def add_arguments(self, parser):
        parser.add_argument("naan", type=int)
        parser.add_argument("ark_count", type=int)

    def handle(self, *args, **options):
        naan_id = options["naan"]
        n_arks = options['ark_count']
        naan = Naan.objects.get(pk=options["naan"])
        if not naan:
            print('minting naan')
            naan = Naan(naan=options['naan'])
            naan.save()

        shoulder = "/b0"
        batch_size = 10000

        for i in range(0, n_arks, batch_size):
            objs = []
            for _ in range(batch_size):
                name = str(os.urandom(8).hex())
                arkstr = f"{naan_id}{shoulder}{name}"
                a = Ark(
                    ark=arkstr,
                    naan=naan,
                    shoulder=shoulder,
                    url=f"https://google.com?q={name}",
                    metadata=""
                )
                objs.append(a)

            with transaction.atomic():
                Ark.objects.bulk_create(objs)

            print(f"Created {i} arks")
