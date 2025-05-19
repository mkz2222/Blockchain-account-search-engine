from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm, LoginForm

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User



from keyw.models import keyw, keyrank, creator_rank
from django.http import JsonResponse
import json

#SIGNUP


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()



def signup(request):

    if request.user.is_authenticated:
        return redirect('search')

    else:

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():

                #! Need to check if email already exist in database

                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Action required to activate your account at EOS TREE'
                message = render_to_string('signup/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message, from_email=None,)
                return redirect('account_activation_sent')

        else:
            form = SignUpForm()
        return render(request, 'signup/signup.html', {'form': form})




def account_activation_sent(request):
    return render(request, 'signup/email_sent.html',)






def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        # return redirect('search')
        return render(request, 'registration/activated.html')
    else:
        return render(request, 'signup/account_activation_invalid.html')




#always return to search page
def user_login(request):

    if request.user.is_authenticated:
        return redirect('search')

    else:

        form = LoginForm(request.POST or None)

        if request.POST:

            login_name = request.POST['username']
            login_pass = request.POST['password']

            user_exist = User.objects.filter(username=login_name).count()

            if user_exist == 1:

                userr = User.objects.get(username=login_name)

                #check if user is disabled
                if userr.profile.disabled:
                    if userr.check_password(login_pass):
                        return render(request, 'registration/disabled.html')
                    else:
                        context = {
                        'login_form' : form,
                        'error' : 'Invalid username or password.'
                        }

                        return render(request, 'registration/login.html', context)
                else:

                    #check if user is active
                    if not userr.is_active:

                        if userr.check_password(login_pass):
                            context = {
                            'user' : login_name,
                            }
                            return render(request, 'registration/inactive.html', context)
                        else:
                            context = {
                            'login_form' : form,
                            'error' : 'Invalid username or password.'
                            }

                            return render(request, 'registration/login.html', context)
                    else:

                        if form.is_valid():

                            user = form.login(request)
                            redirect_url = 'search'

                            if user is not None:

                                #get user ip
                                if 'HTTP_X_FORWARDED_FOR' in request.META:
                                    u_ip =  request.META['HTTP_X_FORWARDED_FOR']
                                else:
                                    u_ip = request.META['REMOTE_ADDR']

                                user.profile.last_ip = u_ip

                                login(request, user)
                                return redirect(redirect_url)

                            context = {
                            'login_form' : form,
                            }

                            return render(request, 'registration/login.html', context)
              

                        else:

                            context = {
                            'login_form' : form,
                            'error' : 'Invalid username or password.'
                            }

                            return render(request, 'registration/login.html', context)

            else:

                context = {
                'login_form' : form,
                'error' : 'Invalid username or password.'
                }

                return render(request, 'registration/login.html', context)


        return render(request, 'registration/login.html', {'login_form' : form})




#redirect to previous page using template signin.html
def user_signin(request):

    form = LoginForm(request.POST or None)

    if request.POST:
        #check if user is active
        login_name = request.POST['username']
        login_pass = request.POST['password']

        user_exist = User.objects.filter(username=login_name).count()
        if user_exist == 1:

            userr = User.objects.get(username=login_name)

            #check if user is disabled
            if userr.profile.disabled:
                if userr.check_password(login_pass):
                    return render(request, 'registration/disabled.html')
                    
            #check if user is activated
            if not userr.is_active:
                if userr.check_password(login_pass):
                    context = {
                    'user' : login_name,
                    }
                    return render(request, 'registration/inactive.html', context)
                else:
                    context = {
                    'login_form' : form,
                    'error' : 'Invalid username or password.'
                    }

                    return render(request, 'registration/login.html', context)
            else:

                if request.user.is_authenticated:
                    return redirect('search')

                else:

                    current_site = get_current_site(request)
                    login_page = 'http://' + current_site.domain + '/login/'
                    signin_page = 'http://' + current_site.domain + '/signin/'
                    signup_page = 'http://' + current_site.domain + '/signup/'
                    #http://142.93.58.28/reset_password/done/
                    login_pages = 'https://' + current_site.domain + '/login/'
                    signin_pages = 'https://' + current_site.domain + '/signin/'
                    signup_pages = 'https://' + current_site.domain + '/signup/'

                    banned_direct_list = [login_page, signup_page, signin_page, login_pages, signin_pages, signup_pages]

                    redirect_url = request.POST.get('next', 'search')

                    if form.is_valid():

                        user = form.login(request)
                        
                        if redirect_url in banned_direct_list:
                            redirect_url = 'search'

                        if user is not None:

                            #get user ip
                            if 'HTTP_X_FORWARDED_FOR' in request.META:
                                u_ip =  request.META['HTTP_X_FORWARDED_FOR']
                            else:
                                u_ip = request.META['REMOTE_ADDR']

                            user.profile.last_ip = u_ip

                            login(request, user)
                            return redirect(redirect_url)

                        context = {
                        'login_form' : form,
                        }

                        return render(request, 'registration/signin.html', context)

                    else:

                        context = {
                        'login_form' : form,
                        'error' : 'Invalid username or password.',
                        're_url' : redirect_url,
                        }

                        return render(request, 'registration/signin.html', context)
        else:

            context = {
            'login_form' : form,
            'error' : 'Invalid username or password.',
            }

            return render(request, 'registration/signin.html', context)



    return render(request, 'registration/signin.html', {'login_form' : form})






def user_logout(request):
    logout(request)
    return redirect('search')




def contact(request):

    return render(request, 'search/contact_form.html')



def agreement(request):

    return render(request, 'search/user_agreement.html')


def privacy(request):

    return render(request, 'search/user_privacy.html')


def advertise(request):

    return render(request, 'search/advertise.html')

def test(request):

    keyrank.objects.using('keyw').all()
    # keyq = keyrank.objects.order_by('id')[:10][::1]
    # keyvol = keyrank.objects.order_by('id').values_list('value', flat=True)
    # vol_list=list(keyvol)

    keyvol = keyrank.objects.order_by('-id').values('name', 'value')
    # js_data = json.dumps(keyvol)
    # creator_rank.objects.using('keyw').all()
    # creatorq = creator_rank.objects.order_by('id')[:10][::1]

    context = {
    'keyvol' : keyvol,
    }
    return render(request, 'search/test.html', context)