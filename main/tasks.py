from time import time

import requests
import json
import re
from bs4 import BeautifulSoup
import pymorphy2
import nltk
import numpy as np
import string
import matplotlib.pyplot as plt
import seaborn as sns;
from sklearn.cluster import AffinityPropagation
from celeryapp import app
sns.set()  # for plot styling
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from main.models import Course, Vacancy


stopwords = set(w.rstrip() for w in open('stopwords.txt', encoding='utf-8'))
snowball = SnowballStemmer(language="russian")
morph = pymorphy2.MorphAnalyzer()
punctuation = set(string.punctuation)
tfidf = TfidfVectorizer()

def lemmatize(text):
    words = text.split() # разбиваем текст на слова
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)
    return res

def tokenizer(s):
    s = s.lower()
    str = ''
    for i in s:
        if i not in punctuation:
            str+=i
    tokens = lemmatize(str)
    tokens = [t for t in tokens if t not in stopwords]
    tokens = [snowball.stem(t) for t in tokens]
    return ' '.join(tokens)

def correct_input(str):
    str.replace('&nbsp;', '')
    str.replace('[', '')
    str.replace(']', '')
    str.replace(',','')
    re.sub(r'\t', '', str)
    re.sub(r'\xa0', '', str)
    return str

def parse_netology():
    urls_netology = ['programs%2Ffullstack-python-dev', 'programs%2Fweb-developer',
                     'programs%2Fjava-developer', 'programs%2Ffront-end', 'programs%2Fqa', 'programs%2Fcpp-developer',
                     'programs%2Ffullstack-devops', 'programs%2Fqa-middle', 'programs%2Fsql-developer',
                     'programs%2Fautomation-engineer', 'programs%2Fandroid-app', 'programs%2Fios-developer',
                     'programs%2Fdeveloper1c', 'programs%2Fdeveloper1c_ultimate', 'programs%2Fbitrix',
                     'programs%2Fsysadmin', 'programs%2Fnetwork-engineer', 'programs%2Finformationsecurity',
                     'programs%2Funity-developer', 'programs%2Fsql-lessons']
    doc = []
    Course.objects.all().delete()
    for i in urls_netology:
        res = requests.get('https://netology.ru/backend/api/page_contents/'+i)
        res = json.loads(res.text)
        course = Course()
        course.title = res['meta']['title']
        course.url = 'https://netology.ru/programs/'+ res['program_family_url']
        course.site_name = 'Netology'
        res = res['content']
        s = ""
        for k, v in res.items():
            if re.match(r'resume', k):
                for t in v['skills']:
                    s+= re.sub(r'\<[^>]*\>', '', t) + ' '
            if re.match(r'programModule_', k):
                block = v['blocks']
                for t in block:
                    s+= re.sub(r'\<[^>]*\>', '', t['title'])
                    s+= ' '
                break
        if(s!='' and len(s.split(' '))>30):
            doc.append(correct_input(s))
            course.content = correct_input(s)
            course.save()
    return doc

def parse_skillbox():
    res = requests.get("https://skillbox.ru/api/v6/ru/sales/skillbox/directions/code/nomenclature/profession?page=1")
    doc = []
    while(res.status_code == 200):
        urls_skillbox = json.loads(res.text)
        for i in urls_skillbox['data']:
            course = Course()
            course.title = i['title'].replace('&nbsp;', ' ')
            course.url = i['href']
            course.site_name='Skillbox'
            res = requests.get(i['href'])
            soup = BeautifulSoup(res.text, "html.parser")
            strg = soup.findAll('li', class_= 'program-v3__subitem').__str__() + ' '
            strg += soup.findAll('li', class_='skills__item p p--2').__str__()
            desc = strg
            strg = re.sub(r'\<[^>]*\>', '', strg)
            if strg != "" and len(str.split(' '))>5:
                doc.append(strg)
                print(desc)
                course.content = correct_input(desc)
                course.save()
        if(urls_skillbox['links']['next'] is None):
            return doc
        res = requests.get(urls_skillbox['links']['next'])
    return doc
def parse_hhru():
    Vacancy.objects.all().delete()
    doc = []
    for pages in range(0, 10):
        res = requests.get("https://api.hh.ru/vacancies?specialization=1&page=" + pages.__str__())
        url_hhru = json.loads(res.text)
        for i in url_hhru['items']:
            vac = Vacancy()
            vac.url = i['alternate_url']
            vac.title = i['name']
            if(i['salary'] is not None):
                vac.salary = i['salary']['from']
            res = requests.get(i['url'])
            str = ""
            vacancy = json.loads(res.text)
            for v in vacancy['key_skills']:
                str+=v['name']+' '
            soup = BeautifulSoup(vacancy['description'], "html.parser")
            s = soup.find_all('ul',itemprop=None)
            for t in s:
                if(t != s[len(s)-1]):
                    str+=t.__str__()
                    str+=' '
            str = re.sub(r'\<[^>]*\>', '', str)
            if(len(str.split(" "))>30 and str is not None and str != " "):
                vac.content = str
                vac.save()
                doc.append(str)
    return doc

@app.task
def LSI_analize():
    t = time()
    doc_index = dict()
    doc1 = parse_netology()
    doc2 = parse_hhru()
    doc3 = parse_skillbox()
    corpus = doc1 + doc2 + doc3
    for i in corpus:
        i = tokenizer(i)
    svd = TruncatedSVD()
    norm = Normalizer(copy=False)
    lsa = make_pipeline(svd, norm)

    X = tfidf.fit_transform(corpus)
    X = lsa.fit_transform(X)
    """mass = []
    for i in range(0, len(doc1)):
        mass.append(X[i])
        print(X[i])
    centers = np.array(mass, np.float64)
    for iter in range(500, 1500, 10):
        for damp in np.arange(0.5, 1.0, 0.001):
            print('____________________________________________')
            km = AffinityPropagation(
                random_state=0,
                damping=damp,
                max_iter=iter
            )
            km.fit(X)
            if len(km.cluster_centers_) > 20 and len(km.cluster_centers_) < 60:
                print("max_iter: " + str(iter) + " damping: " + str(damp) + " clusters: " + str(len(km.cluster_centers_)))
    """
    t0 = time()
    km = KMeans(
        random_state=0,
        n_clusters= 22
    )
    km.fit(X)
    print("Затраченное время на алгоритм k-средних:", str(time()-t0))
    print("Количество документов в корпусе: ", str(len(X)))
    predictions = km.predict(X)
    plt.scatter(X[:, 0], X[:, 1], c=predictions, s=50, cmap='viridis')
    centers = km.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);
    #print('accuracy:', accuracy_score(y_test, predictions))
    #print(
    #    "Silhouette Coefficient: %0.3f"
    #    % metrics.silhouette_score(X_train, km.labels_, sample_size=1000)
    #)
    predictions = km.predict(X)
    for i in range(0, len(km.labels_)-1):
        if(i<len(doc1)):
            item = Course.objects.all()[i]
            item.cluster = km.labels_[i]
            item.save()
        else:
            if(i<len(doc1)+len(doc2)):
                index = i - len(doc1)
                item = Vacancy.objects.all()[index]
                item.cluster = km.labels_[i]
                item.save()
            else:
                index = i - len(doc2)
                item = Course.objects.all()[index]
                item.cluster = km.labels_[i]
                item.save()
    print("Затраченное время на выполнение всей программы: ", str(time() - t))
    plt.show()
LSI_analize()
