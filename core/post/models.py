from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models.profile import validate_is_not_trappist, validate_is_trappist

from conf.model import BaseModel


class Category(BaseModel):
    parent_category = models.ForeignKey('self', verbose_name="دسته بندی پدر", blank=True, null=True,
                                        on_delete=models.CASCADE, related_name='parents_category')
    name = models.CharField(max_length=100, verbose_name='نام', unique=True)
    image = models.ImageField(verbose_name='تصویر', upload_to='category_images', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    color = models.TextField(verbose_name='رنگ', blank=True, null=True)
    index = models.IntegerField(default=0, verbose_name="مرتب سازی بر اساس عدد - هرچه کوچکتر مقدم تر")

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی'
        db_table = 'category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent_category is not None:
            self.index = self.parent_category.index + 1
        super(Category, self).save(*args, **kwargs)


class UserCategory(BaseModel):
    user = models.ForeignKey('account.Profile', on_delete=models.CASCADE,
                             verbose_name='کاربر', related_name='user_category', validators=[validate_is_trappist])
    category = models.ForeignKey(Category, verbose_name='دسته بندی', on_delete=models.CASCADE,
                                 related_name='user_category')
    is_valid = models.BooleanField(verbose_name='معتبر', default=False)
    is_active = models.BooleanField(verbose_name='فعال', default=False)

    class Meta:
        verbose_name = 'دسته بندی کاربر'
        verbose_name_plural = verbose_name
        db_table = 'user_category'

    def __str__(self):
        return f'{self.user.last_name}'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class TrappistCategoryPrice(BaseModel):
    user_category = models.ForeignKey(UserCategory, on_delete=models.CASCADE, related_name='category_price')
    time = models.PositiveIntegerField(verbose_name='رمان', blank=True, null=True)
    add_time = models.PositiveIntegerField(verbose_name='رمان_اضاقه', blank=True, null=True)
    price = models.BigIntegerField(verbose_name='قیمت')
    add_price = models.BigIntegerField(verbose_name='قیمت_اضاقه', blank=True, null=True)
    is_valid = models.BooleanField(verbose_name='معتبر', default=False)

    class Meta:
        verbose_name = 'قیمت تخصص درمانگر'
        verbose_name_plural = verbose_name
        db_table = 'trappist_category_price'

    def __str__(self):
        return self.trappist + ' - ' + self.price


class Post(BaseModel):
    status_choices = (
        ('draft', 'پیش نویس'),
        ('published', 'منتشر شده')
    )
    comment_choices = (
        ('open', 'باز'),
        ('closure', 'بسته')
    )

    author = models.ForeignKey('account.Profile', on_delete=models.CASCADE,
                               verbose_name='کاربر', related_name='posts')
    category = models.ForeignKey(Category, verbose_name='دسته بندی', on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='posts')
    tags = models.ManyToManyField('Tag', verbose_name='تگ ها', related_name='posts')
    title = models.CharField(verbose_name='عنوان', max_length=200)
    body = models.TextField(verbose_name='محتوا', blank=True, null=True)
    published_date = models.BigIntegerField(verbose_name='رمان انتشار', blank=True, null=True)
    status = models.CharField(verbose_name='وضعیت', max_length=20, choices=status_choices, blank=True, null=True)
    comment_status = models.CharField(verbose_name='وضعیت کامنت', max_length=20, choices=comment_choices, blank=True,
                                      null=True)
    views = models.PositiveIntegerField(verbose_name='تعداد بازدید کنندگان', default=0, blank=True, null=True)

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


class PostFile(BaseModel):
    post = models.ForeignKey(Post, verbose_name='پست', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(verbose_name='فایل', upload_to='post_files', blank=True, null=True)
    is_main = models.BooleanField(verbose_name='فایل اصلی', default=False)
    is_valid = models.BooleanField(verbose_name='معتبر', default=True)
    order = models.PositiveIntegerField(verbose_name='ترتیب', blank=True, null=True)

    class Meta:
        verbose_name = 'فایل های پست'
        verbose_name_plural = verbose_name
        db_table = 'post_file'

    def __str__(self):
        return f'{self.post} - {self.is_main} - {self.is_valid}'


class PostRate(BaseModel):
    user = models.ForeignKey('account.Profile', on_delete=models.CASCADE, verbose_name='کاربر',
                             related_name='post_retes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست', related_name='rates')
    rate = models.IntegerField(verbose_name='امتیاز', validators=[MinValueValidator(0), MaxValueValidator(5)],
                               blank=True, null=True)
    like = models.BooleanField(verbose_name='لایک', blank=True, null=True)

    class Meta:
        unique_together = ('user', 'post',)
        verbose_name = 'امتیاز پست'
        verbose_name_plural = verbose_name
        db_table = 'post_rate'

    def __str__(self):
        return f'{self.post} - {self.rate}'


class Tag(BaseModel):
    name = models.CharField(verbose_name='نام', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True, null=True)

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'
        db_table = 'tag'

    def __str__(self):
        return self.name


class Comment(BaseModel):
    user = models.ForeignKey('account.Profile', on_delete=models.CASCADE,
                             verbose_name='کاربر', related_name='comments')
    parent_comment = models.ForeignKey('self', verbose_name="کامنت پدر", blank=True, null=True,
                                       on_delete=models.CASCADE, related_name='parents_comment')
    post = models.ForeignKey(Post, verbose_name='پست', on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='محتوا', max_length=300)
    is_enable = models.BooleanField(verbose_name='فعال', default=True, blank=False, null=False)
    index = models.IntegerField(default=0, verbose_name="مرتب سازی بر اساس عدد - هرچه کوچکتر مقدم تر")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = 'نظرات'
        db_table = 'comment'

    def save(self, *args, **kwargs):
        if self.parent_comment is not None:
            self.index = self.parent_comment.index + 1
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.body
