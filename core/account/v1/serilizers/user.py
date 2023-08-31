from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from account.models.user import CustomUser, PhoneCode
from conf.time import time_now


class TokenObtainCustomPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_date = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({'message': 'کاربر فعال نیست'})
        validate_date['user_id'], validate_date['username'] = (self.user.id, self.user.username)
        return validate_date


class GetCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneCode
        fields = ['phone']

    def validate(self, attrs):
        phone_code = PhoneCode.objects.filter(phone=attrs.get('phone')).order_by('-create_date')
        if phone_code.count() > 0:
            if phone_code.last().expire_date < time_now():
                raise serializers.ValidationError({'message': 'کد قبلا برای شما ارسال شده'})
            for code in phone_code:
                if code.expire_date > time_now():
                    code.is_active = False
                    code.save()
        return super().validate(attrs)

    def create(self, validated_data):
        return PhoneCode.objects.create(phone=validated_data.get('phone'))
    # def validate(self, attrs):
    #     validate_data = super().validate(attrs)
    #     # print(validate_data)
    #     return validate_data
