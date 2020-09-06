from django.db import models
from rest_framework.authtoken.models import Token


class PersonData(models.Model):
    id = models.BigAutoField(primary_key=True)
    enabled = models.BooleanField(blank=False, null=False)
    guid = models.UUIDField(blank=False, null=False)

    class Meta:
        db_table = 'person_data'

    def get_dict(self):
        dict_obj = {'enabled': self.enabled if self.enabled else None,
                    'guid': self.guid
                    }
        return dict_obj

    def __str__(self):
        return 'Person_Data: ' + self.guid


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    city = models.CharField(max_length=30, blank=False, null=False)
    data = models.OneToOneField(PersonData, on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'person'

    def get_dict(self):
        dict_obj = {'first_name': self.first_name if self.first_name else None,
                    'last_name': self.last_name if self.last_name else None,
                    'city': self.city if self.city else None
                    }
        return dict_obj

    def __str__(self):
        return 'Person: ' + self.first_name + ' ' + self.last_name

