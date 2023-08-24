from django.db import models
from django.core.exceptions import ValidationError

from conf.model import BaseModel


# Create your models here.

class Settings(BaseModel):
    site_name = models.CharField(verbose_name="نام سایت", max_length=200, null=False, blank=False, default='')
    site_description = models.TextField(verbose_name="توضیحات سایت", max_length=1000, null=False, blank=False,
                                        default='')
    site_seo_description = models.TextField(verbose_name="توضیحات سئوی سایت", max_length=1000, null=False, blank=False,
                                            default='')
    site_keywords = models.TextField(verbose_name="کلمات کلیدی وب سایت", max_length=1000, null=False, blank=False,
                                     default='')
    global_header = models.TextField(verbose_name="هدر سایت", null=True, blank=True, default='')
    global_footer = models.TextField(verbose_name="فوتر سایت", null=True, blank=True, default='')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = verbose_name
        db_table = 'site_setting'

    def __str__(self):
        return self.site_name


# models of account and post

# Table User{
#   id int [pk, increment]
#   email email
#   password password
#   type varcharector
#   created_date datetime
#   updated_date datetime
# }
#
# Table UserCode{
#   id int
# }
#
# Table Profile{
#   id int [pk, increment]
#   user int
#   first_name varcharector
#   last_name varcharector
#   description text
#   nationality_code int
#   date_of_birth int
#   gender type
#   created_date datetime
#   updated_date datetime
# }
#
# Table PsyProfile{
#   id int [pk, increment]
#   user int
#   first_name varcharector
#   last_name varcharector
#   about_me text
#   nationality_code int
#   date_of_birth int
#   gender type
#   created_date datetime
#   updated_date datetime
# }
#

# Table Resume{
#   id id
#
# }

# Table Post{
#   id int [pk, increment]
#   image file
#   author int
#   title varcharector
#   content text
#   categoty int
#   status bool
#   created_date datetime
#   updated_date datetime
#   published_date datetime
# }
#
# Table categoty{
#   id int [pk, increment]
#   name varcharector
#   image file
#   description text
#   color text
#   created_date datetime
# }
#
# Table Product{
#   id int [pk, increment]
#   name varcharector
#   image file
#   color text
#   description text
#   categoty int
#   created_date datetime
# }
#
# Table UserProduct{
#   id int
#   product int
#   profile int
#   created_date datetime
#   updated_date datetime
#   price int
# }
