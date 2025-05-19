from django.shortcuts import render
from django.http import JsonResponse
import requests
from search.forms import SearchForm
# from search.models import Testdj, Testdj2
from search.models import Testdj
from django.shortcuts import get_object_or_404
from django.db.models import Q
from msg.models import Comments, Likes
import json
import datetime
from search.views import Pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


endpoints = ['https://api.eosnewyork.io', 
             'https://mainnet.eoscanada.com',
             'http://api-mainnet1.starteos.io',
             'http://mainnet.libertyblock.io:8888',
]


add_url = "/v1/chain/get_account"
add_url2 = "/v1/chain/get_code"
# add_url3 = "/v1/history/get_actions"
# add_url4 = "/v1/history/get_transaction"


acct_url = []
code_url =[]
group = {}

date1 = "1970"

for i in range(len(endpoints)):
    acct_url.append(endpoints[i] + add_url)
    code_url.append(endpoints[i] + add_url2)





def acct(request, acct_name):

	
	
	form = SearchForm()

	if acct_name:

		#get account info
		acct_json = {'account_name': acct_name}
		group.clear()
		try:
			response = requests.post(acct_url[0], json = acct_json)
			acct_result = response.json()

		except:
			try:
				response = requests.post(acct_url[1], json = acct_json)
				acct_result = response.json()

			except:
				try:
					response = requests.post(acct_url[2], json = acct_json)
					acct_result = response.json()

				except:
					context = {
					'err_info' : "account info error",
					'form' : form,
					}
					return render(request, 'acct/acct_err.html', context)




		if (request.GET.get('s')): 
			comment_sort = int(request.GET.get('s', 1))
		else:
			comment_sort = 1

		#s=1:newest, s=2:Best, s=3:Oldest


		#get comments:
		Comments.objects.using('msg').all()

		if comment_sort == 1:
			
			c1 = Comments.objects.filter(acct=acct_name).filter(post=True).filter(~Q(active = '0')).order_by('-date')

		elif comment_sort == 2:

			c1 = Comments.objects.filter(acct=acct_name).filter(post=True).filter(~Q(active = '0')).order_by('-up')

		elif comment_sort == 3:

			c1 = Comments.objects.filter(acct=acct_name).filter(post=True).filter(~Q(active = '0')).order_by('date')


		c_num = c1.count()

		#comments pagination:
		c1_p = Pages(c1, 10)
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


		#get likes if user is logged in:
		if request.user.is_authenticated:
		
			Likes.objects.using('msg').all()
			user_like = Likes.objects.filter(comment__acct=acct_name).filter(user_id=request.user.id).filter(like='1').values_list('comment_id', flat=True)
			user_dislike = Likes.objects.filter(comment__acct=acct_name).filter(user_id=request.user.id).filter(like='0').values_list('comment_id', flat=True)

		else: 
			user_like = []
			user_dislike = []

		#get accounts:
		Testdj.objects.using('gosql').all()
		# q1 = Testdj.objects.get(name=acct_name)
		q1 = get_object_or_404(Testdj, name=acct_name)
		acct_result2 = q1



		#check if voter/contract

		if acct_result['voter_info']:
			if acct_result['voter_info']['producers']:

				if q1.group2 != 'v':
					q1.group2 = 'v'
					q1.save()


		#Contract
		if acct_result['last_code_update'][0:4] > date1:
			#update group
			if q1.group5 != 'c':
				q1.group5 = 'c'
				q1.save()

			#get code info
			code_json = {'account_name': acct_name, 
						'code_as_wasm': 'true'
						}

			try:
				response = requests.post(code_url[1], json = code_json)
				code_result = response.json()

			except:
				try:
					response = requests.post(bacct_url[2], json = code_json)
					code_result = response.json()

				except:
					try:
						response = requests.post(bacct_url[0], json = code_json)
						code_result = response.json()

					except:
						context = {
						'err_info' : "account balance error",
						'form' : form,
						}
						return render(request, 'acct/acct_err.html', context)
		else:
			code_result = 0





		if q1.group1 == 'genesis':
			group['group1'] = 'genesis'
		elif q1.group1 == 'p':
			group['group1'] = 'premium'

		if q1.group2 == 'v':
			group['group2'] = 'voter'

		if q1.group3 == 'BP':
			group['group3'] = 'bp'

		if q1.group4 == 'f':
			group['group3'] = 'frozen'

		if q1.group5 == 'c':
			group['group5'] = 'contract'

		#NEW
		if q1.group6 == 's':
			group['group6'] = 'for sale'

		# except Testdj.DoesNotExist:
		# 	try:
		# 		Testdj2.objects.using('gosql').all()
		# 		q2 = get_object_or_404(Testdj2, name=acct_name)
		# 		acct_result2 = q2

		# 		if q2.group1 == 'genesis':
		# 			group['group1'] = 'genesis'
		# 		elif q2.group1 == 'p':
		# 			group['group1'] = 'premium'

		# 		if q2.group2 == 'v':
		# 			group['group2'] = 'voter'

		# 		if q2.group3 == 'bp':
		# 			group['group3'] = 'bp'

		# 		if q2.group4 == 'f':
		# 			group['group3'] = 'frozen'

		# 		if q2.group5 == 'c':
		# 			group['group5'] = 'contract'

		# 	except Testdj2.DoesNotExist:
		# 		context = {
		# 		'err_info' : "account name doesn't exist",
		# 		'form' : form,
		# 		}
		# 		return render(request, 'acct/acct_err.html', context)
			


		group_num = len(group)


		t_net = acct_result['net_limit']['max']
		t_cpu = acct_result['cpu_limit']['max']
		u_cpu = acct_result['cpu_limit']['used']
		t_ram = acct_result['ram_quota']
		u_ram = acct_result['ram_usage']

		ram_usage = round(float(u_ram) / 1024, 2)
		total_ram = round(float(t_ram) /1024, 2)
		cpu_usage = round(float(u_cpu) / 1000, 2)
		total_cpu = round(float(t_cpu) / 1000, 2)
		net_usage = round(acct_result['net_limit']['used'] / 1024, 2)
		total_net = round(int(t_net) / 1024, 2)
		staked_cpu = round(float(acct_result['cpu_weight']) / 10000, 4) 
		staked_net = round(float(acct_result['net_weight']) / 10000, 4) 




		if not acct_result.get('voter_info'):
			staked_total = 0
			staked_etc = 0
		else:
			staked_total = round(float(acct_result['voter_info']['staked']) / 10000, 4) 
			staked_etc = staked_total - staked_net - staked_cpu

		if 'core_liquid_balance' in acct_result: 
			balance = float(acct_result['core_liquid_balance'].replace('EOS', ''))
		else:
			balance = 0


		if not acct_result.get('refund_request'): 
			refund_cpu = 0 
			refund_net = 0 
		else:
			refund_cpu = round(float(acct_result['refund_request']['cpu_amount'].replace(' EOS', '')), 4)
			refund_net = round(float(acct_result['refund_request']['net_amount'].replace(' EOS', '')), 4)
			
		

		total_balance = balance + staked_total + refund_cpu + refund_net
		# total_balance = '{:,}'.format(total_balance)
		# total_balance = "{0:.4f}".format(total_balance)

		#created timee
		if 'created' in acct_result: 
			created_dt = datetime.datetime.strptime(acct_result['created'], '%Y-%m-%dT%H:%M:%S.%f')


		context = {
		'comment_sort' : comment_sort,
		'c1_result' : c1_result,
		'c2' : c2,
		'pagesc2' : pagesc2,
		'user_like' : user_like,
		'user_dislike' : user_dislike,
		'comments' : c1,
		'c_num' : c_num,
		'acct_result' : acct_result,
		'form' : form,
		'acct_result2' : acct_result2,
		'ram_usage' : ram_usage,
		'total_ram' : total_ram,
		'cpu_usage' : cpu_usage,
		'total_cpu' : total_cpu,
		'net_usage' : net_usage,
		'total_net' : total_net,
		'staked_cpu' : staked_cpu,
		'staked_net' : staked_net,
		'staked_etc' : staked_etc,
		'balance' : balance,
		'total_balance' : total_balance,
		'group' : group,
		'group_num' : group_num,
		'code_result' : code_result,
		'created_dt' : created_dt,
		}

		return render(request, 'acct/acct_result.html', context)




	else:
		context = {
		'err_info' : "account name not correct",
		'acct_name' : acct_name,
		'form' : form,
		}
		return render(request, 'acct/acct_err.html', context)



