#from django.shortcuts import render, get_object_or_404
#from .models import PersonalDetails, DegreeYear, UserSkillCount, Company, College,Degree
from itertools import chain
#from django.db.models import Q
#from django.core.files.storage import FileSystemStorage
import nltk
import csv
import os
from collections import OrderedDict
#import spacy
import pandas as pd
import re
from nltk.corpus import stopwords
import docx2txt
from nltk.tag import pos_tag
from geotext import GeoText
from find_job_titles import FinderAcora
import tika
from tika import parser
import zipfile
#from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize,sent_tokenize
import mysql.connector

#stanford_classifier = 'C:\\Users\\Lenovo\\stanford-ner-2018-10-16\\classifiers\\english.all.3class.distsim.crf.ser.gz'
#stanford_ner_path = 'C:\\Users\\Lenovo\\stanford-ner-2018-10-16\\stanford-ner.jar'
#st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
short_month={'Jan':'January','Feb':'February','Mar':'March','Apr':'April','May':'May','Jun':'June','Jul':'July','Aug':'August','Sep':'September','Sept':'September','Oct':'October','Nov':'November','Dec':'December'}
pos_head=['CAREER OBJECTIVE','TECHNICAL SKILLS','ACADEMIC ACHIEVEMENTS','WORK EXPERIENCE','EXPERIENCE SUMMARY','PROJECT DETAILS','PROJECT EXPERIENCE','ADDITIONAL ACTIVITIES',
                  'PROFESSIONAL EXPERIENCE','ACADEMIC DISTINCTIONS','PROFESSIONAL SUMMARY', 'PROJECT PROFILE','TOOLS AND APPLICATIONS','ONLINE COURSES','TECHNICAL PROFICIENCY',
                  'CAREER SUMMARY','ADDITIONAL ENGAGEMENTS','ACADEMIC PROJECTS','ADDITIONAL ACTIVITIES','WORK HISTORY',
                  'PUBLIC PROFILES','OTHER PROJECTS TRAININGS UNDERTAKEN','PROJECT DETAILS',
                  'FIELDS OF INTEREST','AREAS OF INTEREST','TECHNICAL EXPERIENCE','TECHNOLOGIES WORKED','LANGUAGES KNOWN',
                  'PROJECT WORK','PROFESSIONAL PROFILE','MINI PROJECTS','COMMUNICATION SKILLS','WORKING EXPERIENCE',
                  'EDUCATION','OVERALL','EDUCATIONAL','ACADEMIC','ACADEMIA',
                  'ABSTRACT','DECLARATION','EMPLOYMENT','PROJECTS','JOBS','JOB',
                 'CERTIFICATIONS','REFERENCE','LICENSES','CONFERENCES','TALKS','HONORS',
                  'AWARDS','INTERESTS','COURSES','HONORS','PUBLICATIONS','PUBLISHED','SCHOLARSHIPS','PERSONAL','OBJECTIVES',
                  'OBJECTIVE','REFERENCES','PUBLICATIONS',
                  'QUALITIES','LINKS','SOCIETIES','EXTRACURRICULAR','EXTRA-CURRICULAR','SUMMER INTERNSHIP/WORK EXPERIENCE',
                  'COMPETANCY','REFERENCE','ASPIRATION',
                  'APPENDIX','ACCOMPLISHMENTS','EXPERTISE','HOBBIES']
