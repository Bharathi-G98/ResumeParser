import os
import django
import docx2txt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SearchResume.settings")
django.setup()
import pandas as pd
from rsearch.models import Company,College,Degree

col=[]
dat=pd.read_csv("C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\colleges.csv")
col=list(dat.columns.values)
col=list(dict.fromkeys(col))

for j in col:
    i=j.replace('.','')
    i=i.replace(',','')
    i=i.replace('(','')
    i=i.replace(')','')
    i=i.split()
    i=' '.join(i)
    col[col.index(j)]=i
    c=College(collegeName=i)
    c.save()

col=[]
data=pd.read_csv("C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\companies.csv")
col=list(data.columns.values)
col=list(dict.fromkeys(col))

for j in col:
    i=j.replace('.','')
    i=i.replace(',','')
    i=i.replace('(','')
    i=i.replace(')','')
    i=i.split()
    i=' '.join(i)
    col[col.index(j)]=i
    c=Company(companyName=i)
    c.save()

col=[]
fname="C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\degrees.docx"

tempo = fname
tempo = docx2txt.process(fname)
deg=[]
word=""
for i in tempo:
    i=i.replace('\t','')
    if i!='\n':
        word+=i
    else:
        if(word):
            word=word.replace('.','')
            if word[0]==' ':
                word=word[1:]
            deg.append(word)
        word=""
deg.append('Twelveth')

deg=list(dict.fromkeys(deg))


for i in deg:
    d=Degree(degreeName=i)
    d.save()
