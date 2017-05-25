from django.contrib import admin

from base.models import Inscription, Group

admin.site.register(Inscription, admin.ModelAdmin)
admin.site.register(Group, admin.ModelAdmin)