Indian_states=["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
def extract_name(resume,e):
    #print(text)
    name=''
    sent=[]
    person=[]
    if not(person):
                s=''
                c=0
                text3=text
                for u in text.split():
                    if u.isupper() and not(u==e):
                        text3=text3.replace(u,u.capitalize())
                for i in text3:
                    if i!='\n':
                        s+=i
                    else:
                        if s:
                            sent.append(s)
                            c+=1
                        s=''
                sent=[i for i in sent if i!=' ' and not(i.isdigit())]
                if e:
                    ind=[sent.index(i) for i in sent if e in i]
                    if ind:
                        ind=ind[0]
                        if ind>6:
                            sent=sent[ind-6:ind+5]
                        else:
                            sent=sent[:ind+(11-ind)]
                        sent=' '.join(sent)
                        sent=sent.split()
                        for i in sent:
                            if i[0].islower():
                                sent.remove(i)
                        sent=' '.join(sent)
                        #replace the colleges with actual names.
                        sent=sent.replace(' Nit ',' NIT ')
                        sent=sent.replace(' Iit ',' IIT ')
                        sent=sent.replace(' Bits ',' BITS ')
                        sent=sent.replace(' Aieee ',' AIEEE ')
                        s=sent.split()
                        #print(text)
                        for text2 in s:
                                if text2.isalpha() and text2[0].isupper() and not(text2=='Vitae') and not(text2.lower() in sk):
                                    #it's taking mysql and big data and shell scriptingand other skills as name. fix.
                                    #print(text2)
                                    #tokenized_text = word_tokenize(text2)
                                    '''
                                    person=[i[0] for i in text2.split() if st.tag(i)[0][1]=='PERSON']
                                    classified_text = st.tag([text2])
                                    if classified_text[0][1][0].isupper():
                                            person.append(classified_text[0][0])
                                            person.append(s[s.index(text2)+1])
                                            break
                                    '''
                                    person.append(text2)
                                    if text3[text3.lower().index(text2.lower())+1]=="\n":
                                     break
                    #person.append(i[0] for i in classified_text if i[1]=='PERSON')

    if person:
      name=person[0]+" "+person[1]
    for i in name:
        if not(i.isalpha()):
            name=name.replace(i,'')
    name=name.replace('docx','')
    name=name.replace('pdf','')
    return name
	
def extract_phoneNum(text):
                 number=''
                 x=text.replace(" ","")
                 x=x.replace("-","")
                 x=x.replace("(","")
                 x=x.replace(")","")
                 n = re.findall(re.compile(r'([9][1][6-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])'), x)
                 num = re.findall(re.compile(r'([6-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])'), x)
                 if n:
                         number=''.join(n[0])
                         number='+'+number
                         return number
                 else:
                         if num:
                             number=''.join(num[0])
                         return number
def extract_email(text):
            email = re.findall('\S+@\S+', text)
            em=''
            for em in email:
                i=em.index('@')
                t=em[i:]
                if '.' in t:
                    break
            if 'mail:' in em:
                if em.index('mail:')==0 or em.index('mail:')==1:
                    em=em[em.index('mail:')+len('mail:'):]

            return em
						 
def extract_skills(resume_text):
            resume_text=resume_text.replace('\n',' ')
            skill_count={}
            resume_text=re.sub(r"[^a-zA-Z0-9]+", ' ', resume_text)
            #removing stop words, using word tokenizing
            data=pd.read_csv("/home/goscale/Downloads/skillsResume.csv")
            skills = list(data.columns.values)
            skillset = []
            for i in skills:
                if i.lower() in resume_text.lower():
                    print(i)
                    ind=resume_text.lower().index(i.lower())
                    if not(resume_text.lower()[ind-1].isalpha())and not(resume_text.lower()[ind+len(i.lower())].isalpha()):
                        #checking if inside word
                        skillset.append(i)
            print("each skill occurs:")
            for i in skillset:
                ind=resume_text.lower().index(i.lower())
                skill_count[i.lower()]=resume_text.lower().count(i.lower())
            print(skill_count)
            return skillset,skill_count
def time(t):
            p=""
            count=0
            time_periods={}
            month=short_month.values()
            m=[]
            for i in month:
                m.append(i.lower())
            for i in t.split():
                p+=i+" "
                #print(i)
                if ('till date') in p.lower() and p.lower().rfind('till date') not in time_periods.keys():
                    count+=1
                    if count==8:
                        count=0
                    time_periods[p.lower().rfind('till date')]='Till Date'
                elif i.lower()==('present') or i.lower()==('current'):
                    count+=1
                    if count==8:
                        count=0
                    time_periods[p.rfind(i)]=i
                elif i.isdigit():
                    if int(i)>1950 and int(i)<2030:
                        count+=1
                        if count==8:
                            count=0
                        time_periods[p.rfind(i)]=i
                elif i.lower() in m:
                    count+=1
                    if count==8:
                            count=0
                    time_periods[p.rfind(i)]=i

                else:
                    continue
            return time_periods,p
def extract_companies_and_year(text,time_periods):
            dat=pd.read_csv("/home/goscale/Downloads/companies.csv")
            text2=text.replace('.','')
            text2=text2.replace('\n','')
            k=text2.lower()
            #for short forms
            col=list(dat.columns.values)
            col_list={}
            for i in col:
                if i.lower() in k:
                    ind=k.index(i.lower())
                    for m in re.finditer(i.lower(), k):
                        if m:
                            if not(k[m.start()-1].isalpha())and not(k[m.end()].isalpha()):
                                #checking if inside word
                                col_list[k.index(i.lower())]=i
                                break
            col_key=list(col_list.keys())
            if col_key:
            #logic: usually college is written first. therefore, yera-year or month year-month year can be written for college.
            #if the duration is afterwards: acees the next 2 time periods: (month year-month year) or (year to year)
                time2=""
                orig_time_val=time_periods.values()
                time_pd={}
                for k in orig_time_val:
                    for m in re.finditer(k,text2):
                        time_pd[m.start()]=m[0]

                time_pd=OrderedDict(sorted(time_pd.items()))
                time_key=list(time_pd.keys())
                #case 1: if college is listed first and time period is before college
                v=''
                if time_key:
                    if time_key[0]<(col_key[0]):
                        #till_key= max(k for k in time_key if k<=col_key[0])
                        for i in time_key:
                            v=''
                            if i<col_key[0]:
                                if time_pd[i].isdigit():
                                    v=' to '
                                time2+=time_pd[i]+' '+v
                        time2=time2[:-3]
                    #case 2: college listed first and time pd is after it
                    v=''
                    c=0
                    if time2=="":
                        for i in time_key:
                            v=''
                            if c==2:
                                break
                            if time_pd[i].isdigit():
                                c+=1
                                v=' to '
                            time2+=time_pd[i]+' '+v
                        time2=time2[:-3]
                    return col_list.values(),time2
                else:
                    return list(col_list.values()),['none']
            else:
                return ["none"],["none"]
def extract_college_and_year(text,time_periods):
            dat=pd.read_csv("/home/goscale/Downloads/colleges.csv")
            text2=text.replace('.','')
            text2=text2.replace('\n','')
            k=text2.lower()
            #for short forms
            col=list(dat.columns.values)
            col_list={}
            for i in col:
                if i.lower() in k:
                    ind=k.index(i.lower())
                    for m in re.finditer(i.lower(), k):
                        if m:
                            if not(k[m.start()-1].isalpha())and not(k[m.end()].isalpha()):
                                #checking if inside word
                                col_list[k.index(i.lower())]=i
                                break

            #col_long=['birla institute of technology and science','','','','','','','','','',]
            if 'birla institute of technology and science' in text2.lower() :
                col_list[k.index('birla institute of technology and science')]='BITS'
            if 'birla institute of science and technology' in text2.lower() :
                col_list[k.index('birla institute of science and technology')]='BITS'
            if 'indian institute of technology' in text2.lower():
                col_list[k.index('indian institute of technology')]='IIT'
            if 'national institute of technology' in text2.lower():
                col_list[k.index('national institute of technology')]='NIT'
            col_key=list(col_list.keys())
            if col_key:
            #logic: usually college is written first. therefore, yera-year or month year-month year can be written for college.
            #if the duration is afterwards: acees the next 2 time periods: (month year-month year) or (year to year)
                time2=""
                orig_time_val=time_periods.values()
                time_pd={}
                for k in orig_time_val:
                    for m in re.finditer(k,text2):
                        time_pd[m.start()]=m[0]

                time_pd=OrderedDict(sorted(time_pd.items()))
                time_key=list(time_pd.keys())
                #case 1: if college is listed first and time period is before college
                v=''
                if time_key:
                    if time_key[0]<(col_key[0]):
                        #till_key= max(k for k in time_key if k<=col_key[0])
                        for i in time_key:
                            v=''
                            if i<col_key[0]:
                                if time_pd[i].isdigit():
                                    v=' to '
                                time2+=time_pd[i]+' '+v
                        time2=time2[:-3]
                    #case 2: college listed first and time pd is after it
                    v=''
                    c=0
                    if time2=="":
                        for i in time_key:
                            v=''
                            if c==2:
                                break
                            if time_pd[i].isdigit():
                                c+=1
                                v=' to '
                            time2+=time_pd[i]+' '+v
                        time2=time2[:-3]
                    return col_list.values(),time2
                else:
                    return list(col_list.values()),['none']
            else:
                return ["none"],["none"]	
def head(text):
            headings1={}
            t=text.upper()
            global tempor
            tempor=tempor.replace('\n ','\n')
            tempor2=tempor.upper()
            for i in pos_head:
                        if i in tempor2:
                            for m in re.finditer(i, tempor2):
                                if tempor[m.start()].isupper() and tempor2[m.start()-1]=='\n':

                                    headings1[m.start()]=i
                                    break
                                continue
                            if 'EXPERIENCE' in i:
                                for j in headings1.values():
                                    if 'EXPERIENCE' in j:
                                        c=0
                                        break
                #check before and after \n also. if not already in headings
            text.replace("&","and")
            tempor2.replace("&","AND")
            c=0
            for m in re.finditer('\nPROJECTS', tempor2):
                if m:
                    c+=1
            if c==1 and tempor[m.start()].isupper():
                    headings1[tempor2.index('PROJECTS')]='PROJECTS'
            c=0
            for m in re.finditer('\nPUBLIC PROFILE', tempor2):
                if m:
                    c+=1
            if c==1 and tempor[m.start()+1].isupper():
                    headings1[tempor2.index('PUBLIC PROFILE')]='PUBLIC PROFILE'
            c=0
            for m in re.finditer('\nPROJECT DESCRIPTION', tempor2):
                if m:
                    c+=1
            if c==1:
                    headings1[tempor2.index('PROJECT DESCRIPTION')]='PROJECT DESCRIPTION'
            c=0
            for m in re.finditer('\nLANGUAGES', tempor2):
                if m:
                    c+=1
            if c==1 and t[m.start()-1]=='\n':
                    headings1[tempor2.index('LANGUAGES')]='LANGUAGES'
            c=0
            for m in re.finditer('\nSKILLS\n', tempor2):
                if m:
                    c+=1
            if c==1:
                    headings1[tempor2.index('SKILLS')]='SKILLS'
            c=0
            for m in re.finditer('\nROLES AND RESPONSIBILITIES', tempor2):
                if m:
                    c+=1
            if c==1:
                    headings1[tempor2.index('\nROLES AND RESPONSIBILITIES')]='ROLES AND RESPONSIBILITIES'
            r = dict(headings1)
            if 'ACADEMIC' in headings1.values() and 'EDUCATION' in headings1.values():
                for b in headings1.keys():
                    if headings1[b]=='ACADEMIC':
                        break
                del r[b]
                headings1=r
            t=tempor2
            if '\nACADEMIC DISTINCTIONS' in t:
                headings1[t.index('ACADEMIC DISTINCTIONS')]='ACADEMIC DISTINCTIONS'
            if '\nACADEMIC QUALIFICATIONS' in t:
                headings1[t.index('ACADEMIC QUALIFICATIONS')]='ACADEMIC QUALIFICATIONS'
            r = dict(headings1)
            if 'ACADEMIC QUALIFICATIONS' in headings1.values() and 'EDUCATION' in headings1.values():
                for b in headings1.keys():
                    if headings1[b]=='EDUCATION':
                        break
                del r[b]
                headings1=r
            if '\nACADEMIC ACHIEVEMENTS' in t:
                headings1[t.index('ACADEMIC ACHIEVEMENTS')]='ACADEMIC ACHIEVEMENTS'
            if '\nACADEMIC AWARDS' in t:
                headings1[t.index('ACADEMIC AWARDS')]='ACADEMIC AWARDS'
            if '\nACADEMIC PROJECTS' in t:
                headings1[t.index('ACADEMIC PROJECTS')]='ACADEMIC PROJECTS'
            headings1=OrderedDict(sorted(headings1.items()))
            return headings1	
def education(text,headings):
            t=tempor.upper()
            headI=''
            global headings2
            edu=""
            edI=[]
            beg=99999
            end=99999
            headings=OrderedDict(sorted(headings.items()))
            for i,j in headings.items():
                 if 'ACADEMIC QUALIFICATIONS'==j or 'EDUCATION'==j or 'EDUCATIONAL'==j or 'ACADEMIC'==j or 'ACADEMIA'==j:
                     headI=i
                     beg=headI
                     break
            k=sorted(list(headings.keys()))
            if not(headI):
                return edu
            for i in range(0,len(k)):
                if k[i]==headI:
                    if not(i+1==len(k)):
                        end=k[i+1]
                        break
                    else:
                        end=len(tempor)-1
                        break
            e=""
            edu=tempor[beg:end+1]
            for t in edu.split():
                if t==text.split()[0]:
                    break
                else:
                    e+=t+" "
            return e	
def exp(text,headings):
            global headings2
            headings=OrderedDict(sorted(headings.items()))
            inde=''
            ind=''
            edu=""
            #t=text.upper()
            headI=99999
            beg=99999
            end=99999
            t=temp=tempor.upper()
            k=sorted(list(headings.keys()))
            if '\nACHIEVEMENTS' in temp:
                headings[t.index('ACHIEVEMENTS')]='ACHIEVEMENTS'
            for i,j in headings.items():
                if 'EMPLOYMENT'==j or 'WORK EXPERIENCE' in j or 'CAREER SUMMARY'==j or 'EXPERIENCE SUMMARY'==j or 'PROFESSIONAL PROFILE'==j or 'PROFESSIONAL EXPERIENCE'==j or 'ORGANIZATIONAL'==j or 'ORGANISATIONAL'==j or 'JOB'==j or 'JOBS'==j or 'WORKING EXPERIENCE'==j or j=="WORK HISTORY":
                        headI=i
                        beg=headI
                        break
            k=sorted(list(headings.keys()))
            for i in range(0,len(k)):
                if k[i]==headI:
                    if not(i+1==len(k)):
                        end=k[i+1]
                        break
                    else:
                       end=len(text)-1
                       break
            edu=tempor[beg:end]
            edu=edu.split()
            edu=' '.join(edu)
            if(edu):
                return edu
            for m in re.finditer('\nEXPERIENCE', temp):
                    if m and not(temp[m.end()].isalpha()):
                        inde=m.start()
                        for i in k:
                            if headings[i] in temp and i> m.end():
                                end=i
                                break
                        if end==99999:
                            end=len(temp)
                        edu=tempor[inde:end]
                        #print(edu)
                        edu=edu.replace("\n"," ")
                        if edu:
                            break
            if(inde):
                headings2[inde]="EXPERIENCE"
                headings2=OrderedDict(sorted(headings2.items()))
            if(edu):
                return edu
            for m in re.finditer('\n EXPERIENCE', temp):
                    if m and not(temp[m.end()].isalpha()):
                        for i in k:
                            inde=m.start()
                            if headings[i] in temp and (temp.index(headings[i]))> m.end():
                                end=i
                                break
                        if end==99999:
                            end=len(temp)
                        edu=tempor[inde:end]
                        edu=edu.replace("\n"," ")
                        if edu:
                            break
            if(inde):
                headings2[inde]="EXPERIENCE"
                headings2=OrderedDict(sorted(headings2.items()))
            if(edu):
                return edu
'''		
def find_companies(w):
            dat=pd.read_csv("/home/goscale/Downloads/companies.csv")
            text2=w
            text2=text2.replace('.','')
            text2=text2.replace('-','')
            text3=text2.lower()
            #for short forms
            col=list(dat.columns.values)
            col_list={}
            for i in col:
                if i.lower() in text2.lower():
                    ind=text3.index(i.lower())
                    if not(text3[ind-1].isalpha())and not(text3[ind+len(i.lower())].isalpha()):
                        #checking if inside word
                        col_list[text3.index(i.lower())]=i
            return col_list	
'''            
def find_companies(w):
            #print(w)
            conn = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='resumeParser')
            cur = conn.cursor()
            cur.execute("SELECT name FROM companies")
            result = cur.fetchall()
            col=[i[0] for i in result]
            conn.close()
            text2=w
            #text2=text2.replace('.','')
            #text2=text2.replace('-','')
            text3=text2.lower()
            col=[i.replace(",",'') for i in col]
            col=[i.replace("-",' ') for i in col]
            '''
            dat=pd.read_csv("/home/goscale/Downloads/companies.csv")
            col=list(dat.columns.values)
            '''
            col_list={}
            for i in col:
                for m in re.finditer(i.lower(), text3):
                    if not(text3[m.start()-1].isalpha())and not(text3[m.start()+len(i.lower())].isalpha()) and i.lower() != 'c':
                        #checking if inside word
                        col_list[m.start()]=i
            return col_list	
            
            
