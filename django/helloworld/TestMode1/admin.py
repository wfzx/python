from django.contrib import admin
from TestMode1.models import Test,Tag,Contact

class TagInline(admin.TabularInline):
    model = Tag

class ContactAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    fieldsets = (
        ['Main',{
            'fields':('name','email'),
        }],
        ['Advance',{
            'classes':('collapse',),
            'fields':('age',),
        }]
    )

admin.site.register(Contact,ContactAdmin)
admin.site.register([Test])