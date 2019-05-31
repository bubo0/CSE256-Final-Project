from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import resolve
import dill
from lime.lime_text import LimeTextExplainer
import pickle
from .forms import NameForm
import re
from lime.lime_tabular import LimeTabularExplainer
from lime.lime_text import LimeTextExplainer
import numpy as np

model_loaded=False
data_loaded=False
model=None
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

def lime(request):
    current_url = resolve(request.path_info).url_name
    return render(request,'input/test/'+current_url+'.html')

def exp_clean_save(exp,path,file):
    s=exp.as_html()
    s=re.sub(r'{{','',s)
    file= open(path+'/'+file+'.html','w', encoding='utf-8')
    file.write(s)
    file.close()

def classify_text(searchText):
    pipe=model.best_estimator_
    explainer=LimeTextExplainer(class_names=pipe.classes_,verbose=False)
    exp = explainer.explain_instance(searchText, pipe.predict_proba,
                                 num_features=10,top_labels=1)
    path='input/templates/input/test'
    filename='text'
    exp_clean_save(exp,path,filename)
    return filename

def classify_table(searchText):
    vect=model.best_estimator_.named_steps.vect
    tfidf=model.best_estimator_.named_steps.tfidf
    clf=model.best_estimator_.named_steps.clf
    
    searchTextTrans=tfidf.transform(vect.transform([searchText])).toarray()[0]
    idx=np.argwhere(searchTextTrans!=0).flatten()
    searchTextTrans=searchTextTrans[idx]
    train=train_data[:,idx]
    features=[vect.get_feature_names()[i] for i in idx]
    explainer=LimeTabularExplainer(train,class_names=clf.classes_,feature_names=features,verbose=False)
    def predict_proba(X):
        w=clf.coef_[0][idx]
        po=np.dot(X,w)+clf.intercept_[0]
        p=1/(1+np.exp(po))
        ret=zip(p,1-p)
        return np.array(list(ret))
    exp=explainer.explain_instance(searchTextTrans,predict_proba,num_features=10, top_labels=1)
    path='input/templates/input/test'
    filename='table'
    exp_clean_save(exp,path,filename)
    return filename

def classify(request, classify_pk = 1):
    global model, train_data
    global model_loaded, data_loaded
    if not model_loaded:
        print('initializing sentiment text model')
        model=pickle.load(open('input/sentiment_text.model', 'rb'))
        model_loaded=True
    if not data_loaded:
        print('initializing sentiment training data')
        data=pickle.load(open('input/sentiment_train.data', 'rb'))
        vect=model.best_estimator_.named_steps.vect
        tfidf=model.best_estimator_.named_steps.tfidf
        train_data=tfidf.transform(vect.transform(data)).toarray()
        data_loaded=True

    searchText=request.GET['inputText']
    text_url=classify_text(searchText)
    table_url=classify_table(searchText)
    return JsonResponse({'text': text_url, 'table': table_url})

def index(request, index_pk = 1):
    if index_pk == 1:
        return render(request, 'input/test/index.html')
    else:
        return render(request, 'input/test/index2.html')