from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import PostSerializer
from .tasks import VKWorkOffersImporter
from .models import Post


class VKCommunityParseOnce(APIView):
    @swagger_auto_schema(
        operation_description="Parse VK community once",
        manual_parameters=[
            openapi.Parameter(
                'domain',
                openapi.IN_QUERY,
                description="VK community domain",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: "Successfully parsed"}
    )
    def get(self, request):
        community_domain = request.GET.get("domain", None)

        if not community_domain:
            return Response("You should specify community 'domain' to parse", status=status.HTTP_400_BAD_REQUEST)

        VKWorkOffersImporter().run(domain=community_domain)

        return Response("Successfully parsed", status=status.HTTP_200_OK)


class PostView(APIView):
    @swagger_auto_schema(
        operation_description="Get posts list",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request):
        data = PostSerializer(Post.objects.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)
