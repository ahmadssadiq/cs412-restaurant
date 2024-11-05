from django.apps import AppConfig

class MiniFbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_fb'

    def ready(self):
        import mini_fb.signals  # Ensure this matches your app structure