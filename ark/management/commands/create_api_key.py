import os
import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from ark.models import Key  # Assuming your app name is 'key' and the models.py contains the Key model


class Command(BaseCommand):
    help = 'Generate an API key and print it to the command line'

    def add_arguments(self, parser):
        # Add the 'naan' parameter to the command
        parser.add_argument('naan', type=int, help='Value for the "naan" parameter')

    def handle(self, *args, **kwargs):
        naan = kwargs['naan']
        # Generate an API key
        key_obj, api_key = Key.generate_api_key(naan)

        # Print the generated API key to the command line
        self.stdout.write(self.style.SUCCESS("Generated API Key: {}".format(api_key)))
