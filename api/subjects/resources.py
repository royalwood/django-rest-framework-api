from tablib import Dataset
from import_export import resources

from .models import Subject


class SubjectResource(resources.ModelResource): #pylint:disable=no-init
    def before_import_row(self, row, **kwargs):
        row['uni'] = kwargs.get('uni').pk
        row['user'] = kwargs.get('user').pk

    def import_csv(self, csv, uni, user):
        dataset = Dataset()
        dataset.csv = str(csv)
        return self.import_data(dataset, uni=uni, user=user)

    class Meta: #pylint:disable=no-init
        model = Subject
        skip_unchanged = True
        fields = ('code', 'name', 'uni', 'user')
        import_id_fields = ('code',)
