from django.apps import AppConfig

class TmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TM'

    def ready(self):
        print("at ready")
        import TM.signals
        from TM.signals import scheduler
        scheduler()
