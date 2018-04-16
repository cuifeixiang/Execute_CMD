from django.db import models


class Server_Info(models.Model):
    """server information"""

    ip = models.GenericIPAddressField(max_length=15, db_index=True)
    port = models.IntegerField()
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = "server_information"

