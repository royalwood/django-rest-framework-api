from django.conf.urls import url

from config.routers import SharedRouter
from .views import EventViewSet, EventMemberViewSet
from .views import (
    ClubViewSet, ClubMemberViewSet, CustomGroupViewSet,
    CustomGroupMemberViewSet, StudentServiceViewSet, StudentServiceAdminViewSet,
    StudentServiceDropinViewSet, StudentServiceEventViewSet,
    StudentServiceEventMemberViewSet, StudentServiceMemberViewSet,
    StudyGroupViewSet, StudyGroupMemberViewSet, MentorGroupViewSet,
    MentorGroupMemberViewSet, JoinedGroupsView)


router = SharedRouter()

# Clubs
router.register(r'clubs/members', ClubMemberViewSet, base_name='clubmembers')
#router.register(r'clubs/events', ClubEventViewSet, base_name='clubevents')
#router.register(r'clubs/tickets', ClubEventTicketViewSet, base_name='clubtickets')
router.register(r'clubs', ClubViewSet, base_name='clubs')

# Custom Groups
router.register(r'customgroups/members', CustomGroupMemberViewSet, base_name='customgroupmembers')
router.register(r'customgroups', CustomGroupViewSet, base_name='customgroups')

# Student Services
router.register(r'studentservices/admins', StudentServiceAdminViewSet, base_name='studentserviceadmins')
router.register(r'studentservices/members', StudentServiceMemberViewSet, base_name='studentservicemembers')
router.register(r'studentservices/dropins', StudentServiceDropinViewSet, base_name='studentservicedropins')
router.register(r'studentservices/events', StudentServiceEventViewSet, base_name='studentserviceevents')
router.register(r'studentservices/events/attendees', StudentServiceEventMemberViewSet, base_name='studentserviceeventattendees')
router.register(r'studentservices', StudentServiceViewSet, base_name='studentservices')

# Study Groups
router.register(r'studygroups/members', StudyGroupMemberViewSet, base_name='studygroupmembers')
router.register(r'studygroups', StudyGroupViewSet, base_name='studygroups')

# Mentor Groups
router.register(r'mentorgroups/members', MentorGroupMemberViewSet, base_name='mentorgroupmembers')
router.register(r'mentorgroups', MentorGroupViewSet, base_name='mentorgroups')

# Events
router.register(r'events/members', EventMemberViewSet, base_name='eventmembers')
router.register(r'events', EventViewSet, base_name='event')


urlpatterns = [
    url(r'joined', JoinedGroupsView.as_view(), name='joinedgroups'),
]
