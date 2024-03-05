from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import UserCreationForm, LoginForm, SignupForm
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    database='prototype',
    user='anand',
    password='pass'
)

cursor = connection.cursor()

userID = 0

# Create your views here.
def home(request):
  return render(request,'home.html')

def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(request, username=username, password=password)
      if user:
        auth_login(request, user)
        getUserid = f"select UserID from users where username = '{username}'"
        result = cursor.execute(getUserid)
        userID = result[0][0] if result else None
        return redirect('modules')
  else:
    form = LoginForm()
  return render(request, 'login.html', {'form': form})

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
      # TODO: Insert the signup form details into database here
      username = form.cleaned_data.get('username')
      email = form.cleaned_data.get('email')
      password = form.cleaned_data.get('password2')
      add_user = f"INSERT INTO users (Username,Email,PasswordHash) values ('{username}','{email}','{password}')"
      cursor.execute(add_user)
      connection.commit()
      return redirect('login')
  else:
    form = SignupForm()
  return render(request, 'signup.html', {'form': form})

def logout(request):
  auth_logout(request)
  return redirect('login')

def modules(request):
  # get the {modID: moduleName, completedQuestions} from db
  return render(request, 'modules.html')

def question(request):
  return render(request, 'question.html')

def about(request):
  return render(request, 'about.html')

def help(request):
  return render(request, 'help.html')

def pricing(request):
  return render(request, 'pricing.html')