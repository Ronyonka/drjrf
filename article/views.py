from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin

from .models import Article
from .serializers import ArticleSerializer

class ArticleView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        return serializer.save(author=author)

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, *kwargs)

    # def get(self, request, pk=None):
    #     if pk:
    #         article = get_object_or_404(Article.objects.all(), pk=pk)
    #         serializer = ArticleSerializer(article)
    #         return Response({"article": serializer.data})
    #     articles = Article.objects.all()
    #     serializer = ArticleSerializer(articles, many=True)
    #     return Response({"articles": serializer.data})

    def post(self, request):
        article = request.data.get('article')

        # Create an article from the above data
        serializer = ArticleSerializer(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(article_saved.title)})

    def put(self, request, pk):
        saved_article = get_object_or_404(Article.objects.all(), pk=pk)
        data = request.data.get('article')
        serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            article_saved =serializer.save()
        return Response({"success": "Article '{}' updated successfully".format(article_saved.title)})

    def delete(self, request, pk):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()
        return Response({"message": "Article with id `{}` has been deleted successfully.".format(pk)},status=204)

class SingleArticleView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
