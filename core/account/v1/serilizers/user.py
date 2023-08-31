from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from conf.model import MyModelSerializer

from account.models.user import CustomUser, PhoneCode
from conf.time import time_now
from rest_framework_simplejwt.tokens import RefreshToken


class TokenObtainCustomPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_date = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({'message': 'کاربر فعال نیست'})
        validate_date['user_id'], validate_date['username'] = (self.user.id, self.user.username)
        return validate_date


class GetCodeSerializer(MyModelSerializer):
    class Meta:
        model = PhoneCode
        fields = ['phone']

    def validate(self, attrs):
        if attrs.get('phone', None) is None:
            raise serializers.ValidationError({'message': 'وارد کردن شماره همراه الزامی است'})
        return super().validate(attrs)

    def create(self, validated_data):
        data = validated_data
        code = PhoneCode.objects.create_code(phone=validated_data.get('phone'))
        data['code'] = code.code
        return data

    def to_representation(self, instance):
        return instance


class CreateUserSerializer(MyModelSerializer):
    code = serializers.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'code']

    def validate(self, attrs):
        username = attrs.get('username', None)
        code = attrs.pop('code', None)
        if code is None or username is None:
            raise serializers.ValidationError({'message': 'شماره همراه یا کد وارد نشده است'})
        user_code = PhoneCode.objects.filter(phone=username, is_active=True).last()
        if not user_code:
            raise serializers.ValidationError('ابتدا کد دربافت کنید')
        if user_code.expire_date < time_now():
            user_code.is_active = False
            user_code.save()
            raise serializers.ValidationError({'message': 'اعتبار کد تمام شده است'})
        if code != user_code.code:
            raise serializers.ValidationError({'message': 'کد وارد شده صحیح نیست'})

        return super().validate(attrs)

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        validated_data['user_id'] = user.id
        refresh = RefreshToken.for_user(user)
        validated_data['access'] = str(refresh.access_token)
        validated_data['refresh'] = str(refresh)
        return validated_data

    def to_representation(self, instance):
        return instance
