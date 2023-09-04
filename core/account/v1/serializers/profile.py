from rest_framework import serializers
from conf.model import MyModelSerializer
from django.core import exceptions

from account.models.profile import Profile
from account.models.user import CustomUser


class SetProfileSerializer(MyModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'nationality_code', 'date_of_birth']

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
        if Profile.objects.filter(user=self.get_user).exists():
            raise serializers.ValidationError('کاربر با این مشخصات قبلا ثبت شده است')
        return attrs

    def create(self, validated_data):
        if self.get_user.profile is not None:
            raise serializers.ValidationError({'message': 'کاربر قبلا ساخته شده است'})
        self.profile = Profile.objects.create(user=self.get_user, **validated_data)
        return validated_data

    def to_representation(self, instance):
        instance['username'] = self.get_user.username
        instance['user_id'] = self.profile.id
        return instance


class TrappistSetProfileSerializer(MyModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'nationality_code', 'date_of_birth', 'specialized_field', 'level',
                  'member_number', 'license_number', 'city']

    def __init__(self, *args, **kwargs):
        super(TrappistSetProfileSerializer, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
        self.fields['license_number'].required = False
        try:
            self.user = self.context.get('request').user
            if not self.user.is_authenticated:
                raise serializers.ValidationError({'message': 'کاربر وارد نشده است'})
            self.get_user = CustomUser.objects.get(id=self.user.id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'message': 'کاربر با این مشخصات یافت نشد'})

    def validate(self, attrs):
        if Profile.objects.filter(user=self.get_user).exists():
            raise serializers.ValidationError('کاربر با این مشخصات قبلا ثبت شده است')
        return attrs

    def create(self, validated_data):
        self.profile = Profile.objects.create(user=self.get_user, is_trappist=True, **validated_data)
        return validated_data

    def to_representation(self, instance):
        instance['username'] = self.get_user.username
        instance['user_id'] = self.profile.id
        instance['is_trappist'] = True
        return instance
