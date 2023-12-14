from django.shortcuts import render
from django.views import View
from .models import Actions
from .form import ActionForm

# Create your views here.

class ActionView(View):
    def post(self, request):
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save()
            return True
        else:
            return False    
    