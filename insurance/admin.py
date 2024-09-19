from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CustomerQuestion)
admin.site.register(Category)
admin.site.register(Policy)
admin.site.register(PolicyHolder)
admin.site.register(PolicyHolderPolicy)
