from django.contrib import admin

from festival_app.models import Application, Scene


@admin.register(Application)
class AdminApplication(admin.ModelAdmin):
    pass


@admin.register(Scene)
class AdminScene(admin.ModelAdmin):
    list_display = ['get_title_display']
