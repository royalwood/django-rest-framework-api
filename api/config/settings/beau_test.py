from .beau import * #pylint:disable=wildcard-import,unused-wildcard-import

INSTALLED_APPS += (
    # The django-test-without-migrations package lets me run tests faster with
    # `./manage.py test --nomigrations`
    'test_without_migrations',
)

# Use the MD5 password hasher, which speeds up testing by 10x. "This is the most
# effective setting you can use to improve the speed of tests, it may sounds
# ridicolous, but password hashing in Django is designed to be very strong and
# it makes use of several "hashers", but this also means that the hashing is
# very slow. The fastest hasher is the MD5PasswordHasher."
# http://www.daveoncode.com/2013/09/23/effective-tdd-tricks-to-speed-up-django-tests-up-to-10x-faster/
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
