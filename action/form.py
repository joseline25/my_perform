from django import forms
from action.models import Question

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
