from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from work.execute_cmd import *
from work import models
import gevent

class Execution(View):

    obj = models.Server_Info.objects.all()

    def get(self, request, *args ,**kwargs):
        return render(request, "cmd_run.html", {"server": self.obj})

    def post(self, request, *args ,**kwargs):
        result_list = []

        command = request.POST.get('cmd')
        if command:
            result_cmd = Command_Run()
            for host in self.obj:
                result = result_cmd.cmd_run(command,host.ip, host.port, host.username, host.password)
                result_list.append(result)
            return render(request, "cmd_run.html", {"server": self.obj,"result": result_list})
        else:
            return render(request, "cmd_run.html", {"server": self.obj})


class Server_add(View):
    """服务器添加"""

    def get(self, request, *args, **kwargs):
        return render(request, "server_add.html")

    def post(selfr, request, *args, **kwargs):
        result = ""
        server_info = request.POST.get("server_info")
        server_info = server_info.strip().split("\r\n")
        try:
            for server in server_info:
                server = server.strip().split(" ")
                server = [ x for x in server if x != '' ]    # 删除列表中的空字符元素
                ip = server[0]
                port = server[1]
                username = server[2]
                password = server[3]
                obj = models.Server_Info.objects.filter(ip=ip).all()
                if obj:
                    result = "%s exist" %ip
                else:
                    models.Server_Info.objects.create(ip=ip, port=port, username=username, password=password)
                    result = "serever add success!!!"
        except IndexError as e:
            result = "添加失败，错误: %s" % e

        return render(request, "server_add.html",{"result": result})