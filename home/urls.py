from django.urls import re_path,path

from .views import hello_page,oneapp,DownloadFile,SearchNow

urlpatterns = [
    re_path(r'^hello$', hello_page,name='home'),
    path(r'one/<int:id>',oneapp,name='one'),
    path(r'one/download',DownloadFile,name='download'),
    path(r'one/search=<slug:value>',SearchNow,name='search'),
]