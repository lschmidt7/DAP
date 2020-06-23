from django.contrib import admin

# Register your models here.

from .models import User, Vacancy

admin.site.register(User)
admin.site.register(Vacancy)