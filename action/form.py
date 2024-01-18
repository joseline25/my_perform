from django import forms
from action.models import Question
from .models import Action

# validators
# when number has a value answer is null, when answer has a value number is null
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'number', 'answer']
    def clean_question(self):
        number = self.cleaned_data['number']
        answer = self.cleaned_data['answer']
        if number:
            answer = None
        elif answer:
            number = None
            
            
            
# action

class ActionForm(forms.ModelForm):
    
    class Meta:
        model = Action
        fields = ['action_name', 'completion_time', 'objective', 'collaborators', 'tools' ]
        widgets = {
            'action_name': forms.TextInput(attrs={'placeholder': 'E.g I researched on ...'}),
            'completion_time': forms.NumberInput(attrs={'placeholder': 'Enter an Integer'}),
            'objective': forms.Select(attrs={}),
            'collaborators': forms.CheckboxSelectMultiple(attrs={}),
            'tools': forms.CheckboxSelectMultiple(attrs={}),
            # 'objective': forms.Select(attrs={'class': 'form-control'}),
        }
        
            
