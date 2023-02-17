from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from permissions import IsOwnerOrReadOnly
from .serializers import WishSerializer


class WishViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = WishSerializer

    def get_queryset(self):
        return self.request.user.wishes.all()

    def retrieve(self, request, *args, **kwargs):
        wish = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        ser_data = self.serializer_class(instance=wish)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        wish_list = get_list_or_404(self.get_queryset())
        ser_data = self.serializer_class(instance=wish_list, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        ser_data = self.serializer_class(data=request.data, context=request.user)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(f'Created... \n {ser_data.data}', status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        slug = request.get_full_path().split('/')
        wish = get_object_or_404(self.get_queryset(), slug=slug[-2])
        ser_data = self.serializer_class(instance=wish, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.update(wish, ser_data.validated_data)
            return Response(f'Updated... \n {ser_data.data}', status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        slug = request.get_full_path().split('/')
        wish = get_object_or_404(self.get_queryset(), user=request.user, slug=slug[-2])
        wish.delete()
        return Response('Deleted...', status=status.HTTP_200_OK)
