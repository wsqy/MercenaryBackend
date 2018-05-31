import xadmin
from .models import ResourceCategory, ResourceMaterial


class ResourceMaterialInline:
    model = ResourceMaterial
    extra = 0


class ResourceCategoryAdmin:
    list_display = ['id', 'title']
    inlines = [ResourceMaterialInline]


class ResourceMaterialAdmin:
    list_display = ['id', 'title']


xadmin.site.register(ResourceCategory, ResourceCategoryAdmin)
xadmin.site.register(ResourceMaterial, ResourceMaterialAdmin)
