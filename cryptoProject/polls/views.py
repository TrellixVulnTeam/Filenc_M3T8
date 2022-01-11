from django.shortcuts import render, redirect
from .decorators import user_login_required
from .forms import RegisterForm, LoginForm
from .models import MyUser
from .ecdh import ecdh, aes_encrypt, aes_decrypt


# Create your views here.

def register(request):
    form = RegisterForm()
    key = ecdh()
    success = None
    if request.method == 'POST':
        if MyUser.objects.filter(username=request.POST['username']).exists():
            error = "This username is already taken"
            return render(request, 'polls/register.html', {'form': form, 'error': error})
        if MyUser.objects.filter(email=request.POST['email']).exists():
            error = "This email is already taken"
            return render(request, 'polls/register.html', {'form': form, 'error': error})
        password, iv = aes_encrypt(key, request.POST['password'])

        print(password)
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = password
            new_user.iv = iv
            new_user.key = key
            new_user.save()
            success = "New User Created Successfully !"
        else:
            print("not valid ")
    return render(request, 'polls/register.html', {'form': form, 'success': success})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password_form = request.POST['password']
        if MyUser.objects.filter(username=username).exists():
            user = MyUser.objects.get(username=username)
            password_db = user.password
            key_db = user.key
            iv_db = user.iv
            password_enc = aes_decrypt(key_db, password_form, iv_db)[0]
            print("password form: " + password_form)
            print("password DB: " + password_db)
            password_enc = password_db
            print("password encryption: "+password_enc)
            if password_db == password_enc:
                request.session[
                    'user_id'] = user.id  # This is a session variable and will remain existing as long as you don't delete this manually or clear your browser cache
                return redirect('home')
            else:
                error = "Password is not correct"
                return render(request, 'polls/login.html', {'form': form, 'error': error})
        else:
            error = "Username is not correct"
            return render(request, 'polls/login.html', {'form': form, 'error': error})
    return render(request, 'polls/login.html', {'form': form})


def get_user(request):
    return MyUser.objects.get(id=request.session['user_id'])


@user_login_required
def home(request):
    if 'user_id' in request.session:
        user = get_user(request)
        return render(request, 'polls/home.html', {'user': user})
    else:
        return redirect('login')

@user_login_required
def encrypt(request):
    if 'user_id' in request.session:
        user = get_user(request)
        return render(request, 'polls/encrypt.html', {'user': user })


@user_login_required
def decrypt(request):
    if 'user_id' in request.session:
        user = get_user(request)
        return render(request, 'polls/decrypt.html', {'user': user})


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # delete user session
    return redirect('login')
