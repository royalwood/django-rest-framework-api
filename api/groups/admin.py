from django.contrib import admin

from .models import StudyGroup, StudyGroupMember, StudentService, StudentServiceAdmin, StudentServiceDropin, StudentServiceEvent, \
    StudentServiceEventMember, StudentServiceMember, Club, ClubAdminCommittee, ClubAdmin, ClubBank, ClubEvent, ClubEventTicket, \
    ClubField, ClubMember, ClubMembersField, ClubNonUcrooMember, MentorGroup, MentorGroupMember, CustomGroup, \
    CustomGroupMember, Event, EventMember, EventTicketSale


admin.site.register(StudyGroup)
admin.site.register(StudyGroupMember)
admin.site.register(StudentService)
admin.site.register(StudentServiceAdmin)
admin.site.register(StudentServiceDropin)
admin.site.register(StudentServiceEvent)
admin.site.register(StudentServiceEventMember)
admin.site.register(StudentServiceMember)
admin.site.register(Club)
admin.site.register(ClubAdminCommittee)
admin.site.register(ClubAdmin)
admin.site.register(ClubBank)
admin.site.register(ClubEvent)
admin.site.register(ClubEventTicket)
admin.site.register(ClubField)
admin.site.register(ClubMember)
admin.site.register(ClubMembersField)
admin.site.register(ClubNonUcrooMember)
admin.site.register(MentorGroup)
admin.site.register(MentorGroupMember)
admin.site.register(CustomGroup)
admin.site.register(CustomGroupMember)
admin.site.register(Event)
admin.site.register(EventMember)
admin.site.register(EventTicketSale)
