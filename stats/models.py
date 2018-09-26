from django.db import models
from django.urls import reverse


# Create your models here.


class Stats(models.Model):
    stat_id = models.AutoField(primary_key=True, db_column='STAT_ID')
    user_id = models.CharField(max_length=30, db_index=True, db_column='USER_ID')
    voltage = models.DecimalField(max_digits=7, decimal_places=3, db_column='VOLTAGE')
    current = models.DecimalField(max_digits=7, decimal_places=3, db_column='CURR')
    power = models.DecimalField(max_digits=7, decimal_places=3, db_column='POWER')
    time_when_measured = models.DateTimeField(auto_now_add=True, db_column='TIME_WHEN_MEASURED')

    class Meta:
        db_table = 'STATS'

    def get_absolute_url(self):
        return reverse('stats:show_stats', kwargs={'stat_id': self.pk})

    def __str__(self):
        return 'Measurement number {}, measured on {}, for user {}.'.format(
            self.pk,
            self.time_when_measured,
            self.user_id,
        )
