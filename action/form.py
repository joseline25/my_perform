from django import forms
from action.models import Question, Actions

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
        model = Actions
        fields = ['objective', 'questions_id', 'completion_time', 'collaborators_id', 'comment', 'added_by']