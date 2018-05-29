import xadmin
from .models import ResourceCategory, ResourceMaterial


class ResourceCategoryAdmin:
    list_display = ['id', 'title']


class ResourceMaterialAdmin:
    list_display = ['id', 'title']


xadmin.site.register(ResourceCategory, ResourceCategoryAdmin)
xadmin.site.register(ResourceMaterial, ResourceMaterialAdmin)
