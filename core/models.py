from django.db import models

# Create your models here.
from model_utils.fields import MonitorField

from core.utils.defaults import generate_guid


class BaseModel(models.Model):
    guid = models.CharField(max_length=32, default=generate_guid, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.guid


class VerificationModel(models.Model):
    verification_related_name = '+'

    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name=verification_related_name)
    verification_timestamp = MonitorField(monitor='verified_by')

    class Meta:
        abstract = True

    @property
    def is_verified(self):
        return self.verified_by_id is not None


class CreatedByUserModel(models.Model):
    created_by_related_name = '+'

    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name=created_by_related_name)

    class Meta:
        abstract = True


class ApiKey(BaseModel):
    service_name = models.CharField(max_length=100)
    secret = models.CharField(max_length=32, default=generate_guid, db_index=True)
