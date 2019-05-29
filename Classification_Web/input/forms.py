from django import forms

class NameForm(forms.Form):
    input_text = forms.CharField(label='Input text', max_length=300,
    widget=forms.TextInput(attrs={'style': 'width: 500px; height:30px; word-wrap:break-word; word-break:break-all'}))
