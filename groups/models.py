from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)

    def get_group_name(self):
        return self.name

    def __str__(self):
        return self.name