def get_degree(text):
            degrees={}
            fname="/home/goscale/Downloads/degrees.docx"
            #docs=Document(fname)
            tempo = fname
            tempo = docx2txt.process(fname)
            deg=[]
            word=""
            for i in tempo:
                if i!='\n':
                    word+=i
                else:
                    if(word):
                        word=word.replace('.','')
                        if word[0]==' ':
                            word=word[1:]
                        deg.append(word)
                    word=""
            deg.append('Twelfth')
            deg=[i.replace('\t','') for i in deg]
            text=text.replace('.','')
            text2=text.upper()
            for i in deg:
                for m in re.finditer(i.upper(), text2):
                     flag1=False
                     flag2=False
                     if m.start() ==0 or not(text[m.start()-1].isalnum()):
                         flag1=True
                     if m.end()==len(text) or not(text[m.end()].isalnum()):
                         flag2=True
                     if flag1 and flag2:
                             a=1
                             #print(i)
                             degrees=OrderedDict(sorted(degrees.items()))
                             for k in degrees.values():
                                 if i in k:
                                     #print(i)
                                     #print(degrees.values())
                                     if m.start()>text2.index(k.upper()) and m.start()<(text2.index(k.upper())+len(k)):
                                         #print(m.start())
                                         a=0
                                         break
                             if (m[0]=='ME'):
                                 if text2[m.start()-6:(m.start()-1)]=='ABOUT':
                                     a=0
                             if (m[0]=='SECONDARY' or m[0]=='SR SECONDARY'):
                                 if text2[m.end()+1:m.end()+7]=='SCHOOL':
                                     a=0
                             if(a):
                                 degrees[m.start()]=i
            degrees=dict((k, v) for k, v in degrees.items() if v)
            degrees=OrderedDict(sorted(degrees.items()))
            return degrees
