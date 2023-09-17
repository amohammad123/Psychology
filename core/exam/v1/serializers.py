from rest_framework import serializers
from conf.model import MyModelSerializer
from django.core import exceptions
from django.db.models import Avg

from account.v1.serializers.profile import BaseProfileSerializer
from package.models import Package
from exam.models import Test
from post.v1.serializers.category import BaseCategorySerializer


class CategoriesExamSerializer(MyModelSerializer):
    category = BaseCategorySerializer(many=True)

    class Meta:
        model = Test
        exclude = ['is_deleted', 'create_date', 'update_date']

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     # rep['rate'] = instance.rates.all().aggregate(rate=Avg('rate'))['rate'] or 0
    #     rep['like_count'] = instance.rates.filter(like=True).count()
    #     rep['comment_count'] = instance.rates.filter(comment__isnull=False).count()
    #
    #     return rep
