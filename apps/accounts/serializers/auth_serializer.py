from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.roles.models.role import Role
from apps.common.utils.validators import validate_email, validate_password

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
        email = validate_email(validated_data.get('email'))
        password = validate_password(validated_data.get('password'))
        username = validated_data.get('username')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Attribution du rôle par défaut
        try:
            default_role = Role.objects.get(name="user")
            user.role = default_role
            user.save()
        except Role.DoesNotExist:
            pass

        return user