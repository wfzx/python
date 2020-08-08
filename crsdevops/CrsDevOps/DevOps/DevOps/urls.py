"""DevOps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from Ops.Add import AddEnv,AddServer,AddEnvConn
from Ops.Modify import ModifyEnv,ModifyServer,ModifyEnvConn
from Ops.List import ProjectInfo,EnvList,EnvConnList
from Ops.DelRes import Delete,Restore
from login import admin,invita,sendmail
from Alter.WebHook import WebHookAlter
from .settings import ROOT_HOME
from django.views.static import serve

urlpatterns = [
    path('', admin.login),
    path('login',admin.zc),
    path('Sendmail',sendmail.GetAllEmailAddressOrSendMail),
    path('invita',invita.RanNum),
    path('ProjectInfo', ProjectInfo),
    path('AddServer', AddServer),
    path('ModifyServer', ModifyServer),
    path('EnvList', EnvList),
    path('EnvConnList', EnvConnList),
    path('AddEnv', AddEnv),
    path('AddEnvConn', AddEnvConn),
    path('ModifyEnv', ModifyEnv),
    path('ModifyEnvConn', ModifyEnvConn),
    path('Delete',Delete),
    path('Restore',Restore),
    path('Alter',WebHookAlter),
    path('<path:path>', serve, {'document_root': ROOT_HOME}),
]