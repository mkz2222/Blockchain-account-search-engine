from django.shortcuts import render, redirect
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.http import JsonResponse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.utils import six
from signup.views import account_activation_token

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

import datetime
import time

from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

from signup.forms import SignUpForm
from signup.views import account_activation_token

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import update_session_auth_hash

from msg.models import Comments, Likes
from acct.models import Acct_info
from search.models import Testdj

import string


class Email_change_Token_Generator(PasswordResetTokenGenerator):


	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.profile.alt_email)
		)



email_change_token = Email_change_Token_Generator()



def change_email(request):

	data ={}

	if request.method == 'POST':

		new_email = []
		old_email=[]
		new_email.append(request.POST['new_email'])

		#Check if email already exists
		user_u = User.objects.filter(email = request.POST['new_email']).count()

		if user_u != 0:

			data = {
			'error': 'This email address is already in use.', 
			}

		elif user_u == 0:

			if request.user.is_authenticated:
				user_name = request.user.username
				old_email.append(request.user.email)
				user_pk = request.user.pk

				userr = User.objects.get(username=request.user)
				userr.profile.alt_email = new_email[0]
				userr.save()

				current_site = get_current_site(request)
				subject = 'Email change request'
				message = render_to_string('signup/account_change_email.html', {
				'user': user_name,
				'domain': current_site,
				'new_email' : new_email,
				'uid': urlsafe_base64_encode(force_bytes(user_pk)).decode(),
				'token': email_change_token.make_token(request.user),
				})

				subject2 = 'Email change notification'
				message2 = render_to_string('signup/change_email_notify.html', {
				'user': user_name,
				})

				try:
					#change email address
					send_mail(subject, message, '', new_email)
					send_mail(subject2, message2, '', old_email)
					data = {
					'chg': 1, 
					}

				except:
					data = {
					'error': 'An error occurred, please try again.', 
					}

			else:
				data = {
				'login': '0', 
				}

		return JsonResponse(data)






def change_password(request):

	if request.method == 'POST':

		if request.user.is_authenticated:

			password1 = request.POST['password1']
			password2 = request.POST['password2']
			pass_error =[]

			if password1 != password2:

				pass_error.append("New passwords didn't match.") 

			if len(password1) < 8:

				pass_error.append("New password must be at least 8 characters.") 

			
			if not request.user.check_password(request.POST['current_password']):

				pass_error.append("The current password is not correct.") 

			if len(pass_error) == 0:

				userr = User.objects.get(username=request.user)
				userr.set_password(password1)
				userr.save()
				update_session_auth_hash(request, userr)

				data = {
				'chg': 1, 
				}
			else:
				data = {
				'error': pass_error, 
				}	
					
		else:
			data = {
			'login': '0', 
			}

	return JsonResponse(data)






def check_username(request):

	data ={}
	user_error = ""
	user_name = request.GET.get('uname', None)

	if len(user_name) < 4:
		user_error = 'Invalid username.'

	for c in user_name:
		if c in string.punctuation:
			user_error = 'Invalid username.'

	if " " in user_name:
		user_error = 'Invalid username.'

	else:
		user_exist = User.objects.filter(username__iexact=user_name).exists()
		if user_exist:
			user_error= 'This username has been taken.'

	if len(user_error) == 0:

		data = {
		'pass': 1,
		}

	else:

		data = {
		'error': user_error,
		}

	return JsonResponse(data)




def check_email(request):

	data ={}
	email_error =[]
	user_email = request.GET.get('email', None)

	email_exist = User.objects.filter(email__iexact=user_email).exists()
	if email_exist:
		email_error.append('This email has been registered')

	if len(email_error) == 0:

		data = {
		'pass': 1,
		}

	else:
		data = {
		'error': email_error,
		}

	return JsonResponse(data)






def reset_pass(request):

	if request.method == 'POST':

		form = PasswordResetForm(request.POST)

		if form.is_valid():

			#email address
			from_email = ''

			opts = {
			'use_https': request.is_secure(),
			'token_generator': default_token_generator,
			'from_email': from_email,
			'request': request,
			}

			form.save(**opts)

			data = {
			'pass': 1,
			}

		else:
			data = {
			'pass': 1,
			}

	return JsonResponse(data)







def signup(request):

	data ={}
	signup_error =[]

	if request.method == 'POST':

		form = SignUpForm(request.POST)

		if form.is_valid():

			user_name = request.POST['username']
			user_email = request.POST['email']
			user_pass1 = request.POST['password1']
			user_pass2 = request.POST['password2']

			#check username
			if len(user_name) < 4:
				signup_error.append('Username is too short.')
			else:
				if " " in user_name:
					signup_error.append('Invalid username.')
				else:
					for c in user_name:
						if c in string.punctuation:
							signup_error.append('Invalid username.')

						else:
							user_exist = User.objects.filter(username__iexact=user_name).exists()
							if user_exist:
								signup_error.append('This username has been taken.')


			#check email
			email_exist = User.objects.filter(email__iexact=user_email).exists()
			if email_exist:
				signup_error.append('This email has been registered')

			#check password
			if user_pass1 != user_pass2:
				signup_error.append("The password doesn't match")
			else:
				if len(user_pass1) < 8:
					signup_error.append("The password must be at least 8 characters")

			#check form.error
			# for field in form:
			# 	if field.errors:
			# 		signup_error.append(field.errors)

			if len(signup_error) == 0:

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
				# return redirect('account_activation_sent')

				data = {
				'pass': 1,
				}

			else:

				data = {

				'error': signup_error,
				}

			return JsonResponse(data)


		for field in form:
			if field.errors:
				for error in field.errors:

					signup_error.append(error)

		data = {
		'error': signup_error,
		}
		return JsonResponse(data)



	return JsonResponse(data)








