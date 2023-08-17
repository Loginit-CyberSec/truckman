from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

#client model
class Client(models.Model):
    #admin = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to='companies_logo/')
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=10, default='USD')
    country = models.CharField(max_length=30, default='Kenya')
    #phone_code = models.CharField(max_length=5, default='1') 
    '''
    def get_localized_datetime(self, datetime_value):
        user_timezone = timezone.pytz.timezone(self.timezone)
        localized_datetime = datetime_value.astimezone(user_timezone)
        return localized_datetime
    '''
    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    # Specify a unique related_name for groups and user_permissions
    custom_groups = models.ManyToManyField(
        Group,
        verbose_name='custom groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    custom_user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='custom user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)