def locations(w):
            place_string=""
            allPlace={}
            for i in Indian_states:
                for m in re.finditer(i, w):
                    allPlace[m.start()]=i
            p=""
            for i in w.split():
                p+=i+" "
                if i in short_month.values() or i=='Date':
                    continue
                else:
                    if i[0].isupper():
                        i=i.lower()
                        i=i[0].upper()+i[1:]
                        place=GeoText(i)
                        #print(i)
                        #print(place.cities)
                        #print(place.countries)
                        if not(len(place.cities)==0):
                            for c in place.cities:

                                allPlace[p.rfind(i)]=c
                        elif not(len(place.countries)==0):
                            for c in place.countries:

                                allPlace[p.rfind(i)]=c
            allPlace=OrderedDict(sorted(allPlace.items()))
            for j in allPlace.values():
                place_string+=j
            return allPlace		
def designation(w):
            finder=FinderAcora()
            jobTitles={}
            try:
             job=finder.findall(w)
             d=""
             for i in job:
                    jobTitles[i.start]=i.match

             for m in re.finditer('SDE', w):
                    count+=1
                    if count==8:
                        count=0
                    jobTitles[m.start()]='SDE'
             for m in re.finditer('freelancer', w.lower()):
                    count+=1
                    if count==8:
                        count=0
                    jobTitles[m.start()]='Freelancer'
            except:
                pass
            if not jobTitles:
                j=['developer','engineer','intern']
                for i in j:
                 for m in re.finditer(" "+i+" ", w.lower()):
                    jobTitles[m.start()]=i.capitalize()
                
            return jobTitles
