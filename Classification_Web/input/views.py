from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# from django.http import HttpResponseRedirect
from django.template import loader
import dill
from lime.lime_text import LimeTextExplainer
import pickle
from .forms import NameForm
import os
from django.conf import settings
from django.shortcuts import render_to_response
import re
from lime.lime_tabular import LimeTabularExplainer
from lime.lime_text import LimeTextExplainer

text_model=None
table_model=None
train_data=None

def query(request):
    str_list=[]
    initial='a'
    form=NameForm()
    context = {
        'str_list': str_list,
        'initial': initial,
        'form': form,
    }
    # return HttpResponse(template.render(context, request))
    # return render(request, 'input/query.html', context)
    return render(request, 'input/test/query.html', context)

def text(request):
    return render(request,'input/test/text.html')

def table(request):
    return render(request, 'input/test/table.html')

def exp_clean_save(exp,path,file):
    s=exp.as_html()
    s=re.sub(r'{{','',s)
    file= open(path+'/'+file+'.html','w', encoding='utf-8')
    file.write(s)
    file.close()

def classify_text(searchText):
    pipe=text_model.best_estimator_
    text_explainer=LimeTextExplainer(class_names=pipe.classes_,verbose=True)
    text_exp = text_explainer.explain_instance(searchText, pipe.predict_proba,
                                 num_features=10,top_labels=1)
    path='input/templates/input/test'
    filename='text'
    exp_clean_save(text_exp,path,filename)
    return filename

def classify_table(searchText):
    pipe=table_model.best_estimator_
    text_explainer=LimeTextExplainer(class_names=pipe.classes_,verbose=True)
    text_exp = text_explainer.explain_instance(searchText, pipe.predict_proba,
                                 num_features=10,top_labels=1)
    path='input/templates/input/test'
    filename='table'
    exp_clean_save(text_exp,path,filename)
    return filename


def classify(request):
    print('==============================classify is called')
    global text_model, table_model, train_data
    if not text_model:
        print('initializing sentiment text model')
        text_model=pickle.load(open('input/sentiment_text.model', 'rb'))
    if not table_model:
        print('initializing sentiment table model')
        table_model=pickle.load(open('input/sentiment_table.model', 'rb'))
    if not train_data:
        print('initializing sentiment training data')
        train_data=pickle.load(open('input/sentiment_train.data', 'rb'))

    searchText=request.GET['inputText']
    text_url=classify_text(searchText)
    table_url=classify_table(searchText)
    return JsonResponse({'text': text_url, 'table': table_url})

def index(request):
    return render(request, 'input/test/index.html')