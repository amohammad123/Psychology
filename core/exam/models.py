from django.db import models
from conf.model import BaseModel


# Create your models here.


class Test(BaseModel):
    category = models.ForeignKey('', verbose_name='')
    name = models.CharField(verbose_name='', max_length=50)
    sub_test = models.ForeignKey('self', verbose_name='')
    time = models.IntegerField(verbose_name='')
    min_age = models.IntegerField(verbose_name='')
    max_age = models.IntegerField(verbose_name='')
    price = models.IntegerField(verbose_name='')
    index = models.IntegerField(verbose_name='')
    explanation = models.TextField(verbose_name='')

    class Meta:
        verbose_name = 'مراحع'
        verbose_name_plural = 'مراجعان'
        db_table = 'client'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserTest(BaseModel):
    user = models.ForeignKey('', verbose_name='')
    test = models.ForeignKey('', verbose_name='')
    score = models.IntegerField(verbose_name='')
    is_valid = models.BooleanField(verbose_name='')
    start_time = models.IntegerField(verbose_name='')
    end_time = models.IntegerField(verbose_name='')

    class Meta:
        verbose_name = 'مراحع'
        verbose_name_plural = 'مراجعان'
        db_table = 'client'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Question(BaseModel):
    type_choices = (
        ()
    )
    body = models.TextField(verbose_name='')
    file = models.FileField(verbose_name='')
    num = models.IntegerField(verbose_name='')
    test = models.ForeignKey(Test, verbose_name='')
    type = models.CharField(verbose_name='', max_length=15, choices=type_choices)
    explanation = models.TextField(verbose_name='')


    class Meta:
        verbose_name = 'مراحع'
        verbose_name_plural = 'مراجعان'
        db_table = 'client'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Answer(BaseModel):
    body = models.TextField(verbose_name='')
    file = models.FileField(verbose_name='')
    num = models.IntegerField(verbose_name='')
    score = models.IntegerField(verbose_name='')
    question = models.ForeignKey(Question, verbose_name='')
    test = models.ForeignKey(Test, verbose_name='')

    class Meta:
        verbose_name = 'مراحع'
        verbose_name_plural = 'مراجعان'
        db_table = 'client'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserAnswer(BaseModel):
    user_test = models.ForeignKey(UserTest, verbose_name='')
    answer = models.ForeignKey(Answer, verbose_name='')
    question = models.ForeignKey(Question, verbose_name='')

    class Meta:
        verbose_name = 'مراحع'
        verbose_name_plural = 'مراجعان'
        db_table = 'client'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
