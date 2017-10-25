from config.routers import SharedRouter
from .views import (
    UniversityViewSet, SchoolViewSet, CampusViewSet, CourseViewSet)


router = SharedRouter()
router.register(r'universities', UniversityViewSet, base_name='universities')
router.register(r'campuses', CampusViewSet, base_name='campuses')
router.register(r'schools', SchoolViewSet, base_name='schools')
router.register(r'courses', CourseViewSet, base_name='courses')