def like(request):

	if request.method == 'POST':

		post_id = request.POST['post_id']

		if request.user.is_authenticated:

			#check if user alraedy liked/disliked this comment
			user_like_status = Likes.objects.filter(user_id = request.user.id).filter(comment_id = post_id)
			user_like_num = user_like_status.count()

			#user not liked/disliked this yet / user liked but canceled before
			if user_like_num == 0 or user_like_status.values('like') == '2':

				#Check if original post exists
				post_num = Comments.objects.filter(id = post_id).count()

				if post_num == 1:

					original_p = Comments.objects.get(id=post_id)

					#update comment table
					if request.POST['like'] == '1':
						like_or_not = '1'
						original_p.up += 1

					elif request.POST['like'] == '0':
						like_or_not = '0'
						original_p.down += 1

					original_p.save() 

					like_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

					#write new record to likes table
					Likes.objects.create(comment=original_p, date=like_time, user_id = request.user.id, like=like_or_not)

					data = {
					'pass': 1,
					}

				#original post not exist, error
				else:
					data = {
					'error': 'An error has occurred', 
					}


			#user already liked/disliked/canceled
			elif user_like_num == 1:

				this_like = Likes.objects.get(user_id = request.user.id, comment_id = post_id)

				if request.POST['like'] == '1':
					#user click on like but dislike b4 ->change to 1
					if this_like.like == '0':
						try: 
							this_like.like = '1'
							this_like.save()

							original_p = Comments.objects.get(id=post_id)
							original_p.down -= 1
							original_p.up += 1
							original_p.save() 

							data = {
							'pass': 1,
							}
						except:
							data = {
							'error': 'An error has occurred', 
							}


					#user click on like and liked b4 -> cancel like
					elif this_like.like == '1':
						
						try: 
							this_like.like = '2'
							this_like.save()

							original_p = Comments.objects.get(id=post_id)
							original_p.up -= 1
							original_p.save() 

							data = {
							'pass': 1,
							}
						except:
							data = {
							'error': 'An error has occurred', 
							}


					#user canceled b4 -> change to like
					elif this_like.like == '2':
						
						try: 
							this_like.like = '1'
							this_like.save()

							original_p = Comments.objects.get(id=post_id)
							original_p.up += 1
							original_p.save() 

							data = {
							'pass': 1,
							}
						except:
							data = {
							'error': 'An error has occurred', 
							}


				elif request.POST['like'] == '0':

					#user click on dislike but liked b4
					if this_like.like == '1':
						try: 
							this_like.like = '0'
							this_like.save()

							original_p = Comments.objects.get(id=post_id)
							original_p.down += 1
							original_p.up -= 1
							original_p.save() 

							data = {
							'pass': 1,
							}
						except:
							data = {
							'error': 'An error has occurred', 
							}

					#user click on dislike and disliked b4 -> cancel dislike
					elif this_like.like == '0':

						try: 
							this_like.like = '2'
							this_like.save()

							original_p = Comments.objects.get(id=post_id)
							original_p.down -= 1
							original_p.save() 

							data = {
							'pass': 1,
							}
						except:
							data = {
							'error': 'An error has occurred', 
							}
						

					#user canceled b4 -> change to dislike
					elif this_like.like == '2':

						try: 
							this_like.like = '0'
							this_like.save()

							original_p = Comments.objects.get(id=post_id)
							original_p.down += 1
							original_p.save() 

							data = {
							'pass': 1,
							}
						except:
							data = {
							'error': 'An error has occurred', 
							}


				else:
					data = {
					'error': 'An error has occurred', 
					}

			else:
				data = {
				'error': 'An error has occurred', 
				}


		else:
			data = {
			'login': '0',
			}


	return JsonResponse(data)




