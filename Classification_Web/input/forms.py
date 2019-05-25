from django import forms

class NameForm(forms.Form):
    input_text = forms.CharField(label='Input text', max_length=140)
