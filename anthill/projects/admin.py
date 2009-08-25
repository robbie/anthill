from django.contrib import admin
from django.contrib.contenttypes import generic
from anthill.projects.models import Project, Role, Link
from feedinator.models import Subscription

class RoleInline(admin.TabularInline):
    model = Role

class LinkInline(admin.TabularInline):
    model = Link

class FeedInline(generic.GenericTabularInline):
    model = Subscription

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'official')
    list_filter = ('official',)
    inlines = [LinkInline, FeedInline, RoleInline]

admin.site.register(Project, ProjectAdmin)
