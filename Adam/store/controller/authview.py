from django.shortcuts import render,redirect
from django.contrib import messages
from store.forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import authenticate,login,logout,get_user_model

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import AuthenticationForm

from store.decorators import user_not_authenticated

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from store.tokens import account_activation_token
from django.db.models.query_utils import Q
@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "Submit the RECAPTCHA")
                    continue

                messages.error(request, error)
    form = UserRegistrationForm()

    return render(
        request=request,
        template_name="store/auth/register.html",
        context={"form": form}
    )

@user_not_authenticated
def loginpage(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],

            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b> {user.username} </b> ! You have been succesfully logged in ")
                return redirect("/")


        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "Submit the RECAPTCHA")
                    continue

                messages.error(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="store/auth/login.html",
        context={"form": form}
    )
@login_required
def logoutpage(request):
    logout(request)
    messages.info(request, "Logged Out Successfully")
    return redirect("/")

def profile(request, username):
    if request.method == "POST":
        user = request.user
        file_data = request.FILES or None
        form = UserUpdateForm(request.POST, file_data, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Your Profile has been updated!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)
            print(error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(
            request=request,
            template_name="store/auth/profile.html",
            context={"form": form}
        )

    return redirect('/')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account'
    message = render_to_string("store/auth/activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'

    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
        received activation link to confirm and complete the registration.<b>Note: </b> Check your spam folder.")

    else:
        messages.error(request, f"Problem sending email to {to_email}, check if you type it correctly.")

    return redirect('/')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login to your account")
        return redirect('/login')
    else:
        messages.error(request, "Activation link is invalid")

    return redirect('/')


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully")
            return redirect('loginpage')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'store/auth/password_reset_confirm.html', {'form': form})


@user_not_authenticated
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset"
                message = render_to_string("store/auth/reset_template.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                                    <h2>Password reset sent</h2><hr>
                                    <p>
                                        We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                                        You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                                        you registered with, and check your spam folder.
                                    </p>
                                    """
                                     )

                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('/')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request,
        template_name='store/auth/forgot_password.html',
        context={"form": form}
    )


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b> log in </b> now.")
                return redirect('/')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'store/auth/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect('/')

