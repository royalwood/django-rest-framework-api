"""Custom token response, includes the User in the token response. This means
the client app doesn't have to send another request to get the user after
authenticating.
"""
import json

from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import MethodNotAllowed
from oauth2_provider.views import TokenView

from users.serializers import FullUserSerializer


class CustomTokenView(TokenView):
    def create_token_response(self, request):
        """Calls the base class first, then adds the User object into the
        body of the response.
        """
        if request.method != 'POST':
            raise MethodNotAllowed(request.method, 'Use POST for token')
        url, headers, body, status = super().create_token_response(request)
        if status == 200:
            # Get the user
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            # Load the body from JSON string
            body = json.loads(body)
            # This is the only way I know to get Serializer.data in a form that
            # can be serialized to JSON. Removes the nested OrderedDicts
            body['user'] = json.loads(JSONRenderer().render(
                FullUserSerializer(user).data))
            # Serialize back into a string
            body = json.dumps(body)
        return url, headers, body, status
