from django.db import models
from groups.models import Group
from sales.models import Sale


class Editor(models.Model):
    group = models.ManyToManyField(Group)
    default_price = models.IntegerField()
    sale = models.ForeignKey(Sale, on_delete=models.DO_NOTHING, blank=True, null=True)
    sale_started = models.DateTimeField(default=None)

    def __str__(self):
        groups = []
        for group in self.group.all():
            groups.append(group.name)
        return ", ".join(groups)
