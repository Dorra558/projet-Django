from rest_framework import fields, serializers
from .models import User
from .models import Utilisateur


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email' , 'password']

# hide the password and don't return it 
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Utilisateur
        fields = ['id', 'firstname', 'secondname', 'description', 'published']

