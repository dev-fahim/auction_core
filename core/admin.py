from django.contrib import admin


# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'guid', 'created', 'updated', ]


class BaseVerifiedAdmin(BaseAdmin):
    readonly_fields = BaseAdmin.readonly_fields + ['is_verified', 'verification_timestamp', ]


class BaseCreatedAdmin(BaseAdmin):
    readonly_fields = BaseAdmin.readonly_fields + ['created_by', ]


class BaseCreatedWithVerifiedAdmin(BaseVerifiedAdmin):
    readonly_fields = BaseVerifiedAdmin.readonly_fields + ['created_by', ]
