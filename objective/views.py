from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib import messages
from .form import * 

# Create your views here.
def create_objective(request):
        
    if request.method == 'GET':
        context = {'form': ObjectiveForm()}
        return render(request, 'objective/create_objective.html',context)
    
    elif request.method == "POST":
            form = ObjectiveForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success("Objective created!")

    else:
        messages.error("Please correct the following errors")
        return render(request, 'objective/create_objective.html')


