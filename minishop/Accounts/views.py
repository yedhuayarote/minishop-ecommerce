from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
import uuid
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm

from .forms import PasswordResetRequestForm


# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():                    #if we register these if and elif is get false
                messages.info(request, "username is already exist")       #username is unique. Then here check the already existed data's

                return redirect("register")

            elif User.objects.filter(email=email).exists():
                messages.info(request, "email has already exist")
                return redirect("register")

            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print("useer created")
        else:
            messages.info(request, "password is not matching")
            return redirect('register')

        return redirect('/')                    #Redirect to home page

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            uid = str(uuid.uuid4())       #Generate a random UID
            request.session['uid'] = uid    #Add the UID to the session
            request.session['username'] = username    #Adding username to session
            return redirect('/')
        else:
            messages.info(request, 'Incorrect username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')

def forgot_password(request):
    if request.method == "POST":
        password_reset_form = PasswordResetRequestForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'gmail.com',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'yedhu01ayrt@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetRequestForm()
    return render(request=request, template_name="password_reset.html",
                  context={"password_reset_form": password_reset_form})


def password_reset_confirm(request, uidb64=None, token=None):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
    else:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user=user)
        else:
            return HttpResponse('Token is invalid')
    return render(request, 'password_reset_confirm.html', {'form': form})


def password_reset_done(request):
        return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64=None, token=None):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('password_reset_complete')
            else:
                form = SetPasswordForm(user)
        else:
            return HttpResponse('Password reset link is invalid!')

        return render(request, 'password_reset_confirm.html', {'form': form})

def password_reset_complete(request):
        return render(request, 'password_reset_complete.html')

        return render(request, 'forgotpassword.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')
