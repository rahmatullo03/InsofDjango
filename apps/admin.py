from django.contrib import admin
from django.utils.html import format_html

from apps.models import C, P, Icon, User





@admin.register(C)
class CategoryAdmin(admin.ModelAdmin):
    exclude = 'slug',


@admin.register(P)
class ProductAdmin(admin.ModelAdmin):
    exclude = 'slug',
    list_display = 'id','name','price','images','is_available'

    @admin.display(empty_value='1')
    def images(self,obj):
        photo = obj.image
        return format_html("<img src='{}' style='width: 50px' />'",photo)

    @admin.display(empty_value='1')
    def c_name(self,obj):
        return obj.category.name

    @admin.display(empty_value='1')
    def is_available(self, obj):
        photo = 'fas fa-check-circle'
        photo2 = 'fas fa-minus'
        if obj.quantity != 0:
            return format_html('<span class="{}" </span>', photo)
        else:
            return format_html("<span class='{}' <span/>", photo2)


@admin.register(Icon)
class IconicAdmin(admin.ModelAdmin):
    pass
