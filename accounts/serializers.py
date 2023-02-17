from rest_framework import serializers
from .models import User


def clean_email(value):
    if 'admin' in value:
        raise serializers.ValidationError("email can't be admin")


def clean_username(value):
    if value == 'admin':
        raise serializers.ValidationError("username can't be admin")
    return value


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email,)},
            'username': {'validators': (clean_username,)}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords must to match")
        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)


class UserResetPasswordSerializer(serializers.ModelSerializer):
    token_received = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('token_received', 'new_password', 'confirm_password',)

    def validate_token_received(self, value):
        if value != str(self.context.get('token')):
            raise serializers.ValidationError('Invalid Token')
        return value

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError('Passwords should match')
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ChangeUsernameSerializer(serializers.ModelSerializer):
    new_username = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'new_username',)
        extra_kwargs = {
            'username': {'validators': (clean_username,)},
            'new_username': {'validators': (clean_username,)},
        }

    def validate_username(self, value):
        if value != self.instance.username:
            raise serializers.ValidationError("old username is not correct")
        return value

    def validate(self, data):
        print(data.get('username'))
        print(data.get('new_username'))
        if data.get('username') == data.get('new_username'):
            raise serializers.ValidationError("new username must not match old username")
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('new_username')
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('new_password', 'confirm_password', 'old_password',)

    def validate_old_password(self, value):
        user = self.context
        if not user.check_password(value):
            raise serializers.ValidationError("old password is not correct")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords must to match")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
