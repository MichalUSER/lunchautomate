from django.db import models


class EdupageUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    subdomain = models.CharField(max_length=50)

    def __str__(self):
        return self.username
