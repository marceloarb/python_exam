from django.shortcuts import render, redirect
from .models import User,Quote
from django.contrib import messages
import bcrypt
from django.db.models import Count

def index(request):
    return render(request, "index.html")

def createUser(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            print("User's password entered was " + request.POST['password'])
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 
            user = User.objects.create(name=request.POST['name'],email=request.POST['email'], password=hashed_pw)
            print("User's password has been changed to " + user.password)
            
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_name = User.objects.filter(email=request.POST['email'])
        if users_with_name:
            user = users_with_name[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):#This is checking if password are equal to the creation password
                request.session['user_id'] = user.id #IMPORTANT!!! this is how we know this user id is logged in
                return redirect('/homepage')
            else:
                print("Password didn't match")
                messages.error(request, "Incorrect name or password")
        else:
            print("Name not found")
            messages.error(request, "Incorrect name or password")
    return redirect('/')

def delete_session(request):
    request.session.clear()
    return redirect('/')

def homepage(request):
    if 'user_id'  in request.session :
        context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'quotes' : Quote.objects.annotate(likes=Count('users_who_liked')).order_by('-likes')
        
    }
        return render(request, "homepage.html",context)
    else:
        return redirect('/')

def userProfile(request,id):
    if 'user_id' in request.session:
        quote_with_id = User.objects.filter(id=id)
        if quote_with_id:
            context = {
                'user':User.objects.get(id=id)
            }
        return render(request,'one_user.html', context)
    else:
        return redirect('/')

def createQuote(request):
    if request.method == "POST":
        errors = Quote.objects.basic_validator_quote(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            quote = Quote.objects.create(author=request.POST['author'],quote = request.POST['quote'],user=User.objects.get(id=request.session['user_id']))
    return redirect('/homepage')

def likeQuote(request, id):
    if request.method == 'POST':
        quote_with_id = Quote.objects.filter(id=id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            quote.users_who_liked.add(user) #or user.cats_voted_for.add(cat)
    return redirect('/homepage')

def delete_Quote(request,id):
    if request.method == 'POST':
        quote_with_id = Quote.objects.filter(id=id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            if quote.user == user:
                quote.delete()
    return redirect('/homepage')

def display_update(request,id):
    if 'user_id' in request.session:
        context = {
            'user':User.objects.get(id=request.session['user_id'])
        }
        return render(request,'edit_user.html', context)
    else:
        return redirect('/')

def edit_user(request,id):
    if request.method == 'POST':
        errors = User.objects.basic_validator_update(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/display_update/' + str(id))
        else:
            
            User.objects.filter(id=id).update(
                name = request.POST['name'],
                email = request.POST['email'],
            )
            

            return redirect('/homepage')