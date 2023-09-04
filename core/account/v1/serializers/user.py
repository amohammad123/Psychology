from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from conf.model import MyModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import password_validation
from django.core import exceptions

from account.models.user import CustomUser, PhoneCode
from conf.time import time_now


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
        phone = attrs.get('phone', None)
        if phone is None:
            raise serializers.ValidationError({'message': 'وارد کردن شماره همراه الزامی است'})
        # must be uncomment later
        # if len(phone) != 11:
        #     raise serializers.ValidationError({'message': 'شماره وارد شده صحیح نمی باشد'})
        return super().validate(attrs)

    def create(self, validated_data):
        code = PhoneCode.objects.create_code(phone=validated_data.get('phone'))
        validated_data['time_to_expire'] = code.expire_date - time_now()
        validated_data['code'] = code.code
        return validated_data

    def to_representation(self, instance):
        return instance


# class SignUpSerializer(MyModelSerializer):
#     code = serializers.CharField(max_length=15)
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'code']
#
#     def validate(self, attrs):
#         username = attrs.get('username', None)
#         code = attrs.pop('code', None)
#         if code is None or username is None:
#             raise serializers.ValidationError({'message': 'شماره همراه یا کد وارد نشده است'})
#         user_code = PhoneCode.objects.filter(phone=username, is_active=True).last()
#         if not user_code:
#             raise serializers.ValidationError({'message': 'ابتدا کد دربافت کنید'})
#         if user_code.expire_date < time_now():
#             user_code.is_active = False
#             user_code.save()
#             raise serializers.ValidationError({'message': 'اعتبار کد تمام شده است'})
#         if code != user_code.code:
#             raise serializers.ValidationError({'message': 'کد وارد شده صحیح نیست'})
#
#         return super().validate(attrs)
#
#     def create(self, validated_data):
#         user = CustomUser.objects.create(**validated_data)
#         validated_data['user_id'] = user.id
#         refresh = RefreshToken.for_user(user)
#         validated_data['access'] = str(refresh.access_token)
#         validated_data['refresh'] = str(refresh)
#         return validated_data
#
#     def to_representation(self, instance):
#         return instance


class CodeVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=14)
    code = serializers.CharField(max_length=15)

    def validate(self, attrs):
        username = attrs.get('username', None)
        code = attrs.pop('code', None)
        if code is None or username is None:
            raise serializers.ValidationError({'message': 'شماره همراه یا کد وارد نشده است'})
        user_code = PhoneCode.objects.filter(phone=username, is_active=True).last()
        if not user_code:
            raise serializers.ValidationError({'message': 'ابتدا کد دربافت کنید'})
        if user_code.expire_date < time_now():
            user_code.is_active = False
            user_code.save()
            raise serializers.ValidationError({'message': 'اعتبار کد تمام شده است'})
        if code != user_code.code:
            raise serializers.ValidationError({'message': 'کد وارد شده صحیح نمی باشد'})

        return super().validate(attrs)

    def to_representation(self, instance):
        get_user, user_created = CustomUser.objects.get_or_create(username=instance.get('username'))
        user = get_user if get_user is not None else user_created
        instance['user_id'] = user.id
        refresh = RefreshToken.for_user(user)
        instance['access'] = str(refresh.access_token)
        instance['refresh'] = str(refresh)
        return instance


class SetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=200)
    password1 = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'message': 'رمز عبور وارد شده مطابقت ندارد'})
        try:
            # password_validation.validate_password(attrs.get("password"))  # todo: uncomment
            CustomUser.objects.get(username=attrs.get('username'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'message': 'کاربر با این مشخصات یافت نشد'})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        username = validated_data.pop('username', None)
        return CustomUser.objects.get(username=username).update(is_verified=True, **validated_data)

    def to_representation(self, instance):
        user = instance.get('username')
        instance.pop('password')
        instance.pop('password1')
        instance['user_id'] = CustomUser.objects.get(username=user).id
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)
    new_password1 = serializers.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.user = self.context.get('request').user
            if not self.user.is_authenticated:
                raise serializers.ValidationError({'message': 'کاربر وارد نشده است'})
            self.get_user = CustomUser.objects.get(id=self.user.id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'message': 'کاربر با این مشخصات یافت نشد'})

    def validate(self, attrs):
        try:
            if attrs.get('new_password') != attrs.get('new_password1'):
                raise serializers.ValidationError({'message': 'رمز عبور وارد شده مطابقت ندارد'})
            if not self.get_user.check_password(attrs.get('old_password')):
                raise serializers.ValidationError({"message": "رمز عبور فعلی نادرست است"})
            # password_validation.validate_password(attrs.get("new_password"))  # todo: uncomment
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        self.get_user.set_password(validated_data.get('new_password'))
        self.get_user.save()
        validated_data['user_id'] = self.get_user.id
        return validated_data

    def to_representation(self, instance):
        instance.pop('old_password')
        instance.pop('new_password')
        instance.pop('new_password1')
        return instance
