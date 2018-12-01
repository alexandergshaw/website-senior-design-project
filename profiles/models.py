from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .fields import JSONField


class Profile(models.Model):
    STUDENT = 'ST'
    ADMIN = 'AD'
    STATUS_CHOICES = (
        (STUDENT, 'Student User'),
        (ADMIN, 'Site Admin'),
    )

    user = models.OneToOneField(User, primary_key=True, db_column='USER_ID', on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, db_column='STATUS')
    phase_1_settings = JSONField(null=True, blank=True, db_column='PHASE_1_SETTINGS')
    phase_2_settings = JSONField(null=True, blank=True, db_column='PHASE_2_SETTINGS')
    phase_3_settings = JSONField(null=True, blank=True, db_column='PHASE_3_SETTINGS')

    class Meta:
        db_table = 'PROFILE'

    @staticmethod
    def get_absolute_url():
        return reverse('profiles:user_profile')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
