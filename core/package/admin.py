from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Package)
admin.site.register(PackageFile)
# admin.site.register(UserPackage)
admin.site.register(PackagePayment)
admin.site.register(PackageRate)