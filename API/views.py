from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Movie, Ratings
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Our custom method to rate a movie with our logic. Instead of using pre-defined POST,PUT methods it will use our custom method
    @action(detail=True,methods = ['POST']) # This decorates with the condition that only POST method is allowed.
    def rate_movie(self, request, pk = None): 

        if 'stars' in request.data: # Validation of Request Data
            movie = Movie.objects.get(id=pk)  #Selecting the Movie requested, from the database.
            stars = request.data['stars']
            user = request.user
            # user = User.objects.get(id=1) # Static 
            response = {'message': 'Its working'}

            # If the movie and user are present in the database then update the ratings else Create a new movie
            try:
                rating = Ratings.objects.get(user=user.id, movie = movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many = False)
                response = {'message':'Rating updated','result': serializer.data}
                return Response(response, status = status.HTTP_200_OK)
            except:
                rating = Ratings.objects.get(user=user, movie = movie, stars = stars)
                serializer = RatingSerializer(rating, many = False)
                response = {'message':'Rating created','result': serializer.data}
                return Response(response,status = status.HTTP_400_BAD_REQUEST)

        else:
            response = {'message':'You need to provide stars'}
            return Response(response,status = status.HTTP_400_BAD_REQUEST)



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    perimission_classes = (IsAuthenticated,)

    # Over writing these methods to restrict the usage of all 5 CRUD methods provided by ModelViewSet
    # Self-define update method overriding pre-defined method:
    def update(self,request,*args,**kwargs):
        response = {'message':'You cant update permissions like that'}
        return Response(response,status = status.HTTP_400_BAD_REQUEST)

    # Self-define create method overriding pre-defined method:
    def create(self,request,*args,**kwargs):
        response = {'message':'You cant create permissions like that'}
        return Response(response,status = status.HTTP_400_BAD_REQUEST)
