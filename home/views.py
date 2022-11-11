# from django.shortcuts import render

from django.shortcuts import render,HttpResponse
import django_eel as eels
from home.models import Software
import requests
import os,json
from urllib.parse import urlparse
import winreg
from packaging import version

eels.init('home/templates/home')

###########################
# Hello example

def checkInternet():
	import socket

	Ipaddress=socket.gethostbyname(socket.gethostname())
	print(Ipaddress)

	if Ipaddress == '127.0.0.1':
		return False
	else:
		return True


def hello_page(request): # accept request for hello.html
	if checkInternet():
		# '''Checking if any app is alrady installed ''''
		data = Software.objects.all()
		datalist = [item for item in data]
		software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

		installedapps = [str(item.name).lower() for item in checkIsinstalled(installedapp=software_list,dataapps=datalist)]
		print(installedapps)
	

		datas = [i for i in Software.objects.all()]
	
		for item in datas:
			if str(item.name).lower() in installedapps:
				Software.objects.filter(id=item.id).update(position = "installed")
				Software.objects.filter(id=item.id).update(instapos = True)
			else:
				Software.objects.filter(id=item.id).update(position = "available")
				Software.objects.filter(id=item.id).update(instapos = False)

		# '''Checking if any app update is available or not  ''''
		updates = [item for item in checkUpdate(installedapp=software_list,dapps=datalist)]
		
		for item in datas:
			if item in updates:
				Software.objects.filter(id=item.id).update(update=True)
			else:
				Software.objects.filter(id=item.id).update(update=False)

		data = Software.objects.all()
		return render(request, 'home/home.html',{'data':[1,2,3,4,5],'lists':data,'num':[1,2,3],'pre':'#'})
	else:
		return render(request,'home/refresh.html')

def oneapp(request,id):
	if checkInternet():
		dataid = Software.objects.filter(id = id)

		data = Software.objects.all()
		datalist = [item for item in data]
		software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

		installedapps = [str(item.name).lower() for item in checkIsinstalled(installedapp=software_list,dataapps=datalist)]
	

		datas = [i for i in Software.objects.all()]
	
		for item in datas:
			if str(item.name).lower() in installedapps:
				Software.objects.filter(id=item.id).update(position = "installed")
				Software.objects.filter(id=item.id).update(instapos = True)

			else:
				Software.objects.filter(id=item.id).update(position = "available")
				Software.objects.filter(id=item.id).update(instapos = False)


		data = Software.objects.all()

		# '''Checking if any app update is available or not  ''''
		updates = [item for item in checkUpdate(installedapp=software_list,dapps=datalist)]
		print(data,updates)
		for item in datas:
			if item in updates:
				Software.objects.filter(id=item.id).update(update=True)
			else:
				Software.objects.filter(id=item.id).update(update=False)


		data2  = Software.objects.all()
		print("The url is ",request.META.get('HTTP_REFERER'))
		print("hello i am in single app")
		return render(request,'home/oneapp.html',{'lists':dataid,'alldata':data2,'pre':request.META.get('HTTP_REFERER')})

	else:
		return render(request,'home/refresh.html')

def DownloadFile(request): 
	print("The Downloading is starting....")
	# file_url = "https://cdn.pixabay.com/photo/2018/01/12/10/19/fantasy-3077928__480.jpg"
	# eel.jsDownloadFile({'s':5})
	id = request.POST.get('appid')
	exe = request.POST.get('appexe')

	print("The file is : " ,exe)
	file_url =exe
	a = urlparse(file_url)
	# print(a.path)                    # Output: /kyle/09-09-201315-47-571378756077.jpg
	name = os.path.basename(a.path)
	filename = name.replace('%',"_") if '%' in name else name


	r = requests.get(file_url, stream = True)
	
	def sum(i):
		total=0
		for item in i:
			total+=item
		return total

	def sum2(l):
		t = 0
		for chunk in l:
			for item in chunk:
				t   +=item
		
		return t
		
	def per(n):
		
		t =sum2(n)
		
		with open(f"{filename}",'wb') as exe:
			for chunk in n:
				if chunk:
					p = (sum(chunk)*100)/t
					exe.write(chunk)
					print(f"{p}%")

	c = [item for item in r.iter_content(chunk_size=2048)]
	per(c)

	with open('install.bat','w') as i:
		i.write(f"{filename} /S")

	print("Now Installing the file .>>> ")
	import subprocess
	subprocess.run("install.bat")

	# print(id,exe,settings.BASE_DIR)

	data = json.dumps({'data':34},default=str)
	return HttpResponse(data)
###########################

def foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

def checkUpdate(installedapp,dapps):
	installed = []

	for item in dapps:
		for app in installedapp: 
			if item.name.lower() in str(app['name']).lower() and version.parse(item.version)>version.parse(app['version']):
				print("the item is",item.name)
				installed.append(item)

	return set(installed)
	
def checkIsinstalled(installedapp,dataapps):
	installed = []
	d = False
	for item in dataapps:
		for app in installedapp: 
			if item.name.lower() in str(app['name']).lower():
				installed.append(item)
	
	return set(installed)
	
def FindSoftwareUpadate():
	data = Software.objects.all()
	datalist = [item for item in data]
	software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

	print("Available Updates : ",[(item.name,"update") for item in checkUpdate(installedapp=software_list,dapps=datalist)])
	
def SearchNow(request,value):

	alldata = Software.objects.all()
	data = []
	for item in alldata:
		if  str(value).lower() in str(item.name).lower():
			data.append(item)
	print(data)

	return render(request,'home/oneapp.html',{'lists':data,'alldata':alldata,'pre':request.META.get('HTTP_REFERER')})
# FindSoftwareUpadate()

def DeleteFils():
	files  = os.listdir()
	for item in files:
		if item.split('.')[-1]=='exe' or item.split('.')[-1]=='msi':
			os.remove(item)
		
DeleteFils()
###########################
eels.start('home/hello', size=(300, 200),port=0) # optional for off-line browsing