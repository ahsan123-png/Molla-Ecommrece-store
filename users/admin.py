from django.contrib import admin
from django.apps import apps

# Get all models in the current app
app = apps.get_app_config('users')  # ← Replace 'myapp' with your actual app name

for model in app.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass 