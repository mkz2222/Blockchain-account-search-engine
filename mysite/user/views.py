from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.utils import six

from django.db.models import Q

from ajax.views import email_change_token 
import datetime

from django.contrib.auth.forms import PasswordResetForm
from search.views import Pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from msg.models import Comments, Likes
from itertools import islice, chain
from operator import attrgetter


# def user_view(request, user_name):

# 	if request.user.is_authenticated:

# 		userr = User.objects.get(username=request.user)

# 		#get comments & replies:
# 		Comments.objects.using('msg').all()
# 		c1 = Comments.objects.filter(user_id=userr.id).filter(active='1')
# 		c1_num = c1.count()

# 		#get likes:
# 		Likes.objects.using('msg').all()
# 		like1 = Likes.objects.filter(user_id=userr.id).filter(~Q(like = '2'))

# 		#chain two queries
# 		sort_by = 'date'
# 		rev_order = False

# 		qc = sorted(
# 		    chain(c1, like1),
# 		    key=attrgetter(sort_by), reverse=rev_order)


# 		#comments pagination:
# 		c1_p = Pages(qc, 10)
# 		c1_result = c1_p.pages.count

# 		#Get page
# 		if (request.GET.get('page')): 
# 			page = request.GET.get('page', 1)
# 		else:
# 			page = 1

# 		try:
# 			c2 = c1_p.pages.page(page)
# 		except PageNotAnInteger:
# 			c2 = c1_p.pages.page(1)
# 		except EmptyPage:
# 			c2 = c1_p.pages.page(p.pages.num_pages)

# 		pagesc2 = c1_p.pages_to_show(int(page))


# 		context = {
# 		'c1_num' : c1_num,
# 		'c1_result' : c1_result,
# 		'c2' : c2,
# 		'pagesc2' : pagesc2,
# 		'user_name' : user_name, 
# 		'userr' : userr,
# 		'last_login' : request.user.last_login,
# 		}

# 		return render(request, 'user/setting.html', context)

# 	else:
# 		return redirect('search')




def update_email(request, uidb64, token):

	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
		new_email = user.profile.alt_email

	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	#EXPIRED
	if user.profile.alt_email == "":

		context = {
		'result': 'The activation link is expired.', 
		}

		return render(request, 'user/email_update.html', context)

	else:

		#Email already in use
		user_u = User.objects.filter(email = new_email).count()

		if user_u != 0:

			context = {
			'result': 'Sorry, this email address is already in use.', 
			}

			return render(request, 'user/email_update.html', context)

		#The email is not registered yet
		elif user_u == 0:
			#User is valid and token is correct - success
			if user is not None and email_change_token.check_token(user, token):

				user.email = new_email
				current_time = datetime.datetime.now()
				user.profile.email_chg_time = current_time
				user.profile.alt_email =""
				user.save()

				context = {
				'result': 'Your email has been updated!', 
				}

				return render(request, 'user/email_update.html', context)

			else:

				#Unknown error
				context = {
				'result': 'Sorry, an error occurred, please contact us if you need help.', 
				}

				return render(request, 'user/email_update.html', context)	




def forgot_password(request):

	if request.user.is_authenticated:
		return redirect('search')

	else:

		if request.method == "POST":

			form = PasswordResetForm(request.POST)

			context ={
			'form' : form,
			}

			return render(request, 'user/forgot_password.html', context)	

		else:

			form = PasswordResetForm()

			context ={
			'form' : form,
			}

			return render(request, 'user/forgot_password.html', context)	





def user_account(request):

	if request.user.is_authenticated:

		userr = User.objects.get(username=request.user)

		#get comments & replies:
		Comments.objects.using('msg').all()
		c1_num = Comments.objects.filter(user_id=userr.id).filter(active='1').count()

		context = {
		'c1_num' : c1_num,
		'userr' : userr,
		'last_login' : request.user.last_login,
		}

		return render(request, 'user/myaccount.html', context)

	else:
		return redirect('login')




def user_act(request):

	if request.user.is_authenticated:

		# userr = User.objects.get(username=request.user)

		#get comments & replies:
		Comments.objects.using('msg').all()
		c1 = Comments.objects.filter(user_id=request.user.id).filter(active='1')
		c1_num = c1.count()

		#get likes:
		Likes.objects.using('msg').all()
		like1 = Likes.objects.filter(user_id=request.user.id).filter(~Q(like = '2'))

		#chain two queries
		sort_by = 'date'
		rev_order = True

		qc = sorted(
		    chain(c1, like1),
		    key=attrgetter(sort_by), reverse=rev_order)


		#comments pagination:
		c1_p = Pages(qc, 10)
		c1_result = c1_p.pages.count

		#Get page
		if (request.GET.get('page')): 
			page = request.GET.get('page', 1)
		else:
			page = 1

		try:
			c2 = c1_p.pages.page(page)
		except PageNotAnInteger:
			c2 = c1_p.pages.page(1)
		except EmptyPage:
			c2 = c1_p.pages.page(p.pages.num_pages)

		pagesc2 = c1_p.pages_to_show(int(page))


		context = {
		'c1_num' : c1_num,
		'c1_result' : c1_result,
		'c2' : c2,
		'pagesc2' : pagesc2,
		}

		return render(request, 'user/myactivity.html', context)

	else:
		return redirect('login')





def user_setting(request):

	if request.user.is_authenticated:
		return render(request, 'user/mysetting.html')
	else:
		return redirect('login')