from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Stats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER_ID')
    stat_id = models.AutoField(primary_key=True, db_column='STAT_ID')
    voltage = models.DecimalField(max_digits=7, decimal_places=3, db_column='VOLTAGE')
    current = models.DecimalField(max_digits=7, decimal_places=3, db_column='CURR')
    power = models.DecimalField(max_digits=7, decimal_places=3, db_column='POWER')
    time_when_measured = models.DateTimeField(auto_now_add=True, db_column='TIME_WHEN_MEASURED')

    class Meta:
        db_table = 'STATS'

    def get_absolute_url(self):
        return reverse('stats:show_stats', kwargs={'user_id': self.user_id, 'stat_id': self.pk})

    def __str__(self):
        return 'Measurement number {}, measured on {}, for user {}, with voltage {}V, current {}A, and power {}W.'.format(
            self.pk,
            self.time_when_measured,
            self.user.username,
            self.voltage,
            self.current,
            self.power
        )
