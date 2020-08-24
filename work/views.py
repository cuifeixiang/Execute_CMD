# views
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from work.execute_cmd import *
from work.ops_log_redis import *
from work import models
import time
import gevent


class Execution(View):

    obj = models.Server_Info.objects.values("ip")

    def get(self, request, *args, **kwargs):
        return render(request, "cmd_run.html", {"server": self.obj})

    def post(self, request, *args, **kwargs):

        command = request.POST.get('cmd')
        if command:
            result_cmd = Command_Run()
            ops_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for host in self.obj:
                result = result_cmd.cmd_run(command, host.ip, host.port, host.username, host.password)
                print(result.get('ip'), result.get('result'))
                models.Ops_log.objects.create(ops_time=ops_time, ip=result.get('ip'), result=result.get('result'))
            return redirect("/ops_log.html")
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
        result = models.Ops_log.objects.all()
        # print(eval(result))
        return render(request, "ops_log.html", {"result": result})


class Ops_log_detail(View):
    """ops logs detail"""

    def get(self, request, log_id):
        result = ""
        try:
            if log_id:
                result = models.Ops_log.objects.filter(id=log_id)
        except IndexError as e:
            result = "ERROR: %s" % e
        return render(request, 'log_detail.html', {'result': result})


class Logs_id(View):
    """每个执行任务的id"""

    def get(self, request, *args, **kwargs):
        pass


class Redis_stat(View):
    """监控redis cluster"""

    def get(self, request, *args, **kwargs):
        pass


