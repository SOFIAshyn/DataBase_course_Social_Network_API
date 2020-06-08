from django.db import models
from django.contrib.auth.models import AbstractUser
from groups.models import Group
from networks.models import Network


class User(AbstractUser):
    ROLE_CHOICES = (
        (1, 'Author'),
        (2, 'Customer')
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0])
    group = models.ManyToManyField(Group, related_name='participants', blank=True)
    networks = models.ForeignKey(Network, on_delete=models.CASCADE, null=True)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def is_author(self):
        return self.role == self.ROLE_CHOICES[1][0]

    def is_customer(self):
        return self.role == self.ROLE_CHOICES[0][0]

    def __str__(self):
        return f"{self.id}, role: {self.role}"
