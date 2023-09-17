from rest_framework import serializers
from conf.model import MyModelSerializer
from django.core import exceptions
from django.db.models import Avg

from account.v1.serializers.profile import BaseProfileSerializer
from package.models import Package
from account.v1.serializers.profile import BaseProfileSerializer
from post.v1.serializers.post import BaseTagSerializer
from post.v1.serializers.category import BaseCategorySerializer


class CategoriesPackageSerializer(MyModelSerializer):
    user = BaseProfileSerializer()
    category = BaseCategorySerializer(many=True)
    tags = BaseTagSerializer(many=True)

    class Meta:
        model = Package
        exclude = ['is_deleted', 'create_date', 'update_date', 'parent_package']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['rate'] = instance.rates.all().aggregate(rate=Avg('rate'))['rate'] or 0
        rep['like_count'] = instance.rates.filter(like=True).count()
        rep['comment_count'] = instance.rates.filter(comment__isnull=False).count()

        return rep
