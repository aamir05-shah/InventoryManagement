from django.shortcuts import render , redirect
from django.views.generic import TemplateView , View
from django.contrib.auth import authenticate , login
from .forms import UserRegisterForm 
# Create your views here.

class Index(TemplateView):
    template_name = 'dashboard/index.html'

class SignUpView(View):
    
    def get(self , request):    
    
        form = UserRegisterForm()
        return render(request, 'dashboard/signup.html', {'form': form})
    
    def post(self , request):
    
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )
            login(request,user)
            return redirect('index')
        
        return render(request, 'dashboard/signup.html', {'form': form})
    
    
    
class UC(View):
     
     def get(self, request):
         return render(request , 'dashboard/uc.html') 