from django.db import models

# Create your models here.


class Account(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    university_id = models.CharField(max_length=30, db_column='UNIVERSITY_ID')
    student_status = models.CharField(max_length=30, db_column='STUDENT_STATUS')
    color_scheme = models.CharField(max_length=30, null=True, db_column='COLOR_SCHEME')

    class Meta:
        db_table = 'ACCOUNT'

    def __str__(self):
        return '{}: {}'.format(self.university_id, self.student_status)
