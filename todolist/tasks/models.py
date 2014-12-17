from datetime import date
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

PRIORITY_CHOICES = (
    (1, '1 (Low)'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5 (High)'),
)

STATE_CHOICES = (
    (1, 'To do'),
    (2, 'Doing'),
    (3, 'Done'),
)


class Tasks(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    description = models.TextField()
    priority = models.IntegerField(default=3, choices=PRIORITY_CHOICES)
    state = models.IntegerField(default=1, choices=STATE_CHOICES)
    due_date = models.DateField()

    @property
    def is_past_due(self):
        if date.today() > self.due_date:
            return True
        return False