def deg_with_year(degr,time_periods):
            degAndYear={}
            degr_key=list(degr.keys())
            degr_key.sort()
            if (time_periods) and degr_key:
                time_periods_key=list(time_periods.keys())
                time_periods_key.sort()
                if degr_key[0]<time_periods_key[0]:
                    #degrees come first then year
                    for i in range(0,len(degr_key)):
                        years=""
                        if i<(len(degr_key)-1):
                            min_deg_val=degr_key[i]
                            max_deg_val=degr_key[i+1]
                            for j in time_periods_key:
                                if j>min_deg_val and j<max_deg_val:
                                    #print(j)
                                    years+=time_periods[j]+" "
                            years=years[:-1]
                            degAndYear[degr[degr_key[i]]]=years
                        else:
                             for j in time_periods_key:
                                 if j>degr_key[i]:
                                   years+=time_periods[j]+" "
                             years=years[:-1]
                             degAndYear[degr[degr_key[i]]]=years
                if degr_key[0]>time_periods_key[0]:
                    #year comes first then degree
                    for i in range(0,len(degr_key)):
                            years=""
                            if i!=0:
                                max_deg_val=degr_key[i]
                                min_deg_val=degr_key[i-1]
                                for j in time_periods_key:
                                    if j>min_deg_val and j<max_deg_val:
                                        #print(j)
                                        years+=time_periods[j]+" "
                                years=years[:-1]
                                degAndYear[degr[degr_key[i]]]=years
                            else:
                                for j in time_periods_key:
                                 if j<degr_key[i]:
                                   years+=time_periods[j]+" "
                                years=years[:-1]
                                degAndYear[degr[degr_key[i]]]=years

            else:
                degr_val=list(degr.values())
                for d in degr_val:
                    degAndYear[d]='NA'
            return degAndYear	
