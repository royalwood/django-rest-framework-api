#pylint:disable=no-init
from tablib import Dataset
from import_export import resources

from .models import Campus, School, Course


class CampusResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row['uni'] = kwargs.get('uni').pk

    def import_csv(self, csv, uni):
        dataset = Dataset()
        dataset.csv = str(csv)
        return self.import_data(dataset, uni=uni)

    class Meta:
        model = Campus
        skip_unchanged = True
        fields = ('name', 'uni')
        import_id_fields = ('name', 'uni')


class SchoolResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row['uni'] = kwargs.get('uni').pk

    def import_csv(self, csv, uni):
        dataset = Dataset()
        dataset.csv = str(csv)
        return self.import_data(dataset, uni=uni)

    class Meta:
        model = School
        skip_unchanged = True
        fields = ('name', 'uni')
        import_id_fields = ('name', 'uni')


class CourseResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row['uni'] = kwargs.get('uni').pk

    def import_csv(self, csv, uni):
        dataset = Dataset()
        dataset.csv = str(csv)
        return self.import_data(dataset, uni=uni)

    class Meta:
        model = Course
        skip_unchanged = True
        fields = ('name', 'uni')
        import_id_fields = ('name', 'uni')
