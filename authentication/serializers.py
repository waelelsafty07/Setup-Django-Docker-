from rest_framework import serializers
from users.models import Users
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'passwordConfirm']

    username = serializers.CharField(required=True, validators=[
                                     UniqueValidator(queryset=Users.objects.all())])
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=Users.objects.all())])
    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])
    passwordConfirm = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])

    def validate(self, data):
        if data['password'] != data['passwordConfirm']:
            raise serializers.ValidationError("password not confirmed.")
        return data

    def create(self, validated_data):
        user = Users(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.set_password(validated_data['passwordConfirm'])

        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        message = ''
        if user and not user.is_active:
            user.is_active = True
            user.save()
            message = "Welcome Back to our app we so happy for you to comback again"
            return [user, message]
        if user and user.is_active:
            return user, message

        raise serializers.ValidationError('Incorrect Credentials Passed.')

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'bio', 'is_active', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'bio', 'is_active']
