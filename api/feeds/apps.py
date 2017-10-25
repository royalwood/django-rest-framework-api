from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'feeds'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Post'))
        registry.register(self.get_model('Comment'))
