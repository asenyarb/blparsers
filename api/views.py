from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import PublicationSerializer
from parsers.vkparser.models import Publication


class VKPostsView(APIView):
    @swagger_auto_schema(
        operation_description="Get posts list",
        responses={200: PublicationSerializer(many=True)}
    )
    def get(self, request):
        data = PublicationSerializer(Publication.objects.all().order_by('-created_date'), many=True).data
        return Response(data, status=status.HTTP_200_OK)
