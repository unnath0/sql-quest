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

        cursor.execute(getUserid)
        result = cursor.fetchall()

        request.session["userID"] = result[0][0] if result else None

        return redirect('modules')
  else:
    form = LoginForm()
  return render(request, 'login.html', {'form': form})

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()

      username = form.cleaned_data.get('username')
      email = form.cleaned_data.get('email')
      password = form.cleaned_data.get('password2')

      add_user = f"INSERT INTO users (Username,Email,PasswordHash) values ('{username}','{email}','{password}')"
      cursor.execute(add_user)

      return redirect('login')
  else:
    form = SignupForm()
  return render(request, 'signup.html', {'form': form})

def logout(request):
  auth_logout(request)
  return redirect('login')

def modules(request):
  userID = request.session.get('userID')

  # get the {modID: moduleName, completedQuestions, progressPercentage} from db
  getUserModuleProgress = f"select A.ModuleID,A.Description,B.CompletedQuestions,B.TotalQuestions,B.ProgressPercentage from modules A,usermoduleprogress B where A.ModuleID = B.ModuleID and UserID = {userID}"

  cursor.execute(getUserModuleProgress)
  result = cursor.fetchall()

  # Convert list of tuples to list of dictionaries
  columns = [col[0] for col in cursor.description]  # Get column names
  moduleDict = [dict(zip(columns, row)) for row in result]

  getUserTotalModuleProgress = f"select sum(CompletedQuestions) as complete,sum(TotalQuestions) as total,(sum(CompletedQuestions)/sum(TotalQuestions))*100 as progress from usermoduleprogress where UserID = {userID}"

  cursor.execute(getUserTotalModuleProgress)
  result = cursor.fetchall()

  # Convert list of tuples to list of dictionaries
  columns = [col[0] for col in cursor.description]  # Get column names
  modulesTotalProgress = dict(zip(columns,result[0])) if result else {}
  print(modulesTotalProgress)

  return render(request, 'modules.html', {'modulesData': moduleDict, 'allModulesProgress': modulesTotalProgress})

def question(request):
  userID = request.session.get('userID')

  # get the information necessary for sidebar
  getSideBarInfo = f"select A.ModuleID,A.Description,B.QuestionID from modules A, questions B where A.ModuleID = B.ModuleID"

  cursor.execute(getSideBarInfo)
  result = cursor.fetchall()

  # Convert list of tuples to list of dictionaries
  columns = [col[0] for col in cursor.description]  # Get column names
  sideBarInfoDict = [dict(zip(columns, row)) for row in result]

  # Initialize a dictionary to group by ModuleID and Description
  grouped_data = {}

  # Group the data by ModuleID and Description
  for item in sideBarInfoDict:
      key = (item['ModuleID'], item['Description'])
      if key not in grouped_data:
          grouped_data[key] = []
      grouped_data[key].append(item['QuestionID'])

  # Convert grouped data to the desired format
  sideBar = [{'ModuleID': key[0], 'Description': key[1], 'QuestionID': value} for key, value in grouped_data.items()]


  questionID = request.GET.get('questionID')

  if (questionID):
    # get the information of selected question
    getQuestionInfo = f"select A.Description,B.CompletedQuestions,B.TotalQuestions,B.ProgressPercentage,C.QuestionID,C.QuestionText from modules A, usermoduleprogress B, questions C where A.ModuleID = B.ModuleID and A.ModuleID = C.ModuleID and B.UserID = {userID} and C.QuestionId = {questionID}"
  else:
      # get the information of the first question if nothing is selected
    getQuestionInfo = f"select A.Description,B.CompletedQuestions,B.TotalQuestions,B.ProgressPercentage,C.QuestionID,C.QuestionText from modules A, usermoduleprogress B, questions C where A.ModuleID = B.ModuleID and A.ModuleID = C.ModuleID and B.UserID = {userID} and C.QuestionId = 1"

  cursor.execute(getQuestionInfo)
  result = cursor.fetchall()

  # Convert list of tuples to single dictionary
  columns = [col[0] for col in cursor.description]  # Get column names
  questionInfoDict = dict(zip(columns,result[0])) if result else {}

  return render(request, 'question.html', {'sideBarData': sideBar, 'questionInfo': questionInfoDict})

def about(request):
  return render(request, 'about.html')

def help(request):
  return render(request, 'help.html')

def pricing(request):
  return render(request, 'pricing.html')