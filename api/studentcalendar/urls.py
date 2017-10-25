from config.routers import SharedRouter
from .views import CalendarViewSet


router = SharedRouter()
router.register(r'calendar', CalendarViewSet, base_name='calendar')
#router.register(r'calendar/university_calendar_ics/', CalendarViewSet, base_name='uni_cal') download ics file
