from django.db import models
from accesses.models import Access


class SystemMessage(models.Model):
    STYLES = (
        (1, 'Assertive'),
        (2, 'Passive-aggressive'),
        (3, 'Aggressive'),
        (4, 'Submissive'),
        (5, 'Manipulative'),
        (6, 'Romantic'),
    )
    style = models.IntegerField(choices=STYLES)
    access = models.ForeignKey(Access, on_delete=models.DO_NOTHING, related_name='messages')
    send_to = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.style}: {self.text}"