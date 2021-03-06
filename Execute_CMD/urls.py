"""Execute_CMD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from work import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cmd_run.html$', views.Execution.as_view()),
    url(r'^server_add.html$', views.Server_add.as_view()),
    url(r'^ops_log.html$', views.Ops_log.as_view()),
    url(r'^ops_log.html/(.+)$', views.Ops_log_detail.as_view()),
    url(r'^logId.html$', views.Log_id.as_view()),
    url(r'^logId.html/(.+)$', views.Log_id_detail.as_view()),

    # url(r'^ops_log.html/(.+)$', views.Redis_stat.as_view()),

]
