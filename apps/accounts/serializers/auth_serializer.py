from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.roles.models.role import Role

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Le champ username est requis par défaut

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password']
        )
        
        # Attribution du rôle par défaut
        try:
            default_role, _ = Role.objects.get_or_create(name="user")
            user.role = default_role
            user.save()
        except Role.DoesNotExist:
            pass
            
        return user