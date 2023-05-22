from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.
class TodoItem(models.Model):
  title = models.CharField(max_length=255)
  date = date.today()
  author= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, default=None
    )
  checked = models.BooleanField(default=False)
  def __str__(self):
    return f'{self.id} {self.title}'