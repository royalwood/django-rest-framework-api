from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'groups'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Club'))
        registry.register(self.get_model('CustomGroup'))
        registry.register(self.get_model('StudentService'))
        registry.register(self.get_model('StudyGroup'))
        registry.register(self.get_model('MentorGroup'))
