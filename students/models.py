from django.db import models

# Create your models here.

class Students(models.Model):
    s_id=models.IntegerField(primary_key=True)
    s_name=models.CharField(max_length=50)
    s_mail=models.EmailField()
    s_contact=models.CharField(max_length=10)

    def __str__(self):
        return self.s_name