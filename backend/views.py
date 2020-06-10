from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from .tasks import VKWorkOffersImporter
from .models import Post


class VKCommunityParseOnce(APIView):
    def get(self, request):
        community_domain = request.GET.get("domain", None)

        if not community_domain:
            return Response("You should specify community 'domain' to parse", status=status.HTTP_400_BAD_REQUEST)

        VKWorkOffersImporter().run(domain=community_domain)

        return Response("Successfully parsed", status=status.HTTP_200_OK, )


class PostView(APIView):
    def get(self, request):
        data = PostSerializer(Post.objects.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)
