from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    UNDERGRAD = 'UN'
    GRADUATE = 'GR'
    PROFESSOR = 'PRO'
    ADMIN = 'AD'
    STATUS_CHOICES = (
        (UNDERGRAD, 'Undergraduate Student'),
        (GRADUATE, 'Graduate Student'),
        (PROFESSOR, 'Professor'),
        (ADMIN, 'Site Admin'),
    )

    user = models.OneToOneField(User, primary_key=True, db_column='USER_ID', on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, db_column='STATUS')
    color_scheme = models.CharField(max_length=30, db_column='COLOR_SCHEME')

    class Meta:
        db_table = 'PROFILE'

    def get_absolute_url(self):
        return reverse('profiles:user_profile')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
