from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from work.execute_cmd import *
from work.ops_log_redis import *
from work import models
import time
import gevent


class Execution(View):

    obj = models.Server_Info.objects.all()

    def get(self, request, *args, **kwargs):
        return render(request, "cmd_run.html", {"server": self.obj})

    def post(self, request, *args, **kwargs):
        result_list = []

        command = request.POST.get('cmd')
        if command:
            result_cmd = Command_Run()
            for host in self.obj:
                result = result_cmd.cmd_run(command, host.ip, host.port, host.username, host.password)
                result_list.append(result)
            ops_log = Ops_log_redis()
            log_key = time.strftime("%Y%m%d%H%M%S", time.localtime())
            ops_log.lpush_insert(log_key, "%s" % result_list)
            return render(request, "cmd_run.html", {"server": self.obj, "result": result_list})
        else:
            return render(request, "cmd_run.html", {"server": self.obj})


class Server_add(View):
    """服务器添加"""

    def get(self, request, *args, **kwargs):
        return render(request, "server_add.html")

    def post(self, request, *args, **kwargs):
        # 清空表
        models.Server_Info.objects.all().delete()
        result = ""
        server_info = request.POST.get("server_info")
        server_info = server_info.strip().split("\r\n")
        try:
            for server in server_info:
                server = server.strip().split(" ")
                server = [x for x in server if x != '']    # 删除列表中的空字符元素
                ip = server[0]
                port = server[1]
                username = server[2]
                password = server[3]
                obj = models.Server_Info.objects.filter(ip=ip).all()
                if obj:
                    result = "%s exist" % ip
                else:
                    models.Server_Info.objects.create(ip=ip, port=port, username=username, password=password)
                    result = "serever add success!!!"
        except IndexError as e:
            result = "添加失败，错误: %s" % e

        return render(request, "server_add.html", {"result": result})


class Ops_log(View):
    """get ops log"""

    def get(self, request, *args, **kwargs):
        ops = Ops_log_redis()
        result = ops.lpush_get("20200724182538")
        print(ops.lpush_get("20200724182538"))
        return render(request, "ops_log.html", {"result": eval(result)})
