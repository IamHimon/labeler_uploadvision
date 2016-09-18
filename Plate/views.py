#encoding:utf-8
from django.shortcuts import render
#from imageSearchModel import search_img
import time,os
from django import forms
from django.http import HttpResponse
import json
import sys
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf-8')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMG_DIR = "/car/static/upload/"
COUNTDIR = BASE_DIR+"/car/static/count.txt"
upload_path = BASE_DIR + BASE_IMG_DIR
DIR = BASE_DIR+"/car/static/upload/"
PlateDIR = BASE_DIR+"/car/static/plateTxt/"
'''
class plateForm(forms.Form):
    imgName = forms.CharField()
    plateImg = forms.FileField()
'''

def handle_uploaded_file(f,ImgType,i):
   #newImageName = str(time.time()).split(".")[0]
   destination = open(BASE_DIR+BASE_IMG_DIR+str(i)+"."+ImgType, 'wb')
   for chunk in f.chunks():
      destination.write(chunk)
   destination.close()
   #return newImageName
def index(request):
      #return HttpResponse("Hello world ! ")
     #imgName = request.GET.get('url')
     #context['error'] = 'system exception'	
     return render(request, 'index.html')
def manage(request):
     imgList = []
     context = {}
     with open("plate.txt","a+") as f:
        lines = f.readlines()
        for line in lines:
          line = line.strip()
          arr = line.split("\t")
          name = arr[0]
          path = DIR+name
          w,h = Image.open(path).size
          new_w = 500 * float(arr[3]) / w
          new_h = 500 * float(arr[4]) / h
           
          new_x = 500 * float(arr[1]) / w
          new_y = 500 * float(arr[2]) / h
          arr[1] = new_y
          print(arr[1])
          arr[2] = new_x
          arr[3] = new_w
          arr[4] = new_h
          imgList.append(arr)
     context['imgList'] = imgList   
     context['hello'] = "hello111"   
     #print(imgList)
     return render(request, 'manage.html',context)

def getCount():
    with open(COUNTDIR,"r") as f:
      lines = f.readlines()
      line = lines[0]
      count = int(line)+1
    with open(COUNTDIR,"wb") as f:
       f.write(str(count))
    return count
def sub(request):
      #return HttpResponse("Hello world ! ")
     #imgName = request.GET.get('url')
     #context['error'] = 'system exception'	
     '''
     if request.method == "POST":
        pf = plateForm(request.POST,request.FILES)
        if pf.is_valid():
            imgName = uf.cleaned_data['username']
            plateImg = uf.cleaned_data['headImg']
            return HttpResponse('upload ok!')
    '''
     i = getCount()
     x = request.POST.get('x')
     y = request.POST.get('y')
     w = request.POST.get('w')
     h = request.POST.get('h')
     #print(request.FILES['file'])
     imgType = request.FILES['file'].name.split(".")[1]
     handle_uploaded_file(request.FILES['file'],imgType,i)
     print("坐标=======>>>",x,y,w,h)
     if(x !=None and y != None and w!= None and h != None):
        line = str(i)+"."+imgType+"\t"+x+"\t"+y+"\t"+w+"\t"+h
        with open(PlateDIR+str(i)+".txt","w") as f:
           f.write(line+"\n")
        return HttpResponse("1")
     else:
        return HttpResponse("0")

	