def comment(request):

	if request.method == 'POST':

		comment_content = request.POST['comment']

		if comment_content.strip() == "":
			data = {
			'empty': '1',
			}
			return JsonResponse(data)
		else: 

			if request.user.is_authenticated:

				acct_name1 = request.POST['acct_name']
				c_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				userr = User.objects.get(username=request.user)

				#get testdj object
				this_acct = Testdj.objects.get(name=acct_name1)
				testnum = 1

				try:
					new_c = Comments.objects.create(acct=acct_name1, date=c_time, user = userr, content=comment_content)
					new_c.parent_id = new_c.id
					new_c.save()

					#add comment # to acct_info 11_9
					comm_acct = Acct_info.objects.filter(acct_id = this_acct.pk)
					comm_acct_num = comm_acct.count()

					if comm_acct_num == 1:

						this_acct.acct_info.comm_num += 1
						this_acct.acct_info.save()

					elif comm_acct_num == 0:

						testnum = 3
						new_acct_info = Acct_info.objects.create(acct=this_acct, acct_name=acct_name1)
						new_acct_info.comm_num += 1
						
						new_acct_info.save()

					data = {
					'pass': 1,
					}

				except:
					data = {
					'error': 'An error has occurred',
					}

				return JsonResponse(data)

			else:

				data = {
				'error': 'Please log in to leave a comment',
				}

				return JsonResponse(data)
	else:

		data = {
		'error': 'An error has ocurred',
		}

		return JsonResponse(data)






def reply(request):

	if request.user.is_authenticated:

		if request.method == 'POST':

			reply_content = request.POST['reply']

			if reply_content.strip() == "":

				data = {
				'empty': '1',
				}

			else: 

				post_id = request.POST['post_id']
				acct_name = request.POST['acct_name']
				c_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				userr = User.objects.get(username=request.user)

				#get testdj object
				this_acct = Testdj.objects.get(name=acct_name)

				try:
					Comments.objects.create(acct=acct_name, post=False, parent_id=post_id, user=userr, content=reply_content, date=c_time)

					#add comment # to acct_info 11_9
					this_acct.acct_info.comm_num += 1
					this_acct.acct_info.save()

					data = {
					'pass': 1,
					}

				except:
					data = {
					'error': 'An error has ocurred',
					}

		else:

			data = {
			'error': 'An error has ocurred',
			}

	else:
		data = {
		'login': '0',
		}


	return JsonResponse(data)






def delete(request):

	if request.method == 'POST':

		if request.user.is_authenticated:

			post_id = request.POST['post_id']
			acct_name = request.POST['acct_name']

			c_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			userr = User.objects.get(username=request.user)

			#get testdj object
			this_acct = Testdj.objects.get(name=acct_name)

			try:
				del_comment = Comments.objects.get(pk=post_id)
				del_childern = del_comment.children()
				child_count = del_childern.count()
				like_count = Likes.objects.filter(comment_id = post_id).count()

				if child_count == 0:

					del_comment.active = '0'
					del_comment.last_update = c_time
					del_comment.save()

					this_acct.acct_info.comm_num -= 1
					this_acct.acct_info.save()

				elif child_count != 0:
					del_comment.active = '2'
					del_comment.content = '<comment deleted by user>'
					del_comment.last_update = c_time
					del_comment.save()

					this_acct.acct_info.comm_num -= child_count
					this_acct.acct_info.save()

				if like_count != 0:
					Likes.objects.filter(comment_id = post_id).update(like = '2')

				data = {
				'pass': 1,
				}

			except:
				data = {
				'error': 'An error has ocurred',
				}

		else:
			data = {
			'login': '1',
			}

	else:

		data = {
		'error': 'An error has ocurred',
		}

	return JsonResponse(data)





def contact(request):

	data ={}

	if request.method == 'POST':

		if request.POST['type'] == 'ad':

			to_email = []

			#email address
			to_email.append('')

			sender_email = request.POST['sender_email']
			sender_name = request.POST['sender_name']
			subject = 'Advertise inquiry'
			content = request.POST['content']

			message = render_to_string('search/ad_inq_email.html', {
			'sender_name': sender_name,
			'sender_email': sender_email,
			'content': content,
			 })

			try:
				#email address
				send_mail(subject, message, '', to_email)

				data = {
				'chg': 1, 
				}

			except:
				data = {
				'error': 'An error occurred, please try again.', 
				}

		else:
			to_email = []

			#email address
			to_email.append('')
			
			sender_email = request.POST['sender_email']
			subject = request.POST['subject']
			content = request.POST['content']
			message = render_to_string('search/contact_email.html', {
			'sender_email': sender_email,
			'content': content,
			 })

			try:
				#email address
				send_mail(subject, message, '', to_email)

				data = {
				'chg': 1, 
				}

			except:
				data = {
				'error': 'An error occurred, please try again.', 
				}

	else:
		data = {
		'error': 'An error occurred, please try again.', 
		}

	return JsonResponse(data)






def resend_link(request):

	if request.user.is_authenticated:
		return redirect('search')
	else:
		if request.method == 'POST':

			login_name = request.POST['username']
			userr = User.objects.get(username=login_name)

			if not userr.is_active:

				current_site = get_current_site(request)
				subject = 'Action required to activate your account at EOS TREE'
				message = render_to_string('signup/account_activation_email.html', {
				'user': userr,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(userr.pk)).decode(),
				'token': account_activation_token.make_token(userr),
				})
				try: 
					userr.email_user(subject, message, from_email=None,)
					data = {
					'chg': '1', 
					}
				except:
					data = {
					'error': 'An error occurred, please try again.', 
					}
			else:
				data = {
				'error': 'An error occurred, please try again.', 
				}

		else:
			data = {
			'error': 'An error occurred, please try again.', 
			}

	return JsonResponse(data)