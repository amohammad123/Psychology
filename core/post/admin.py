from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(UserCategory)
admin.site.register(TrappistCategoryPrice)
admin.site.register(Post)
admin.site.register(PostFile)
admin.site.register(PostRate)
admin.site.register(Tag)
admin.site.register(Comment)