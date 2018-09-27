import xadmin
from .models import Company, PartTimeOrder, PartTimeOrderCard, PartTimeOrderSignUp, PartTimeOrderCardSignUp


class CompanyAdmin:
    list_display = ['name', 'telephone', 'address', 'weight', 'status']
    list_editable = ['weight', 'status']
    list_filter = ['name',]


class PartTimeOrderCardInline:
    model = PartTimeOrderCard
    extra = 0


class PartTimeOrderSignUpInline:
    model = PartTimeOrderSignUp
    extra = 0


class PartTimeOrderAdmin:
    list_display = ['id', 'name', 'company', 'settlement_method', 'status', 'liaison']
    list_display_links = ['id', 'name']
    list_editable = ['status', 'liaison', 'settlement_method']
    list_filter = ['company', 'liaison', 'settlement_method']
    inlines = [PartTimeOrderCardInline, PartTimeOrderSignUpInline]


class PartTimeOrderCardSignUpInline:
    model = PartTimeOrderCardSignUp
    extra = 0


class PartTimeOrderCardAdmin:
    list_display = ['id', 'recruit', 'address', 'start_time', 'end_time', 'registration_deadline_time', 'work_time', 'reward', 'status']
    list_display_links = ['id', 'recruit']
    list_editable = ['status', 'registration_deadline_time', 'work_time', 'reward']
    list_filter = ['address', 'recruit', 'status', ]
    inlines = [PartTimeOrderCardSignUpInline,]


class PartTimeOrderSignUpAdmin:
    list_display = ['id', 'user', 'recruit', 'status']
    list_display_links = ['id', 'user', 'recruit']
    list_editable = ['status', ]
    list_filter = ['user', 'recruit', 'status', ]
    search_fields = ['cust_mobile', ]
    inlines = [PartTimeOrderCardSignUpInline,]


class PartTimeOrderCardSignUpAdmin:
    list_display = ['id', 'user', 'recruit', 'sign', 'card', 'status']
    list_display_links = ['id', 'user', 'recruit', 'sign', 'card']
    list_editable = ['status', ]
    list_filter = ['user', 'recruit', 'sign', 'card', 'status', ]


xadmin.site.register(Company, CompanyAdmin)
xadmin.site.register(PartTimeOrder, PartTimeOrderAdmin)
xadmin.site.register(PartTimeOrderCard, PartTimeOrderCardAdmin)
xadmin.site.register(PartTimeOrderSignUp, PartTimeOrderSignUpAdmin)
xadmin.site.register(PartTimeOrderCardSignUp, PartTimeOrderCardSignUpAdmin)



