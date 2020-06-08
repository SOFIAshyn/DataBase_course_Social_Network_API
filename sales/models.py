from django.db import models


class Sale(models.Model):
    SALE_DURATIONS_NAMES = (
        (1, 'One Day'),
        (7, 'Week')
    )
    percent = models.IntegerField()
    duration = models.IntegerField(choices=SALE_DURATIONS_NAMES)

    # TODO: set percent to be from 0 to 100

    def __str__(self):
        return self.duration
