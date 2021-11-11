import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from time import strptime
from pandas.core import base
import plotly.express as px

class Myclass:
    def __init__(self,path1,path2):
        self.path1=path1
        self.path2=path2

    def matrix_multiplication(self):
        dataR=pd.read_excel(self.path1)
        dataPF=pd.read_excel(self.path2)
        dataR=dataR.set_index(dataR.columns[0])
        dataPF=dataPF.set_index(dataPF.columns[0])
        self.matrix_mul=dataR.dot(dataPF)
        self.matrix_mul.index.name='TimeFrame'
        return self.matrix_mul

 
    """ Params->1. df: DataFrame   2.period: Periods (month/year/particula day) 
        3. DMY_NO(DateMonthYear_No.):Exact no. of DMY  4.single: For particular columns in dataframe. """

    def cumsum_result(self,df,period,DMY_NO,single):
        newdf=df.cumsum()
        newdf=newdf.reset_index()
        newdf['day']=newdf['TimeFrame'].dt.day_name()
        if period=='day':
            dd=newdf[newdf['day'].isin(DMY_NO)]
            del dd['day']
            dd=dd.set_index(dd.columns[0])
            return dd[single]

        elif period=='month':
            mnt=[]
            for i in DMY_NO:
                mnt.append(strptime(i,'%b').tm_mon)
            dd=newdf[newdf['TimeFrame'].dt.month.isin(mnt)]
            del dd['day']
            dd= dd.set_index(dd.columns[0])
            return dd[single]

        elif period=='year':
            DMY_NO=[int(i) for i in DMY_NO]
            dd=newdf[newdf['TimeFrame'].dt.year.isin(DMY_NO)]
            del dd['day']
            return dd.set_index(dd.columns[0])[single]
 
    def dates(self,df,st,ed):
        filt=df.loc[st:ed]
        return filt

    def calculations(self,df):
        lTvar=[]
        uTvar=[]
        
        cal= df.apply(['min','max','std','mean','skew','kurt','median'])
        cal.loc['Sharp']=cal.loc['std'] / cal.loc['min']
        cal.loc['LowerVar']=df.quantile(q=0.05)
        cal.loc['UpperVar']=df.quantile(q=0.9)
        
        for i,j,k in zip(df.columns,cal.loc['LowerVar'].tolist(),cal.loc['UpperVar'].tolist()):
            lower=df[i][df[i]<j]  
            upper=df[i][df[i]>k]
            lTvar.append(lower.mean())
            uTvar.append(upper.mean())
        cal.loc['LowerTvar']=lTvar
        cal.loc['UpperTvar']=uTvar
        return cal

    def Formula_calculation(self,df,Min,LTVar,LVar,UVar,UTVar,Max):
        pd_list=[]    

        std=df.std()
        md=df.median()

        pd_list.append([(i*Min+k)*100 for i,k in zip(std,md)])
        pd_list.append([(i*LTVar+k)*100 for i,k in zip(std,md)])
        pd_list.append([(i*LVar+k)*100 for i,k in zip(std,md)])
        pd_list.append([(i*UVar+k)*100 for i,k in zip(std,md)])
        pd_list.append([(i*UTVar+k)*100 for i,k in zip(std,md)])
        pd_list.append([(i*Max+k)*100 for i,k in zip(std,md)])

        formula=pd.DataFrame(pd_list,columns=df.columns,index=['Min','LowerTVar','LowerVar','UpperVar','UpperTVar','Max'])
        formula.loc['Median']=md*100
        formula=formula.reindex(['Min','LowerTVar','LowerVar','Median','UpperVar','UpperTVar','Max'])
        return formula.round(2)

    ### For Plotly interactive graph8
    def myvisual(self,mydf,per):
        df=mydf.multiply(100)
        mynew=df.reset_index()

        if per=='day':
            mynew=mynew.set_index(mynew.columns[0])
            fig = px.line(mynew)
            return fig
        elif per=='month':
            myplot=mynew.groupby(pd.Grouper(key=mynew.columns[0],freq='M')).sum()
        else:
            myplot=mynew.groupby(pd.Grouper(key=mynew.columns[0],freq='M')).sum()
        
        fig = px.line(myplot)
        return fig



""" For matplotlib graph """

    # def get_graph(self):
    #     buffer=BytesIO()
    #     plt.savefig(buffer,format='png')
    #     buffer.seek(0)
    #     image_png=buffer.getvalue()
    #     graph=base64.b64encode(image_png)
    #     graph=graph.decode('utf-8')
    #     buffer.close()
    #     return graph

    # def visual(self,mydf,per):
    #     plt.switch_backend('AGG')
    #     plt.figure(figsize=(10,5))
    #     plt.title('Assets-Portfolio')
    #     plt.xlabel('TimeFrame')
    #     plt.ylabel('Portfolio')
    #     df=mydf.multiply(100)
    #     mynew=df.reset_index()

    #     if per=='day':
    #         myplot=mynew.groupby(pd.Grouper(key=mynew.columns[0],freq='Y')).sum()
    #     elif per=='month':
    #         myplot=mynew.groupby(pd.Grouper(key=mynew.columns[0],freq='Y')).sum()
    #     else:
    #         myplot=mynew.groupby(pd.Grouper(key=mynew.columns[0],freq='M')).sum()
            
    #     plt.grid()
    #     plt.plot(myplot)
    #     plt.legend(myplot.columns,ncol=3)
    #     graph=self.get_graph()
    #     return graph






