from config.routers import SharedRouter
from .views import SubjectViewSet, EnrolledSubjectsViewSet


router = SharedRouter()
router.register(r'subjects/enrolled', EnrolledSubjectsViewSet, base_name='subjectsenrolled')
router.register(r'subjects', SubjectViewSet, base_name='subjects')
