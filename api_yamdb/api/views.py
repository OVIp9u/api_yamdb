from http.client import HTTPException

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from titles.models import Title, Genre, Category
from rest_framework import viewsets, status

from .serializers import TitleSerializer, CategorySerializer, GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer(many=True)
    lookup_field = 'slug'

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save()

    # def list(self, request):
    #     queryset = Genre.objects.all()
    #     serializer = GenreSerializer(self.get_queryset(), many=True)
    #     return Response(serializer.data)