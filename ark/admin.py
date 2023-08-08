"""Django Admin models for Arklet."""

from django.contrib import admin, messages
from ark.models import Ark, Key, Naan, Shoulder, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Django Admin model for ARK admin users."""


@admin.register(Naan)
class NaanAdmin(admin.ModelAdmin):
    """Django Admin model for Name Assignment Authority Number bearing organizations."""

    list_display = ["name", "naan"]

@admin.register(Shoulder)
class ShoulderAdmin(admin.ModelAdmin):
    """Django Admin model for shoulders"""

    # don't allow editing shoulders after creation
    # because it will break existing ARK identifiers
    def get_readonly_fields(self, request, obj=None):
        defaults = super().get_readonly_fields(request, obj=obj)
        if obj:  
            defaults = tuple(defaults) + ('shoulder', )  
        return defaults

    list_display = ["shoulder", "name", "naan"]

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    """Django Admin model for managing Arklet access keys.

    These access keys are used to mint and bind ARKs via the Arklet API.
    """

    list_display = ["key", "naan", "active"]
    exclude=['key']

    def save_model(self, request, obj, form, change):
        obj, api_key = obj.generate_api_key()
        super().save_model(request, obj, form, change)
        
        # Add a custom message after saving the model
        messages.success(request, f"Your new API key is {api_key}. Write this down in a secure location!")
