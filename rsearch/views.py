from django.shortcuts import render, get_object_or_404
from .models import PersonalDetails, DegreeYear, UserSkillCount, Company, College,Degree
from itertools import chain
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
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
#import sqlite3
#from sqlite3 import Error
import django




from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize,sent_tokenize

# Create your views here.

def upload(request):
    if request.method == 'POST':
        uploaded_file=request.FILES['document']
        iszip=False
        fs=FileSystemStorage()
        fname=uploaded_file.name
        print(fname)
        if fname[-3:]=='zip':
            iszip=True
            with zipfile.ZipFile(uploaded_file,"r") as zip_ref:
                dir="C:\\Users\\Lenovo\\SearchResume\\media\\"+fname[:-4]
                os.mkdir(dir)
                zip_ref.extractall(dir)
        # text=uploaded_file.read()
        # print(text)
        # uploaded_file.read() to read contents\
        fs.save(uploaded_file.name, uploaded_file)
        stanford_classifier = 'C:\\Users\\Lenovo\\stanford-ner-2018-10-16\\classifiers\\english.all.3class.distsim.crf.ser.gz'
        stanford_ner_path = 'C:\\Users\\Lenovo\\stanford-ner-2018-10-16\\stanford-ner.jar'
        st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')

        #text = 'While in France, Resume Curriculum Vitae Sample Anand Kapoor Christine Lagarde Bharathi Gummanur discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'





        short_month={'Jan':'January','Feb':'February','Mar':'March','Apr':'April','May':'May','Jun':'June','Jul':'July','Aug':'August','Sep':'September','Sept':'September','Oct':'October','Nov':'November','Dec':'December'}

        pos_head=['CAREER OBJECTIVE','TECHNICAL SKILLS','ACADEMIC ACHIEVEMENTS','WORK EXPERIENCE','EXPERIENCE SUMMARY','PROJECT DETAILS','PROJECT EXPERIENCE','ADDITIONAL ACTIVITIES',
                  'PROFESSIONAL EXPERIENCE','ACADEMIC DISTINCTIONS','PROFESSIONAL SUMMARY', 'PROJECT PROFILE','TOOLS AND APPLICATIONS','ONLINE COURSES','TECHNICAL PROFICIENCY',
                  'CAREER SUMMARY','ADDITIONAL ENGAGEMENTS','ACADEMIC PROJECTS','ADDITIONAL ACTIVITIES'
                  'PUBLIC PROFILES','OTHER PROJECTS TRAININGS UNDERTAKEN','PROJECT DETAILS',
                  'FIELDS OF INTEREST','AREAS OF INTEREST','TECHNICAL EXPERIENCE','TECHNOLOGIES WORKED','LANGUAGES KNOWN',
                  'PROJECT WORK','PROFESSIONAL PROFILE','MINI PROJECTS','COMMUNICATION SKILLS','WORKING EXPERIENCE',
                  'EDUCATION','OVERALL','EDUCATIONAL','ACADEMIC','ACADEMIA',
                  'ABSTRACT','DECLARATION','EMPLOYMENT','PROJECTS','JOBS','JOB',
                 'CERTIFICATIONS','REFERENCE','LICENSES','CONFERENCES','TALKS','HONORS',
                  'AWARDS','INTERESTS','COURSES','HONORS','PUBLICATIONS','PUBLISHED','SCHOLARSHIPS','PERSONAL','OBJECTIVES',
                  'INTERNSHIPS','OBJECTIVE','REFERENCES',
                  'QUALITIES','LINKS','SOCIETIES','EXTRACURRICULAR','EXTRA-CURRICULAR',
                  'COMPETANCY','REFERENCE','ASPIRATION',
                  'APPENDIX','ACCOMPLISHMENTS','EXPERTISE','HOBBIES']
        Indian_states=["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]


        #took out project description and roles
        #nlp = spacy.load('en')

        ##doc files
        #
        #filename="C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\SharonJasmineSaldanha[8_0].docx"
        #docs=Document(filename)
        #tempor = filename
        #tempor = docx2txt.process(filename)
        #
        #
        #
        #text = [line.replace('\t', ' ') for line in tempor.split('\n') if line]
        #text= ' '.join(text)
        #
        #text.replace(":"," ")
        #text.replace("/"," ")
        #
        #

        #commom functions


        #to extract names
        def extract_name(resume,e):
            name=''
            sent=[]
            person=[]
            #text2=text.replace('\n',' ')
        #    t=''
        #    for i in text2.split():
        #        if i.isalpha():
        #            t+=" "+i
        #    tagged_sent = pos_tag(text.split())
        ## [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]
        #
        #    propernouns = [word for word,pos in tagged_sent if pos == 'NNP' and word!='Microsoft' and word!='Word' and word.isalpha() and word.lower()!='resume']
        #    print(propernouns)
        #
        #    plac=[]
        #    places2=list(places.values())
        #    for p in places2:
        #        plac.append(p.upper())
        #    if propernouns:
        #        if not(propernouns[0].upper() in plac) and propernouns[0] not in short_month.values():
        #
        #            name=propernouns[0]
        #            if propernouns[1]!='\n' and propernouns[1].isalpha():
        #                name+=" "+propernouns[1]
        #
        #        else:
        #            name=propernouns[1]
        #            if propernouns[2]!='\n' and propernouns[2].isalpha():
        #                name+=" "+propernouns[2]
        #    text2=t


            #resolve: somtimes people give emails at end of resume. in that acse, name is usually in the first few words

        #    t=text.split()
        #    if len(t)>3:
        #        for i in range(0,2):
        #                if t[i].isalpha() and t[i][0].isupper() and not(t[i].capitalize()=='Vitae') and not(t[i].lower() in sk):
        #                    classified_text = st.tag([t[i]])
        #                    if classified_text[0][1]=='PERSON':
        #                            print(t[i])
        #                            person.append(classified_text[0][0])
        #                            person.append(t[i+1])
        #                            break

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
                        for text2 in s:
                                if text2.isalpha() and text2[0].isupper() and not(text2=='Vitae') and not(text2.lower() in sk):
                                    #it's taking mysql and big data and shell scriptingand other skills as name. fix.


                                    print(text2)
                                    #tokenized_text = word_tokenize(text2)
                                    #person=[i[0] for i in text2.split() if st.tag(i)[0][1]=='PERSON']

                                    classified_text = st.tag([text2])



                                    if classified_text[0][1]=='PERSON':
                                            person.append(classified_text[0][0])
                                            person.append(s[s.index(text2)+1])
                                            break



                    #person.append(i[0] for i in classified_text if i[1]=='PERSON')


            if person:
                name=person[0]+' '+person[1]
            for i in name:
                if not(i.isalpha()):
                    name=name.replace(i,'')
            name=name.replace('docx','')
            name=name.replace('pdf','')

            return name




        #    Nouns_List = []
        #    text2=text.replace('.',' ')
        #    text2=text2.replace(',',' ')
        #    text2=text2.replace(':',' ')
        #    text2=text2.replace('/',' ')
        #    Words_List=text2.split()
        #    for Word in nltk.pos_tag(Words_List):
        #        if re.match('[NN.*]', Word[1]):
        #             Nouns_List.append(Word[0])
        #    from nltk.corpus import wordnet
        #
        #    Names = []
        #    for Nouns in Nouns_List:
        #        if not wordnet.synsets(Nouns) and Nouns!='Microsoft'and Nouns.isalpha() and Nouns[0].isupper():
        #            #Not an English word
        #            Names.append(Nouns)
        #        if Nouns=='Jain' or Nouns=='Das':
        #            Names.append(Nouns)
        #    if not(Names[0].capitalize() in places.values()):
        #        i=Nouns_List.index(Names[0])
        #        if Nouns_List[i+1].isalpha() and len(Nouns_List[i+1])==1 and (Nouns_List[i+1])[0].isupper():
        #            name=Names[0]+" "+Nouns_List[i+1]
        #        else:
        #            name=Names[0]+" "+Names[1]
        #    else:
        #        name=Names[1]+" "+Names[2]
        #    return name

            #extracting phone numbers using regular expressions
            # have multiple forms such as (+91) 1234567890 or +911234567890 or +91 123 456 7890 or +91 1234567890

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
        #extracting email using regular expressions again.
        #alphanumeric string should follow a @ symbol, again followed by a string, followed by a . (dot) and a string at the end

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
            '''if email:
                try:

                    e=email[0].split()[0].strip(';')
                    if ':' in e:
                        ind=e.rfind(':')
                        e=e[ind+1:]
                    nam=""
                    for i in e:
                        if i.isalpha() or i.isdigit() or i=='@':
                            nam=nam+i
                    cI=nam.index('com')
                    if(nam[cI-1]!='.'):
                        nam=nam[:cI]+'.'+nam[cI:]
                    return nam
                except IndexError:
                    return None'''





        def extract_skills(resume_text):
            resume_text=resume_text.replace('\n',' ')
            skill_count={}
            resume_text=re.sub(r"[^a-zA-Z0-9]+", ' ', resume_text)
            #removing stop words, using word tokenizing
            data=pd.read_csv("C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\skillsResume.csv")

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
                elif i.lower()==('present'):
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


        def extract_college_and_year(text,time_periods):

            dat=pd.read_csv("C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\colleges.csv")
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


        #extracting education:
        STOPWORDS = set(stopwords.words('english'))
        # Education Degrees
        def head(text):
            headings1={}
            t=text.upper()
            global tempor
            tempor=tempor.replace('\n ','\n')
            tempor2=tempor.upper()
        #    tempor3=tempor.replace(' ','')
        #    tempor2=tempor2.replace(' ','')
        #
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
            '''if 'PROJECT DESCRIPTION'  in t:
                 tempI=(tempor.upper().index('PROJECT DESCRIPTION'))
                 if tempor[tempI-1]=='\n':
                     if tempor[tempI+len('PROJECT DESCRIPTION')]=='\n' or tempor[tempI+len('PROJECT DESCRIPTION')+1]=='\n':
                         headings1[t.index('PROJECT DESCRIPTION')]='PROJECT DESCRIPTION'

            if 'TECHNICAL SKILLS'  in t:
                 tempI=(tempor.upper().index('TECHNICAL SKILLS'))
                 if tempor[tempI-1]=='\n':
                     if tempor[tempI+len('TECHNICAL SKILLS')]=='\n' or tempor[tempI+len('TECHNICAL SKILLS')+1]=='\n': #or condition cuz of spaces after the heading and then \n
                         headings1[t.index('TECHNICAL SKILLS')]='TECHNICAL SKILLS' '''

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
                if 'EMPLOYMENT'==j or 'WORK EXPERIENCE'==j or 'CAREER SUMMARY'==j or 'EXPERIENCE SUMMARY'==j or 'PROFESSIONAL PROFILE'==j or 'PROFESSIONAL EXPERIENCE'==j or 'ORGANIZATIONAL'==j or 'ORGANISATIONAL'==j or 'JOB'==j or 'JOBS'==j or 'WORKING EXPERIENCE'==j:
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

                            if headings[i] in temp and (temp.index(headings[i]))> m.end():

                                end=temp.index(headings[i])
                                break
                        if end==99999:
                            end=len(temp)
                        edu=tempor[inde:end]
                        edu=edu.replace("\n"," ")
                        break
        #    if(inde):
        #        expI=[]
        #        for m in re.finditer('EXPERIENCE', t):
        #            if m:
        #                expI.append(m.start())
        #        ind=min(expI, key=lambda x:abs(x-inde))
        #
        #        headings2[ind]="EXPERIENCE"
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

                                end=temp.index(headings[i])
                                break
                        if end==99999:
                            end=len(temp)
                        edu=tempor[inde:end]
                        edu=edu.replace("\n"," ")
                        break
        #    if(inde):
        #        expI=[]
        #        for m in re.finditer('EXPERIENCE', t):
        #            if m:
        #                expI.append(m.start())
        #        ind=min(expI, key=lambda x:abs(x-inde))
            if(inde):
                headings2[inde]="EXPERIENCE"
                headings2=OrderedDict(sorted(headings2.items()))
            if(edu):
                return edu
        #    if '\nEXPERIENCE' in temp :
        #        inde=temp.index('\nEXPERIENCE')
        #        temp.replace(":"," ")
        #        temp.replace("/" ," ")
        #        for i in k:
        #
        #            if headings[i] in temp and (temp.index(headings[i]))> inde+len('\nEXPERIENCE'):
        #                end=temp.index(headings[i])
        #                break
        #        edu=tempor[inde:end]
        #        edu=edu.replace("\n"," ")
        #        if(edu):
        #            return edu
            '''if '\nEXPERIENCE \n' in temp:
                inde=temp.index('\nEXPERIENCE \n')
                temp.replace(":"," ")
                temp.replace("/" ," ")
                for i in k:

                    if headings[i] in temp and (temp.index(headings[i]))> inde+len('\nEXPERIENCE \n'):
                        end=temp.index(headings[i])
                        break
                edu=tempor[inde:end]
                edu=edu.replace("\n"," ")
                return edu'''

        #    if '\n EXPERIENCE' in temp:
        #        inde=temp.index('\n EXPERIENCE')
        #        temp.replace(":"," ")
        #        temp.replace("/" ," ")
        #        for i in k:
        #
        #            if headings[i] in temp and (temp.index(headings[i]))> inde+len('\n EXPERIENCE'):
        #                end=temp.index(headings[i])
        #                break
        #        edu=tempor[inde:end]
        #        edu=edu.replace("\n"," ")
        #        if(edu):
        #            return edu
        #


        def find_companies(w):
            dat=pd.read_csv("C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\companies.csv")
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
            comp=list(col_list.values())
            return comp



        def get_degree(text):
        #degrees

            degrees={}

            fname="C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\degrees.docx"
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

            text=text.replace('.','')
            text2=text.upper()

            for i in deg:
                i=i.replace('\t','')
                for m in re.finditer(i.upper(), text2):
                     if not(text[m.start()-1].isalnum()) and not(text[m.end()].isalnum()):
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
            degrees=OrderedDict(sorted(degrees.items()))

            return degrees


        #locations
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


        #    designations
        def designation(w):
            finder=FinderAcora()
            job=finder.findall(w)
            jobTitles={}
            count=0
            d=""
            for i in job:
                u=i[2]
                ind=w.index(u)+len(u)
                if(w[ind]==" "):
                    #print(u)
                    d+=u+" "
                    count+=1
                    if count==8:
                            count=0
                    jobTitles[d.rfind(u)]=u

            for m in re.finditer('SDE', w):
                    count+=1
                    if count==8:
                        count=0
                    jobTitles[m.start()]='SDE'
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
                #    text=text.split()
                #    for i in range(0,len(text)):
                #        if text[i].isdigit():
                #
                #            if  int(text[i])>1950 and int(text[i])<=2019:
                #                if i!=len(text)-1:
                #                    if text[i+1].isdigit():
                #                        text[i]=text[i]+" to"
                #                    elif not(text[i+1]=='to' or text[i+1]=='To' or text[i+1]=='till' or text[i+1]=='Till' or text[i+1]=='until' or text[i+1]=='Until'):
                #                        text[i]=text[i]+' and'
                #                if i!=0:
                #                    if not(text[i-1]=='From' or text[i-1]=='from'):
                #                         text[i]="from "+text[i]
                #    text= ' '.join(text)
                #########pdf & doc

                # s=os.listdir("C:\\Resumes")
                #
                # for fol in s:
                #     fpath="C:\\Resumes\\"+fol
                #letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
                # s=os.listdir("C:\\TestResumes\\Profiles")
                # #let=0
                # c=0
                # for fol in s:
                #     c+=1
                #     if c>358:
                #         break
        def Parsing(fpath):
            global tempor
            e=""
            headings2={}
            places={}
            text=''

            # fpath='C:\\Users\\Lenovo\\SearchResume\\media\\'+uploaded_file.name

            raw = parser.from_file(fpath)

            text=raw['content']

            text=removeEnc(text)
            text=text.replace('('," ")
            text=text.replace(')'," ")
            text=text.replace('  ',' ')
            text=text.replace('\t',' ')
            text=text.replace(' Linkedin ',' LinkedIn ')

            #text=text.replace('�','ti')








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

            #text2=tempor.split()
            #for i in short_month.keys():
            #    if i in text2:
            #        tempor=tempor.replace(i,short_month[i])
            #    if i.upper() in text2:
            #        tempor=tempor.replace(i.upper(),short_month[i])
            #    if i.lower() in text2:
            #        #print(i)
            #        tempor=tempor.replace(i.lower(),short_month[i])
            #
            #tempor=tempor.replace('Junee','June')
            #
            #
            #for i in range(0,len(text2)):
            #    if text2[i].isdigit():
            #
            #        if  int(text2[i])>1950 and int(text2[i])<=2019:
            #            if i!=len(text2)-1:
            #                if text2[i+1].isdigit():
            #                    tempor=tempor.replace(text2[i],text2[i]+" to")
            #                elif not(text2[i+1]=='to' or text2[i+1]=='To' or text2[i+1]=='till' or text2[i+1]=='Till' or text2[i+1]=='until' or text2[i+1]=='Until'):
            #                    tempor=tempor.replace(text2[i],text2[i]+' and')
            #            if i!=0:
            #                if not(text2[i-1]=='From' or text2[i-1]=='from'):
            #                     tempor=tempor.replace(text2[i],"from "+text2[i])




            #OUTPUTS

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

            ph=extract_phoneNum(text)



            w=exp(text,headings2)
            if(w):
                w=w.replace(',',' ')
                w=w.replace('–',' ')
                w=w.replace('—',' ')
                w=removeEnc(w)
                w=monthYear(w)

            educat=education(text,headings2)
            if (educat):
                educat2=educat.replace('.','')

                educat2=educat2.replace(' X ',' Tenth ')
                educat2=educat2.replace(' 10th ',' Tenth ')
                educat2=educat2.replace(' 10 ',' Tenth ')
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



            if w:
                companies=find_companies(w)
            else:
                companies=find_companies(text)
            if not(degr):
                textt=text.replace('.','')

                time_periods={}
                time_periods,textt=time(textt)
                degr=get_degree(textt)
                r = dict(time_periods)
                dk=list(degr.keys())
            #    for k,v in time_periods.items():
            #        if abs(k-dk[0])>50:
            #            del r[k]
            #        else:
            #            break
                #time_periods=r
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
                #if len(list(deg_year.values()))==1:



                        l=j.split()

                        for i in l:
                            if i.isdigit() and len(i)==4:
                                t_y.append(l.index(i))
                        if len(t_y)>2:
                             u=l[:(t_y[1]+1)]
                             u=' '.join(u)
                             deg_year[k]=u
            # det=[namePdf,e,ph,deg_year,companies,col]
            # with open('C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\TestResumeDetails.csv', 'a') as csvFile:
            #     writer = csv.writer(csvFile)
            #     writer.writerow(det)
            # csvFile.close()

        #    xfile = openpyxl.load_workbook('C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\TestResumeDetails.xlsx')
        #
        #    sheet = xfile.get_sheet_by_name('Sheet1')
        #    l=letters[let]
        #
        #    for j in range(1,7):
        #        l+=str(j)
        #        sheet[l] = det[j-1]
        #        xfile.save('TestResumeDetails.xlsx')

            #desig=designation(w)



            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SearchResume.settings")
            django.setup()
            from rsearch.models import PersonalDetails,Skill,College,Company,DegreeYear, UserSkillCount, Degree

            try:
                p = PersonalDetails.objects.get(email=e)
                print("P exists")
            except:
                p = None

            if not(p):
                p = PersonalDetails.objects.create(phone=ph, name=namePdf, email=e)
                for c in col:
                    if not(c=='none'):
                        #print(c)
                        colObject = College.objects.get(collegeName=c)
                        print(colObject)
                        p.college.add(colObject)
                for c in companies:
                    if not(c=='none'):
                        #print(c)
                        compObject = Company.objects.get(companyName=c)
                        print(compObject)
                        p.company.add(compObject)
                p.save()

                sk_count_val=list(sk_count.values())
                if (sk_count_val):
                    for i in range(0,len(sk)):
                        skillObject = Skill.objects.get(skillName=sk[i])
                        userSkillCnt = UserSkillCount.objects.create(user=p, userSkill=skillObject, userSkillCount=int(sk_count_val[i]))
                        skillObject.save()



                deg_year=OrderedDict(sorted(deg_year.items()))
                deg_year_val=list(deg_year.values())
                deg_year_key=list(deg_year.keys())
                if deg_year_val and deg_year_key:
                    for i in deg_year_key:
                        degreeObject = Degree.objects.get(degreeName=i)
                        d=DegreeYear.objects.create(user=p, userDegree=degreeObject, userDegreeYear=deg_year[i])
                        d.save()
        # if iszip==False:
        #
        #                 fpath='C:\\Users\\Lenovo\\SearchResume\\media\\'+uploaded_file.name
        #
        #                 raw = parser.from_file(fpath)
        #
        #                 text=raw['content']
        #
        #                 text=removeEnc(text)
        #                 text=text.replace('('," ")
        #                 text=text.replace(')'," ")
        #                 text=text.replace('  ',' ')
        #                 text=text.replace('\t',' ')
        #                 text=text.replace(' Linkedin ',' LinkedIn ')
        #
        #                 #text=text.replace('�','ti')
        #
        #
        #
        #
        #
        #
        #
        #
        #                 propernoun=[]
        #                 spacy_extract={}
        #                 nltk_extract={}
        #                 spacy_string=""
        #
        #                 #nlp = spacy.load('en')
        #                 text=text.replace('—'," ")
        #                 text=text.replace('–'," ")
        #                 text=text.replace('-'," ")
        #                 text=text.replace(','," ")
        #
        #                 global tempor
        #                 tempor=text
        #                 #print(tempor)
        #
        #                 text=monthYear(text)
        #                 tempor=monthYear(tempor)
        #
        #                 #text2=tempor.split()
        #                 #for i in short_month.keys():
        #                 #    if i in text2:
        #                 #        tempor=tempor.replace(i,short_month[i])
        #                 #    if i.upper() in text2:
        #                 #        tempor=tempor.replace(i.upper(),short_month[i])
        #                 #    if i.lower() in text2:
        #                 #        #print(i)
        #                 #        tempor=tempor.replace(i.lower(),short_month[i])
        #                 #
        #                 #tempor=tempor.replace('Junee','June')
        #                 #
        #                 #
        #                 #for i in range(0,len(text2)):
        #                 #    if text2[i].isdigit():
        #                 #
        #                 #        if  int(text2[i])>1950 and int(text2[i])<=2019:
        #                 #            if i!=len(text2)-1:
        #                 #                if text2[i+1].isdigit():
        #                 #                    tempor=tempor.replace(text2[i],text2[i]+" to")
        #                 #                elif not(text2[i+1]=='to' or text2[i+1]=='To' or text2[i+1]=='till' or text2[i+1]=='Till' or text2[i+1]=='until' or text2[i+1]=='Until'):
        #                 #                    tempor=tempor.replace(text2[i],text2[i]+' and')
        #                 #            if i!=0:
        #                 #                if not(text2[i-1]=='From' or text2[i-1]=='from'):
        #                 #                     tempor=tempor.replace(text2[i],"from "+text2[i])
        #
        #
        #
        #
        #                 #OUTPUTS
        #
        #                 headings2=head(text)
        #                 #for repetition of important text in document
        #                 textf=''
        #                 text3=text.split()
        #                 textt=''
        #                 for i in text3:
        #                     textt+=i+" "
        #                     if i.upper() in headings2 and text.count(i)>1 and i[0].isupper() and textt[textt.rfind(i)].isupper():
        #
        #                         ind=textt.rfind(i)
        #
        #                         checksent=text[ind:ind+50]
        #                         if checksent in textt:
        #                             print(checksent)
        #                             textf=text[:ind]
        #                             break
        #
        #                 if(textf):
        #                     text=textf
        #
        #
        #                 places=locations(text)
        #
        #                 e=extract_email(text)
        #                 e=removeEnc(e)
        #                 sk,sk_count=extract_skills(text)
        #
        #                 namePdf=extract_name(text,e)
        #
        #                 ph=extract_phoneNum(text)
        #
        #
        #
        #                 w=exp(text,headings2)
        #                 if(w):
        #                     w=w.replace(',',' ')
        #                     w=w.replace('–',' ')
        #                     w=w.replace('—',' ')
        #                     w=removeEnc(w)
        #                     w=monthYear(w)
        #
        #                 educat=education(text,headings2)
        #                 if (educat):
        #                     educat2=educat.replace('.','')
        #
        #                     educat2=educat2.replace(' X ',' Tenth ')
        #                     educat2=educat2.replace(' 10th ',' Tenth ')
        #                     educat2=educat2.replace(' 10 ',' Tenth ')
        #                     educat2=educat2.replace('XII','Twelfth')
        #                     educat2=educat2.replace('12th','Twelfth')
        #                     educat2=educat2.replace(' 12 ','Twelfth')
        #                     educat2=educat2.replace('\'',' \'')
        #                     educat2=educat2.replace('|','')
        #                     educat2=removeEnc(educat2)
        #                     text=text.replace(educat,educat2)
        #                     educat=educat2
        #                     educat=monthYear(educat)
        #
        #                 if not(educat):
        #                     textr= "".join(text.rsplit(w))
        #                     time_periods,textr=time(textr)
        #                     col,prd=extract_college_and_year(textr,time_periods)
        #                     degr=get_degree(textr)
        #                 else:
        #                     educat=educat.replace('/',' ')
        #                     time_periods,educat=time(educat)
        #
        #                     col,prd=extract_college_and_year(educat,time_periods)
        #                     degr=get_degree(educat)
        #                     degr_val=list(degr.values())
        #                     degr_key=list(degr.keys())
        #                     degr_val=[i.lower() for i in degr_val]
        #                     if 'tenth' in degr_val:
        #                         if 'matriculation' in degr_val or 'secondary' in degr_val:
        #                             i=degr_val.index('tenth')
        #                             k=degr_key[i]
        #                             del degr[k]
        #                     if 'twelfth' in degr_val:
        #                         if 'puc' in degr_val or 'higher secondary' in degr_val:
        #                             i=degr_val.index('twelfth')
        #                             k=degr_key[i]
        #                             del degr[k]
        #
        #
        #
        #                 if w:
        #                     companies=find_companies(w)
        #                 else:
        #                     companies=find_companies(text)
        #                 if not(degr):
        #                     textt=text.replace('.','')
        #
        #                     time_periods={}
        #                     time_periods,textt=time(textt)
        #                     degr=get_degree(textt)
        #                     r = dict(time_periods)
        #                     dk=list(degr.keys())
        #                 #    for k,v in time_periods.items():
        #                 #        if abs(k-dk[0])>50:
        #                 #            del r[k]
        #                 #        else:
        #                 #            break
        #                     #time_periods=r
        #                     deg_k=list(degr.keys())
        #                     if deg_k:
        #                         deg_first=deg_k[0]
        #                         ind=min(time_periods, key=lambda x:abs(x-deg_first))
        #                         time_p={}
        #                         for k,v in time_periods.items():
        #                             if k<ind:
        #                                 continue
        #                             else:
        #                                 time_p[k]=v
        #                         time_periods=time_p
        #
        #                 deg_year=deg_with_year(degr,time_periods)
        #
        #
        #                 #multiple year values for each degree
        #                 for k,j in deg_year.items():
        #                             t_y=[]
        #                     #if len(list(deg_year.values()))==1:
        #
        #
        #
        #                             l=j.split()
        #
        #                             for i in l:
        #                                 if i.isdigit() and len(i)==4:
        #                                     t_y.append(l.index(i))
        #                             if len(t_y)>2:
        #                                  u=l[:(t_y[1]+1)]
        #                                  u=' '.join(u)
        #                                  deg_year[k]=u
        #                 # det=[namePdf,e,ph,deg_year,companies,col]
        #                 # with open('C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\TestResumeDetails.csv', 'a') as csvFile:
        #                 #     writer = csv.writer(csvFile)
        #                 #     writer.writerow(det)
        #                 # csvFile.close()
        #
        #             #    xfile = openpyxl.load_workbook('C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\TestResumeDetails.xlsx')
        #             #
        #             #    sheet = xfile.get_sheet_by_name('Sheet1')
        #             #    l=letters[let]
        #             #
        #             #    for j in range(1,7):
        #             #        l+=str(j)
        #             #        sheet[l] = det[j-1]
        #             #        xfile.save('TestResumeDetails.xlsx')
        #
        #                 #desig=designation(w)
        #
        #
        #
        #                 os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SearchResume.settings")
        #                 django.setup()
        #                 from rsearch.models import PersonalDetails,Skill,College,Company,DegreeYear, UserSkillCount, Degree
        #
        #                 try:
        #                     p = PersonalDetails.objects.get(email=e)
        #                     print("P exists")
        #                 except:
        #                     p = None
        #
        #                 if not(p):
        #                     p = PersonalDetails.objects.create(phone=ph, name=namePdf, email=e)
        #                     for c in col:
        #                         if not(c=='none'):
        #                             #print(c)
        #                             colObject = College.objects.get(collegeName=c)
        #                             print(colObject)
        #                             p.college.add(colObject)
        #                     for c in companies:
        #                         if not(c=='none'):
        #                             #print(c)
        #                             compObject = Company.objects.get(companyName=c)
        #                             print(compObject)
        #                             p.company.add(compObject)
        #                     p.save()
        #
        #                     sk_count_val=list(sk_count.values())
        #                     if (sk_count_val):
        #                         for i in range(0,len(sk)):
        #                             skillObject = Skill.objects.get(skillName=sk[i])
        #                             userSkillCnt = UserSkillCount.objects.create(user=p, userSkill=skillObject, userSkillCount=int(sk_count_val[i]))
        #                             skillObject.save()
        #
        #
        #
        #                     deg_year=OrderedDict(sorted(deg_year.items()))
        #                     deg_year_val=list(deg_year.values())
        #                     deg_year_key=list(deg_year.keys())
        #                     if deg_year_val and deg_year_key:
        #                         for i in deg_year_key:
        #                             degreeObject = Degree.objects.get(degreeName=i)
        #                             d=DegreeYear.objects.create(user=p, userDegree=degreeObject, userDegreeYear=deg_year[i])
        #                             d.save()
        if iszip==True:
            s=os.listdir('C:\\Users\\Lenovo\\SearchResume\\media\\'+fname[:-4])
            print(len(s))
            numfiles=len(s)
            count=0
            for fol in s:
                            count+=1
                            print(count)
                            if count==numfiles:
                                break

                            fpath='C:\\Users\\Lenovo\\SearchResume\\media\\'+fname[:-4]+'\\'+fol
                            # fpath='C:\\Users\\Lenovo\\SearchResume\\media\\'+uploaded_file.name

                            raw = parser.from_file(fpath)

                            text=raw['content']

                            text=removeEnc(text)
                            text=text.replace('('," ")
                            text=text.replace(')'," ")
                            text=text.replace('  ',' ')
                            text=text.replace('\t',' ')
                            text=text.replace(' Linkedin ',' LinkedIn ')

                            #text=text.replace('�','ti')








                            propernoun=[]
                            spacy_extract={}
                            nltk_extract={}
                            spacy_string=""

                            #nlp = spacy.load('en')
                            text=text.replace('—'," ")
                            text=text.replace('–'," ")
                            text=text.replace('-'," ")
                            text=text.replace(','," ")

                            global tempor
                            tempor=text
                            #print(tempor)

                            text=monthYear(text)
                            tempor=monthYear(tempor)

                            #text2=tempor.split()
                            #for i in short_month.keys():
                            #    if i in text2:
                            #        tempor=tempor.replace(i,short_month[i])
                            #    if i.upper() in text2:
                            #        tempor=tempor.replace(i.upper(),short_month[i])
                            #    if i.lower() in text2:
                            #        #print(i)
                            #        tempor=tempor.replace(i.lower(),short_month[i])
                            #
                            #tempor=tempor.replace('Junee','June')
                            #
                            #
                            #for i in range(0,len(text2)):
                            #    if text2[i].isdigit():
                            #
                            #        if  int(text2[i])>1950 and int(text2[i])<=2019:
                            #            if i!=len(text2)-1:
                            #                if text2[i+1].isdigit():
                            #                    tempor=tempor.replace(text2[i],text2[i]+" to")
                            #                elif not(text2[i+1]=='to' or text2[i+1]=='To' or text2[i+1]=='till' or text2[i+1]=='Till' or text2[i+1]=='until' or text2[i+1]=='Until'):
                            #                    tempor=tempor.replace(text2[i],text2[i]+' and')
                            #            if i!=0:
                            #                if not(text2[i-1]=='From' or text2[i-1]=='from'):
                            #                     tempor=tempor.replace(text2[i],"from "+text2[i])




                            #OUTPUTS

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

                            ph=extract_phoneNum(text)



                            w=exp(text,headings2)
                            if(w):
                                w=w.replace(',',' ')
                                w=w.replace('–',' ')
                                w=w.replace('—',' ')
                                w=removeEnc(w)
                                w=monthYear(w)

                            educat=education(text,headings2)
                            if (educat):
                                educat2=educat.replace('.','')

                                educat2=educat2.replace(' X ',' Tenth ')
                                educat2=educat2.replace(' 10th ',' Tenth ')
                                educat2=educat2.replace(' 10 ',' Tenth ')
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



                            if w:
                                companies=find_companies(w)
                            else:
                                companies=find_companies(text)
                            if not(degr):
                                textt=text.replace('.','')

                                time_periods={}
                                time_periods,textt=time(textt)
                                degr=get_degree(textt)
                                r = dict(time_periods)
                                dk=list(degr.keys())
                            #    for k,v in time_periods.items():
                            #        if abs(k-dk[0])>50:
                            #            del r[k]
                            #        else:
                            #            break
                                #time_periods=r
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
                                #if len(list(deg_year.values()))==1:



                                        l=j.split()

                                        for i in l:
                                            if i.isdigit() and len(i)==4:
                                                t_y.append(l.index(i))
                                        if len(t_y)>2:
                                             u=l[:(t_y[1]+1)]
                                             u=' '.join(u)
                                             deg_year[k]=u
                            # det=[namePdf,e,ph,deg_year,companies,col]
                            # with open('C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\TestResumeDetails.csv', 'a') as csvFile:
                            #     writer = csv.writer(csvFile)
                            #     writer.writerow(det)
                            # csvFile.close()

                        #    xfile = openpyxl.load_workbook('C:\\Users\\Lenovo\\.spyder-py3\\.spyder-py3\\TestResumeDetails.xlsx')
                        #
                        #    sheet = xfile.get_sheet_by_name('Sheet1')
                        #    l=letters[let]
                        #
                        #    for j in range(1,7):
                        #        l+=str(j)
                        #        sheet[l] = det[j-1]
                        #        xfile.save('TestResumeDetails.xlsx')

                            #desig=designation(w)



                            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SearchResume.settings")
                            django.setup()
                            from rsearch.models import PersonalDetails,Skill,College,Company,DegreeYear, UserSkillCount, Degree

                            try:
                                p = PersonalDetails.objects.get(email=e)
                                print("Updating new details")
                                PersonalDetails.objects.filter(email=e).delete()
                                p=None
                            except:
                                p = None

                            if not(p):
                                p = PersonalDetails.objects.create(phone=ph, name=namePdf, email=e)
                                for c in col:
                                    if not(c=='none'):
                                        #print(c)
                                        colObject = College.objects.get(collegeName=c)
                                        print(colObject)
                                        p.college.add(colObject)
                                for c in companies:
                                    if not(c=='none'):
                                        #print(c)
                                        compObject = Company.objects.get(companyName=c)
                                        print(compObject)
                                        p.company.add(compObject)
                                p.save()

                                sk_count_val=list(sk_count.values())
                                if (sk_count_val):
                                    for i in range(0,len(sk)):
                                        skillObject = Skill.objects.get(skillName=sk[i])
                                        userSkillCnt = UserSkillCount.objects.create(user=p, userSkill=skillObject, userSkillCount=int(sk_count_val[i]))
                                        skillObject.save()



                                deg_year=OrderedDict(sorted(deg_year.items()))
                                deg_year_val=list(deg_year.values())
                                deg_year_key=list(deg_year.keys())
                                if deg_year_val and deg_year_key:
                                    for i in deg_year_key:
                                        degreeObject = Degree.objects.get(degreeName=i)
                                        d=DegreeYear.objects.create(user=p, userDegree=degreeObject, userDegreeYear=deg_year[i])
                                        d.save()


    return render(request,'rsearch/uploaded.html')
#path('user_detail_search/<str:userName>/<str:phone>/<str:email>/<str:college>/<str:degree>/<str:grad_year>/<str:company>/', views.get_user_details, name='user_detail_search'),

def get_user_details(request, userName="NA",phone="NA",email="NA", college="NA",degree="NA",grad_year="NA", company="NA"):

    flag = False


    # Check if value available
    # if available


#initialize finalqueryset to empty query object
    finalQuerySet=PersonalDetails.objects.none()
    degreeObject=Degree.objects.filter(degreeName__iexact=degree)
    degreeObject=[c for c in degreeObject]
    # degreeYearObject=Degree.objects.filter(degreeName__icontains=degree)
    # degreeYearObject=[c for c in degreeYearObject]
    # gradYear = DegreeYear.objects.filter(userDegree=degreeObject[0])

    collegeObject = College.objects.filter(collegeName__iexact=college)
    collegeObject=[c for c in collegeObject]
    companyObject = Company.objects.filter(companyName__icontains=company)
    companyObject=[c for c in companyObject]
    userObject=PersonalDetails.objects.none()
    usereObject=PersonalDetails.objects.none()
    userpObject=PersonalDetails.objects.none()

    deg=DegreeYear.objects.none()





    if collegeObject:
        personalCollegeDetail = PersonalDetails.objects.filter(college=collegeObject[0])
        flag=True
    if(flag):
        finalQuerySet=personalCollegeDetail
    flag=False



    if companyObject:
        personalCompanyDetail = PersonalDetails.objects.filter(company=companyObject[0])
        flag=True
    if(flag):
        if(finalQuerySet):
            finalQuerySet=finalQuerySet.intersection(personalCompanyDetail)
        elif not(collegeObject):
            finalQuerySet=personalCompanyDetail
    flag=False

    if userName!="NA":
        userObject = PersonalDetails.objects.filter(name__icontains=userName)
        flag=True
    if(flag):
        if(finalQuerySet):
            finalQuerySet=finalQuerySet.intersection(userObject)
        elif not(collegeObject or companyObject):
            finalQuerySet=userObject
    flag=False
    if phone!="NA":
        userpObject = PersonalDetails.objects.filter(phone__icontains=phone)
        flag=True
    if(flag):
        if(finalQuerySet):
            finalQuerySet=finalQuerySet.intersection(userpObject)
        elif not(collegeObject or companyObject):
            finalQuerySet=userpObject
    flag=False
    if email!="NA":
        usereObject = PersonalDetails.objects.filter(email__icontains=email)
        flag=True
    if(flag):
        if(finalQuerySet):
            finalQuerySet=finalQuerySet.intersection(usereObject)
        elif not(collegeObject or companyObject):
            finalQuerySet=usereObject

    flag=False
    if grad_year!="NA":
        deg=DegreeYear.objects.filter(userDegreeYear__icontains=grad_year)
        flag=True

    if degreeObject:
        degYearDetail = DegreeYear.objects.filter(userDegree=degreeObject[0])
        flag=True

        if deg and degYearDetail:
            degYearDetail=degYearDetail.intersection(deg)
            flag=True




    elif deg:
        degYearDetail=deg
        flag=True
    if(flag):
        if(finalQuerySet):

            finalQueryEmails=[]
            degYearEmails=[]
            Emails=[]
            for i in range(0,len(finalQuerySet)):
                finalQueryEmails.append(finalQuerySet[i].email)
            for i in range(0,len(degYearDetail)):
                degYearEmails.append(degYearDetail[i].user.email)

            for i in finalQueryEmails:
                if i not in degYearEmails:
                    finalQueryEmails.remove(i)
            Emails=list(finalQueryEmails)
            # finalQueryEmails=finalQueryEmails.sort()
            # degYearEmails=degYearEmails.sort()
            # finalObject=PersonalDetails.objects.none()
            # for i in range(0,len(finalQuerySet)):
            #     if finalQuerySet[i].email in degYearEmails:
            #         p=PersonalDetails.objects.filter(email=finalQuerySet[i])
            #         finalObject=list(chain(finalObject,p))
            userList=[]
            for i in Emails:
                    uObject = PersonalDetails.objects.filter(email__iexact=i)
                    uObject=[u for u in uObject]
                    userList.append(uObject[0])


            finalQuerySet=DegreeYear.objects.filter(Q(user__in=userList) & Q(userDegree=degreeObject[0]))



        elif not(collegeObject or companyObject or userObject or usereObject or userpObject):
            finalQuerySet=degYearDetail





    if not(userObject or userpObject or usereObject or companyObject or collegeObject or degreeObject or deg):
        finalQuerySet = PersonalDetails.objects.all()

    context = {
        'finalQuerySet':finalQuerySet,
    }
    return render(request, 'rsearch/user_detail_search.html', context)


def justrender(request):
    context={'context':'context'}
    return render(request,'rsearch/user_detail.html')
