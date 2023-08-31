from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Test)
admin.site.register(TestPayment)
admin.site.register(UserTest)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserAnswer)