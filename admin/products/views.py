import random

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
from .serializers import ProductSerializer
from .producer import publish

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        GET request for retrieving all of the products.

        PATH: /api/products
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """
        POST request for creating a new product.

        PATH: /api/products
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """
        GET request for getting the details of a specific product.

        PATH: /api/products/<str:id>
        """
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """
        PUT request for updating a specific product.

        PATH: /api/products/<str:id>
        """
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        """
        DELETE request for deleting a specific product.

        PATH: /api/products/<str:id>
        """
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
    
    def post(self, _):
        User.objects.create()
        return Response(status=status.HTTP_201_CREATED)