from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Movie,Ratings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {'password':{'write_only':True,'required':True}}
    
    # For registration of a new user
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user) # For generating a new Token for the new user
        return user
 
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id','title','description','no_of_ratings')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ('id','stars','user','movie')