from django.db import models
from django.urls import reverse
from django.conf import settings

from conf.model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name='نام')
    parent_category = models.ForeignKey('self', verbose_name="دسته بندی پدر", blank=True, null=True,
                                        on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='تصویر', upload_to='user_images', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    color = models.TextField(verbose_name='رنگ', blank=True, null=True)
    index = models.IntegerField(default=0, verbose_name="مرتب سازی بر اساس عدد - هرچه کوچکتر مقدم تر")

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی'
        db_table = 'category'

    def __str__(self):
        return self.name


class UserCategory(BaseModel):
    category = models.ForeignKey(Category, verbose_name='دسته بندی', on_delete=models.CASCADE)
    user = models.ForeignKey('account.Trappist', verbose_name='کاربر', on_delete=models.CASCADE)
    price = models.BigIntegerField(verbose_name='قیمت', blank=True, null=True)
    is_valid = models.BooleanField(verbose_name='فعال')


class Post(BaseModel):
    status_choices = (
        ('draft', 'پیش نویس'),
        ('published', 'منتشر شده')
    )
    comment_choices = (
        ('open', 'باز'),
        ('closure', 'بسته')
    )
    title = models.CharField(verbose_name='عنوان', max_length=200)
    image = models.ImageField(verbose_name='تصویر', upload_to='user_images', null=True, blank=True)
    body = models.TextField(verbose_name='محتوا', blank=True, null=True)
    published_date = models.BigIntegerField(verbose_name='رمان انتشار', blank=True, null=True)
    status = models.CharField(verbose_name='وضعیت', max_length=20, choices=status_choices, blank=True, null=True)
    comment_status = models.CharField(verbose_name='وضعیت کامنت', max_length=20, choices=comment_choices, blank=True,
                                      null=True)
    views = models.PositiveIntegerField(verbose_name='تعداد بازدید کنندگان', default=0, blank=True, null=True)
    author = models.ForeignKey('account.Trappist', verbose_name='نویسنده', on_delete=models.CASCADE,
                               related_name='author')
    category = models.ForeignKey('Category', verbose_name='دسته بندی', on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField('Tag', verbose_name='تگ ها', blank=True, null=True)

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
        db_table = 'post'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detailbyid', kwargs={
            'article_id': self.id
        })

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


class Tag(BaseModel):
    name = models.CharField(verbose_name='نام', max_length=30, unique=True)
    slug = models.SlugField(verbose_name='اسلاگ', default='no-slug', max_length=60, blank=True, null=True)

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'
        db_table = 'tag'

    def __str__(self):
        return self.name


class Comment(BaseModel):
    body = models.TextField(verbose_name='محتوا', max_length=300)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='نویسنده', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='پست', on_delete=models.CASCADE, related_name='post')
    parent_comment = models.ForeignKey('self', verbose_name="کامنت پدر", blank=True, null=True,
                                       on_delete=models.CASCADE)
    is_enable = models.BooleanField(verbose_name='فعال', default=False, blank=False, null=False)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = 'نظرات'
        db_table = 'comment'

    def __str__(self):
        return self.body
