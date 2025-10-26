from django.shortcuts import render

def home(request):
    #Step 1: If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "index.html")