"""Move all of this into the Model.save method. No need for signals"""
#pylint:disable=unused-argument
from django.template.loader import get_template
from django.core.mail import EmailMessage
from .models import StudentService

UCROO_WEBSITE_LINK = "https://www.ucroo.com.au"

def study_member_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        user = instance.user
        invited_by_user = instance.invited_by_user

        if user.email_notifications and invited_by_user is not None:
            group = instance.study_group
            invited_by_user_name = invited_by_user.first_name + " " + invited_by_user.last_name

            message = get_template('../templates/emails/add_study_group.html').render({'name': user.first_name, 'by': invited_by_user_name, 'group': group.name, 'link': UCROO_WEBSITE_LINK})
            msg = EmailMessage('You are added to a UCROO study group', message, 'no-reply@ucroo.com', ['%s' % user.email])
            msg.content_subtype = 'html'
            msg.send()

def student_service_member_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        user = instance.user
        invited_by_user = instance.student_email

        if user.email_notifications and invited_by_user is not None:
            invited_by_user_query = User.objects.all().filter(email=invited_by_user)

            if invited_by_user_query.exists():
                invited_by_user = invited_by_user_query[0]
                invited_by_user = invited_by_user.first_name + " " + invited_by_user.last_name

            group = instance.student_service

            message = get_template('../templates/emails/add_study_group.html').render({'name': user.first_name, 'by': invited_by_user, 'group': group.name, 'link': UCROO_WEBSITE_LINK})
            msg = EmailMessage('You are added to a UCROO student service group', message, 'no-reply@ucroo.com', ['%s' % user.email])
            msg.content_subtype = 'html'
            msg.send()

def follow_student_service_group(email, group_id):
    group = StudentService.objects.all().filter(id=group_id)

    if group.exists():
        group = group[0]
        message = get_template('../templates/emails/invite_follow_student_service_group.html').render({'group': group.name, 'link': UCROO_WEBSITE_LINK})
        msg = EmailMessage('You are added to a UCROO student service group', message, 'no-reply@ucroo.com', ['%s' % email])
        msg.content_subtype = 'html'
        msg.send()

        print message

def custom_member_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        user = instance.user
        invited_by_user = instance.member_email

        if user.email_notifications and invited_by_user is not None:
            invited_by_user_query = User.objects.all().filter(email=invited_by_user)

            if invited_by_user_query.exists():
                invited_by_user = invited_by_user_query[0]
                invited_by_user = invited_by_user.first_name + " " + invited_by_user.last_name

            group = instance.customgroups
            member_type = instance.member_type

            if member_type == 0: # is a member
                message = get_template('../templates/emails/add_study_group.html').render({'name': user.first_name, 'by': invited_by_user, 'group': group.name, 'link': UCROO_WEBSITE_LINK})
                msg = EmailMessage('You are added to a UCROO custom group', message, 'no-reply@ucroo.com', ['%s' % user.email])
                msg.content_subtype = 'html'
                msg.send()
            elif member_type == 1: # is an admin
                message = get_template('../templates/emails/add_customgroups_admin_user_email.html').render({'name': user.first_name, 'by': invited_by_user, 'group': group.name, 'link': UCROO_WEBSITE_LINK})
                msg = EmailMessage('You are added to a UCROO custom group', message, 'no-reply@ucroo.com', ['%s' % user.email])
                msg.content_subtype = 'html'
                msg.send()

def mentor_member_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        user = instance.user
        member_type = instance.types

        if user.email_notifications and member_type == 1: # 1 is for Mentor
            
            group = instance.mentor

            message = get_template('../templates/emails/add_study_group.html').render({'name': user.first_name, 'by': 'Someone', 'group': group.name, 'link': UCROO_WEBSITE_LINK})
            msg = EmailMessage('You are added to a UCROO mentor group', message, 'no-reply@ucroo.com', ['%s' % user.email])
            msg.content_subtype = 'html'
            msg.send()

def club_member_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        user = instance.user
        invited_by_user = instance.student_email

        if user.email_notifications and invited_by_user is not None:
            invited_by_user_query = User.objects.all().filter(email=invited_by_user)

            if invited_by_user_query.exists():
                invited_by_user = invited_by_user_query[0]
                invited_by_user = invited_by_user.first_name + " " + invited_by_user.last_name

            group = instance.club

            message = get_template('../templates/emails/add_study_group.html').render({'name': user.first_name, 'by': invited_by_user, 'group': group.name, 'link': UCROO_WEBSITE_LINK})
            msg = EmailMessage('You are added to a UCROO club', message, 'no-reply@ucroo.com', ['%s' % user.email])
            msg.content_subtype = 'html'
            msg.send()
