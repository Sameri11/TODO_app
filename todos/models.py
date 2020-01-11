from django.contrib.auth.models import User
from django.db import models


class Tasks(models.Model):
    PRIORITY_CHOICE = [
        (1, 'High Priority'),
        (2, 'Medium Priority'),
        (3, 'Low Priority'),
    ]

    STATUS_CHOICE = [
        (1, 'Not started'),
        (2, 'In progress'),
        (3, 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, default='')
    priority = models.IntegerField(choices=PRIORITY_CHOICE, default=2)
    status = models.IntegerField(choices=STATUS_CHOICE, default=1)

    def __str__(self):
        return str(self.name)
