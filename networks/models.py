from django.db import models


class Network(models.Model):
    fb_username = models.CharField(max_length=100, null=True)
    fb_password = models.CharField(max_length=100, null=True)

    inst_username = models.CharField(max_length=100, null=True)
    inst_password = models.CharField(max_length=100, null=True)

    tg_username = models.CharField(max_length=100, null=True)
    tg_password = models.CharField(max_length=100, null=True)

    # TODO: add checker if username exist, but password do not
    # TODO: check if the data is valid

    def get_id(self):
        return self.id if self.id else None

    def __str__(self):
        return f"inst: {self.inst_username if self.inst_username else ' '}, \
        fb: {self.fb_username if self.fb_username else ' '}, \
        tg: {self.tg_username if self.tg_username else ' '}"

