from django.shortcuts import render
from django.http import HttpResponse
# from django.http import HttpResponseRedirect
from django.template import loader

from .forms import NameForm

def query(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            
            
            '''

            insert nlp model and process the input_text here
                        
            
            '''

            output_text = "Text successfully submitted: " + input_text
            return HttpResponse(output_text)
    else:
        form = NameForm()
        
        str_list = ['Make America great again!', 'Build a wall, and make Mexico pay for it!']
        initial = ['You can enter a sentence now and see if it is likely spoken by Trump, for example:']
        # template = loader.get_template('input/query.html')
        context = {
            'str_list': str_list,
            'initial': initial,
            'form': form,
        }
        # return HttpResponse(template.render(context, request))
        return render(request, 'input/query.html', context)