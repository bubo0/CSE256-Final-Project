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

def classify(request):
    print('==============================classify is called')
    searchText=request.GET['inputText']
    print('searching '+ searchText)
    modelfile='input/sentiment.model'
    grid_search=pickle.load(open(modelfile, 'rb'))
    text_file='input/text.explainer'
    text_explainer=dill.load(open(text_file, 'rb'))
    pipe=grid_search.best_estimator_
    text_exp = text_explainer.explain_instance(searchText, pipe.predict_proba,
                                 num_features=10,top_labels=1)
    #TODO
    #1 .Save the explainer output as a html
    #2. Correctly return a url mapping to the right html
    text_exp.save_to_file('result.html')
    return HttpResponse('query')

def index(request):
    return render(request, 'input/test/index.html')