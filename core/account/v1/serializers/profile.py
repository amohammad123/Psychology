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
        return super().validate(attrs)

    def create(self, validated_data):
        self.profile = Profile.objects.create(user=self.get_user, **validated_data)
        return validated_data

    def to_representation(self, instance):
        instance['username'] = self.get_user.username
        instance['user_id'] = self.profile.id
        return instance