def removeEnc(t):
            t=t.replace('\u200b','')
            t=t.replace('\xa0','')
            t=t.replace('\uf0d8','')
            t=t.replace('\uf0b7','')
            t=t.replace('\uf02a','')
            t=t.replace('\ufffd','')
            return t			
def monthYear(text):
            text2=text.split()
            for i in short_month.keys():
                for t in text2:
                    if i.lower()==t.lower():
                        #print(i)
                        text=text.replace(' '+t+' ',' '+short_month[i]+' ')
                        break
            #text=' '.join(text2)
            n = re.findall(re.compile(r'( \'[0-9][0-9])'), text)
            for t in n:
                t2=t.replace('\'',' 20')
                text=text.replace(t,t2)
            n = re.findall(re.compile(r'([0-9][0-9]-[0-9][0-9] )'), text)
            for t in n:
                t2=t.replace('-',' 20')
                text=text.replace(t,t2)
            return text	
            
def getWorkDetails(w,companies,desig,time_periods,text,headings):
 #in w: usually, we have comp_name : duration and designation. might or might not have projects. 
 #fetch 1st occurnace of all companies. from ind to next ind, fetch designation, dur, skills. if skills empty, look for those skills wrt those names under Projects heading.
 #print(w)
 
 #res: list of [company,[designation],time periods,{skill:skill_count}]
 #time_periods,w=time(w)
 print(w)
 tp_keys = list(time_periods.keys())
 tp_keys.sort()
 if companies:
  comp_keys = list(companies.keys())
  comp_keys.append(len(w))
  comp_keys.sort()
  desig_keys = list(desig.keys())
  desig_keys.append(len(w))
  desig_keys.sort()
  res = []
  if desig and min(desig_keys) < min(comp_keys):
   for k in desig_keys:
    if desig_keys.index(k) == len(desig_keys)-1:
     break   
    r=[]
    t = w[k:desig_keys[desig_keys.index(k)+1]]
    co=[]
    dur=""
    for c in comp_keys:
     if c > k and c < desig_keys[desig_keys.index(k)+1]:
      co.append(companies[c])
    r.append(co)
    r.append(desig[k])
    for tp in tp_keys:
     if tp > k and tp < desig_keys[desig_keys.index(k)+1]: 
       dur+=" "+time_periods[tp]
       if len(time_periods[tp])==4 and time_periods[tp].isdigit():
        dur+=" - "
    if dur:
     if dur[-2:]=="- ":
         dur=dur[:-2]
    r.append(dur)
    sk,sk_count=extract_skills(t)
    r.append(sk_count)
    res.append(r)
  else:
   for k in comp_keys:
    if comp_keys.index(k) == len(comp_keys)-1:
     break   
    r=[]
    t = w[k:comp_keys[comp_keys.index(k)+1]]
    co=[]
    r.append(companies[k])
    dur=""
    if desig:
     for c in desig_keys:
      if c > k and c < comp_keys[comp_keys.index(k)+1]:
       co.append(desig[c])
    r.append(co)
    for tp in tp_keys:
     if tp > k and tp < comp_keys[comp_keys.index(k)+1]: 
       dur+=" "+time_periods[tp]
       if len(time_periods[tp])==4 and time_periods[tp].isdigit():
        dur+=" - "
    if dur:
     if dur[-2:]=="- ":
         dur=dur[:-2]
    r.append(dur)
    sk,sk_count=extract_skills(t)
    r.append(sk_count)
    res.append(r)
  return res
     
 val = list(headings.values())
 key = list(headings.keys())
 if "PROJECTS" in val:
  v = val.index("PROJECTS")
  begin = key[v]
  end = key[v+1]
  workDetails = text[begin:end]
  companies=find_companies(w)
  if companies:
   comp_keys = list(companies.keys())
   comp_keys.append(len(workDetails))
   comp_keys.sort()
   for c in comp_keys:
    if comp_keys.index(c) == len(comp_keys)-1:
     break
    t = workDetails[c:comp_keys[comp_keys.index(c)+1]]
    sk,sk_count=extract_skills(t)


  #return workDetails
  
            
