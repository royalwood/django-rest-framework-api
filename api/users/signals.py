#pylint:disable=unused-argument
from django.template.loader import get_template
from django.core.mail import EmailMessage


# Signals here are for sending emails; might move to model save - TBA.
# Templates are in the core '/template/emails' folder.


# activate email
def activate_email(sender, instance, **kwargs):
#    print 'activate email'
    if kwargs['created']:
        # display vars
        email_to = 'nick@ucroo.com'
        name = 'test name'
        link_id = 2

        message = get_template('../templates/emails/activate.html').render({'name': name, 'link_id': link_id})
        msg = EmailMessage('Activate your account', message, 'no-reply@ucroo.com', ['%s' % email_to])
        msg.content_subtype = 'html'
        msg.send()


# welcome email
def welcome_email(sender, instance, **kwargs):
    if kwargs['created']:
        # display vars
        email_to = 'nick@ucroo.com'
        first_name = 'first name'
        university_name = 'Stanford Uni'
        user_email = 'nick@test.com'
        web_app_url = 'https://sucroo.com'
        # determine template for user type
        # user_type = instance

        # print 'instance = ' + instance

        message = get_template('../templates/emails/welcome_student.html').render(
            {'first_name': first_name, 'university_name': university_name, "user_email": user_email,
             "web_app_url": web_app_url})
        msg = EmailMessage('Activate your account', message, 'no-reply@ucroo.com', ['%s' % email_to])
        msg.content_subtype = 'html'
        msg.send()


def user_post_save(sender, instance, **kwargs):
    if kwargs['created'] and instance.email_notifications:
        print("Singal created User")


def request_demo(name, institute, role, email, phone):
    message = get_template('../templates/emails/request_demo_email.html').render({'name': name, 'institute': institute, 'role': role, 'email': email, 'phone': phone})
    msg = EmailMessage('Someone requests a Ucroo demo', message, 'no-reply@ucroo.com', ['admin@ucroo.com'])
    msg.content_subtype = 'html'
    msg.send()
