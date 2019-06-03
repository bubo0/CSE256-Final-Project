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
import json
import shap

sen_model_loaded = False
sen_data_laoded = False
sen_model = None
sen_examples = None
sen_examples_loaded = False
trump_text_loaded = False
trump_text = None
trump_table_loaded = False
sen_train_data = None
trump_table = None
trump_examples = None
trump_examples_loaded = False


def lime(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'input/'+current_url+'.html')


def exp_clean_save(exp, path, file):
    s = exp.as_html()
    s = re.sub(r'{{', '', s)
    file = open(path+'/'+file+'.html', 'w', encoding='utf-8')
    file.write(s)
    file.close()


def classify_text(searchText, classify_pk):
    if classify_pk == 1:
        pipe = sen_model.best_estimator_
    else:
        pipe = trump_text['pipeline']
    explainer = LimeTextExplainer(class_names=pipe.classes_, verbose=False)
    exp = explainer.explain_instance(searchText, pipe.predict_proba,
                                     num_features=10, top_labels=1)

    path = 'input/templates/input'
    filename = 'text'
    exp_clean_save(exp, path, filename)
    return filename


def loadExamples(classify_pk):
    global trump_examples, sen_examples
    if classify_pk == 1:
        sen_examples = set()
        types = ['tp', 'tn', 'fp', 'fn']
        for t in types:
            for e in pickle.load(open("../Sentiment/" + t + ".pickple", "rb")):
                sen_examples.add(e[0])
        sen_examples_loaded = True
    else:
        trump_examples = set()
        for _, sentences in json.loads(open("../Trump/example_instances.json").read()).items():
            for sent, _ in sentences.items():
                trump_examples.add(sent)
        trump_examples_loaded = True


def classify_table(searchText, classify_pk):
    trump_result = ['-1']

    if classify_pk == 1:
        vect = sen_model.best_estimator_.named_steps.vect
        tfidf = sen_model.best_estimator_.named_steps.tfidf
        clf = sen_model.best_estimator_.named_steps.clf
        train_data = sen_train_data
        searchTextTrans = vect.transform([searchText])
        if tfidf.get_params()['use_idf']:
            searchTextTrans = tfidf.transform(searchTextTrans)

    else:
        clf = trump_table['cls']
        train_data = trump_table['trainX']
        vect = trump_table['vect']
        searchTextTrans = vect.transform([searchText])
        trump_result = clf.predict(searchTextTrans)

    searchTextTrans = searchTextTrans.toarray()[0]
    idx = np.argwhere(searchTextTrans != 0).flatten()
    searchTextTrans = searchTextTrans[idx]
    train = train_data[:, idx]
    weights = clf.coef_[0][idx]
    weights = np.round(weights, decimals=2)

    intercept = clf.intercept_[0]
    intercept = np.round(intercept, decimals=2)

    if classify_pk == 2:
        train = train.toarray()
    features = [vect.get_feature_names()[i] for i in idx]
    explainer = LimeTabularExplainer(
        train, class_names=clf.classes_, feature_names=features, verbose=False)

    def predict_proba(X):
        w = clf.coef_[0][idx]
        po = np.dot(X, w)+clf.intercept_[0]
        p = 1/(1+np.exp(po))
        ret = zip(p, 1-p)
        return np.array(list(ret))
    exp = explainer.explain_instance(
        searchTextTrans, predict_proba, num_features=10, top_labels=1)
    path = 'input/templates/input'
    filename = 'table'
    exp_clean_save(exp, path, filename)
    # return filename, features.tolist(), weights.tolist(), intercept
    return filename, {features[i]: weights[i] for i in range(len(weights))}, intercept, trump_result[0]


def classify_shap(searchText, classify_pk):
    if classify_pk == 1:
        vect = sen_model.best_estimator_.named_steps.vect
        tfidf = sen_model.best_estimator_.named_steps.tfidf
        clf = sen_model.best_estimator_.named_steps.clf
        train_data = sen_train_data
        searchTextTrans = vect.transform([searchText])
        if tfidf.get_params()['use_idf']:
            searchTextTrans = tfidf.transform(searchTextTrans)
    else:
        clf = trump_table['cls']
        train_data = trump_table['trainX']
        vect = trump_table['vect']
        searchTextTrans = vect.transform([searchText])
    searchTextTrans = searchTextTrans.toarray()[0]
    idx = np.argwhere(searchTextTrans != 0).flatten()
    explainer = shap.LinearExplainer(clf, train_data, feature_dependence="independent")
    shap_values = explainer.shap_values(searchTextTrans)
    shap_vals=np.round(shap_values[idx],decimals=2)
    X_test_mod=np.round(searchTextTrans[idx],decimals=2)
    features=[vect.get_feature_names()[i] for i in idx]
    out=shap.force_plot(explainer.expected_value, shap_vals, X_test_mod,feature_names=features)
    path = 'input/templates/input'
    filename = 'shap'
    shap.save_html(path+'/'+filename+'.html', out)
    # return filename, features.tolist(), weights.tolist(), intercept
    return filename

def classify(request, classify_pk=1):
    global sen_model, sen_train_data, trump_text, trump_table
    global sen_model_loaded, sen_data_laoded, trump_table_loaded, trump_text_loaded
    global sen_examples, trump_examples, sen_examples_loaded, trump_examples_loaded
    searchText = request.GET['inputText']
    if 'fromTable' in request.GET:
        searchText = searchText[:10]
        if classify_pk == 1:
            if not sen_examples_loaded:
                loadExamples(classify_pk)
            examples = sen_examples
        if classify_pk == 2:
            if not trump_examples_loaded:
                loadExamples(classify_pk)
            examples = trump_examples
        for example in examples:            
            if searchText in example:                
                searchText = example
                print(searchText)
                break
    if classify_pk == 1:
        if not sen_model_loaded:
            print('initializing sentiment text model')
            sen_model = pickle.load(open('input/sentiment_text.model', 'rb'))
            sen_model_loaded = True
        if not sen_data_laoded:
            print('initializing sentiment training data')
            data = pickle.load(open('input/sentiment_train.data', 'rb'))
            vect = sen_model.best_estimator_.named_steps.vect
            tfidf = sen_model.best_estimator_.named_steps.tfidf
            sen_train_data = tfidf.transform(vect.transform(data)).toarray()
            sen_data_laoded = True
    else:
        if not trump_text_loaded:
            print('initializing Trump text model')
            trump_text = pickle.load(open('input/trump_text.pickle', 'rb'))
            trump_text_loaded = True
        if not trump_table_loaded:
            print('initializing Trump trainning data')
            trump_table = pickle.load(open('input/trump_table.pickle', 'rb'))
            trump_table_loaded = True

    text_url = classify_text(searchText, classify_pk)
    table_url, table_weight, table_intercept, table_trump_result = classify_table(
        searchText, classify_pk)
    shap_url = classify_shap(searchText, classify_pk)
    table_weight['Feature'] = 'Weight'
    data = {'text': text_url, 'table': table_url, 'shap': shap_url, 'table_intercept': table_intercept, 'table_trump_result' : table_trump_result}
    data.update(table_weight)
    print(data)
    return JsonResponse(data)


def index(request, index_pk=1):
    template = str(request.build_absolute_uri('?')).split('/')[-1]
    if template.endswith('html'):
        return render(request, 'input/' + template)
    if index_pk == 1:
        return render(request, 'input/index.html')
    else:
        return render(request, 'input/index2.html')