#############################START##################################	
global tempor
e=""
headings2={}
places={}
text=''

fpath='/home/goscale/resumes/Matej Cica-resumerd8i0C.pdf'

raw = parser.from_file(fpath)

text=raw['content']
text=removeEnc(text)
text=text.replace('('," ")
text=text.replace(')'," ")
text=re.sub(' +', ' ', text)
text = text.replace('\n ','\n')
text=text.replace('\t',' ')
text=text.replace(' Linkedin ',' LinkedIn ')	
propernoun=[]
spacy_extract={}
nltk_extract={}
spacy_string=""
#nlp = spacy.load('en')
text=text.replace('—'," ")
text=text.replace('–'," ")
text=text.replace('-'," ")
text=text.replace(','," ")
tempor=text
#print(tempor)
text=monthYear(text)
tempor=monthYear(tempor)
headings2=head(text)

#for repetition of important text in document
textf=''
text3=text.split()
textt=''
for i in text3:
    textt+=i+" "
    if i.upper() in headings2 and text.count(i)>1 and i[0].isupper() and textt[textt.rfind(i)].isupper():

	    ind=textt.rfind(i)

	    checksent=text[ind:ind+50]
	    if checksent in textt:
		    print(checksent)
		    textf=text[:ind]
		    break

if(textf):
   text=textf


