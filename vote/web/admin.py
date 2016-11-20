from django.contrib import admin
from .models import Person,IP

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name','ticket','isOpen')
    fields = ('name','ticket','isOpen')
    
admin.site.register(Person,PersonAdmin)
admin.site.register(IP)
