from django import forms
from action.models import Question, Action

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
            
            
            
# form for action
class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['action_name','objective', 'questions', 'completion_time', 'collaborators', 'comment', 'skills', 'achievements', 'added_by']