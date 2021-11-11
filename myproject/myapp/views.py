from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from myapp import Port_Assets as pa
import calendar
from time import strptime
from django.shortcuts import redirect

# Create your views here.


def home(request):
    
    if request.method=='POST':
        # try:
        d1=request.FILES['txt1']
        d2=request.FILES['txt2']
        return demo(request,d1,d2) 
        # except:
        #     return HttpResponse("<h1 style='text-align:center'>Oops uploaded file are invalid shape or format can't perform matrix multiplication</h1>")
    return render(request,'home.html')

data=None
obj=None

def demo(request,d1,d2):
    global data,obj
    obj=pa.Myclass(d1,d2)
    data=obj.matrix_multiplication()
    checklist=list(data.columns)
    mindate=str(data.index.min())[0:10]
    maxdate=str(data.index.max())[0:10]
    dummy=data.reset_index()
    dummy['day']=dummy['TimeFrame'].dt.day_name()
    mnt=dummy['TimeFrame'].dt.strftime("%m").unique().tolist()
    yr=dummy['TimeFrame'].dt.strftime("%y").unique().tolist()
    day=dummy['day'].unique().tolist()
    mnt=[int(i) for i in mnt]
    mnt=sorted(mnt)
    mnt_name=[]
    for i in mnt:
        mnt_name.append(calendar.month_abbr[i])
    yr=[int('20'+i) for i in yr]
    context={'col':checklist,'month':mnt_name,'year':yr,'day':day,'min':mindate,'max':maxdate}
    return render(request,'home2.html',context)

def aft(request):
    if request.method=='POST':
        r1=request.POST['fav_language']  # Radio button
        check=request.POST.getlist('recommendations')   # Checklist column name
        viw=request.POST['showresult']       # View statistics / Graphical
        if r1=='day':
            t1=request.POST.getlist('dropdown')              # t1 for dropdown
        elif r1=='month':
            t1=request.POST.getlist('dropdown1') 
        else:
            t1=request.POST.getlist('dropdown2') 
        st=request.POST['start']               # Start Date
        ed=request.POST['end']                 # End date
        range_data = obj.dates(data,st,ed)
        
        cumsum = obj.cumsum_result(range_data,r1,t1,check)  

        if viw=='Statistical':
            cal=obj.calculations(cumsum)
            minn=request.POST['min']              # Take expert user data from input type in form.
            lt=request.POST['ltvar']
            lv=request.POST['lvar']
            uv=request.POST['uvar']
            ut=request.POST['utvar']
            maxx=request.POST['max']

            # Set default value for lvar,ltvar etc.
            if len(minn)==0 and len(lt)==0 and len(lv)==0 and len(uv)==0 and len(ut)==0 and len(maxx)==0:
                formula=obj.Formula_calculation(cumsum,-2.53732145332991,-1.75498331932487,-1.2815515655446
                                ,1.2815515655446,1.75498331932487,2.53732145332991)

                return render(request,'table.html',{'data':cal.to_html(),'formula':formula.to_html()})
            else:
                formula=obj.Formula_calculation(cumsum,float(minn),float(lt),float(lv),float(uv),float(ut),float(maxx))
                return render(request,'table.html',{'data':cal.to_html(),'formula':formula.to_html()})
        else:
            plot=obj.myvisual(cumsum,r1)
            return render(request,'graph.html',{'graph':plot.to_html()})
    return redirect('home/')
        