places=locations(text)

e=extract_email(text)
e=removeEnc(e)
sk,sk_count=extract_skills(text)

namePdf=extract_name(text,e)
#namePdf=""
ph=extract_phoneNum(text)
print("Headingsssss")
print(headings2)

w=exp(text,headings2)
if(w):
 w=w.replace(',',' ')
 w=w.replace('–',' ')
 w=w.replace('—',' ')
 w=removeEnc(w)
 w=monthYear(w)
workDetails=""
if w:
 textr= "".join(text.rsplit(w))
 time_periods,textr=time(w)
 companies=find_companies(textr)
 print("companies")
 print(companies)
 col,prd=extract_companies_and_year(textr,time_periods)
 desig = designation(textr)
 workDetails = getWorkDetails(w,companies,desig,time_periods,text,headings2)
 print(workDetails)
else:
 companies=find_companies(text)
#print(text)
educat=education(text,headings2)
if (educat):
 educat2=educat.replace('.','')

 educat2=educat2.replace(' X ',' Tenth ')
 educat2=educat2.replace(' 10th ',' Tenth ')
 educat2=educat2.replace(' 10 ',' Tenth ')
 educat2=educat2.replace('Matriculation',' Tenth ')
 educat2=educat2.replace('Intermediate','Twelfth')
 educat2=educat2.replace('XII','Twelfth')
 educat2=educat2.replace('12th','Twelfth')
 educat2=educat2.replace(' 12 ','Twelfth')
 educat2=educat2.replace('\'',' \'')
 educat2=educat2.replace('|','')
 educat2=removeEnc(educat2)
 text=text.replace(educat,educat2)
 educat=educat2
 educat=monthYear(educat)
if not(educat):
 textr= "".join(text.rsplit(w))
 time_periods,textr=time(textr)
 col,prd=extract_college_and_year(textr,time_periods)
 degr=get_degree(textr)
else:
 educat=educat.replace('/',' ')
 time_periods,educat=time(educat)

 col,prd=extract_college_and_year(educat,time_periods)
 degr=get_degree(educat)
 print('in else')
 degr_val=list(degr.values())
 degr_key=list(degr.keys())
 degr_val=[i.lower() for i in degr_val]
 if 'tenth' in degr_val:
   if 'matriculation' in degr_val or 'secondary' in degr_val:
     i=degr_val.index('tenth')
     k=degr_key[i]
     del degr[k]
 if 'twelfth' in degr_val:
   if 'puc' in degr_val or 'higher secondary' in degr_val:
     i=degr_val.index('twelfth')
     k=degr_key[i]
     del degr[k]


if not(degr):
 textt=text.replace('.','')

 time_periods={}
 time_periods,textt=time(textt)
 degr=get_degree(textt)
 r = dict(time_periods)
 dk=list(degr.keys())
 deg_k=list(degr.keys())
 if deg_k:
     deg_first=deg_k[0]
     ind=min(time_periods, key=lambda x:abs(x-deg_first))
     time_p={}
     for k,v in time_periods.items():
      if k<ind:
       continue
      else:
         time_p[k]=v
      time_periods=time_p

deg_year=deg_with_year(degr,time_periods)


#multiple year values for each degree
for k,j in deg_year.items():
 t_y=[]
 l=j.split()
 for i in l:
  if i.isdigit() and len(i)==4:
    t_y.append(l.index(i))
 if len(t_y)>2:
  u=l[:(t_y[1]+1)]
  u=' '.join(u)
  deg_year[k]=u	
if not workDetails:
    workDetails=w
det=[namePdf,e,ph,deg_year,workDetails,col]
print('DETAILS')
for i in det:
 print(i)
