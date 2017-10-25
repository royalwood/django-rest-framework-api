import os
from binascii import hexlify

from django.conf import settings

from django.contrib.auth import get_user_model
from rest_framework import views, status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FileUpload
from .serializers import FileUploadSerializer


class FileUploadView(views.APIView):
    permission_classes = (IsAuthenticated,)
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = JSONParser, MultiPartParser
    UPLOAD_FILE_SIZE_LIMIT_MB = 3

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, format=None): #pylint:disable=redefined-builtin
        queryset = FileUpload.objects.all()
        object_id = self.request.query_params.get('object_id')
        user_id = self.request.query_params.get('user_id')

        if object_id:
            serializer = FileUploadSerializer(queryset.filter(object_id=object_id), many=True)
        elif user_id:
            serializer = FileUploadSerializer(queryset.filter(user=user_id), many=True)
        else:
            serializer = FileUploadSerializer(queryset.none(), many=True)

        res_dictionary = []

        for obj in serializer.data:
            obj["url"] = settings.URL_UPLOAD + obj["filename"]
            res_dictionary.append(obj)

        return Response(res_dictionary)

    def post(self, request, format=None): #pylint:disable=redefined-builtin
        up_file = request.data.get('file')

        if up_file is not None:

            if up_file.size > (FileUploadView.UPLOAD_FILE_SIZE_LIMIT_MB * 1000000):
                return Response("File size exceeds the limit of "+str(FileUploadView.UPLOAD_FILE_SIZE_LIMIT_MB)+"MB",
                                status=status.HTTP_202_ACCEPTED,
                                headers={'Location': settings.URL_UPLOAD + up_file.name})

            filename = up_file.name.replace(" ", "_")
            filename = str(hexlify(os.urandom(6)))+"-" + filename

            object_id = request.data.get('object_id')
            email = request.data.get('email')

            ext = os.path.splitext(filename)[1]
            valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.xls', '.docx', '.xlsx']

            if not ext.lower() in valid_extensions:
                return Response("File format is not supported", status=status.HTTP_202_ACCEPTED,
                                headers={'Location': settings.URL_UPLOAD + filename})

            if os.path.exists(settings.MEDIA_ROOT + filename):
                return Response("Duplicate data", status=status.HTTP_202_ACCEPTED,
                                headers={'Location': settings.URL_UPLOAD + filename})
            else:
                queryset = get_user_model().objects.all().filter(email=email)[:1]

                if queryset.exists():
                    user = queryset[0].id
                    file_name = filename

                    destination = open(settings.MEDIA_ROOT + filename, 'wb+')

                    for chunk in up_file.chunks():
                        destination.write(chunk)
                        destination.close()

                    r_obj = {}
                    r_obj['user'] = user
                    r_obj['object_id'] = object_id
                    r_obj['filename'] = filename
                    r_obj['file_size'] = up_file.size / 1000

                    serializer = FileUploadSerializer(data=r_obj)
                    serializer.is_valid()
                    serializer.save()

                    return Response({'message': 'Uploaded ' + file_name,
                                     'location': settings.URL_UPLOAD + file_name},
                                    status=status.HTTP_202_ACCEPTED,
                                    headers={'Location': settings.URL_UPLOAD + file_name})
        else:
            return Response('Upload error', status=status.HTTP_409_CONFLICT)
