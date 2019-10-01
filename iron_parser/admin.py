from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(GooseBase)
admin.site.register(Opponent)
admin.site.register(OpponentGoose)
admin.site.register(Check)
admin.site.register(SubCheck)