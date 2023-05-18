from rest_framework import serializers
from .models import CustomUserModel, UserProfileModel, UserVideoModel


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUserModel
        fields = "__all__"

    def save(self):
        user = CustomUserModel(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileModel
        fields = "__all__"


class UserVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserVideoModel
        fields = "__all__"
