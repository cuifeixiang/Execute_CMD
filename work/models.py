from django.db import models


class Server_Info(models.Model):
    """server information"""

    ip = models.GenericIPAddressField(max_length=15, db_index=True)
    port = models.IntegerField()
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = "app_server_information"


class Ops_log(models.Model):
    """save ops command result log"""

    ops_time = models.CharField(max_length=50)
    ip = models.CharField(max_length=20)
    result = models.CharField(max_length=10240)
    log_id = models.ForeignKey("Log_id", to_field="id", on_delete=models.CASCADE)

    class Meta:
        db_table = "app_ops_command_result_log"


class Log_id(models.Model):
    """log id"""

    ops_time = models.CharField(max_length=50)
    # ops_id = models.ForeignKey("Ops_log", on_delete=models.CASCADE)

    class Meta:
        db_table = "app_log_id"
