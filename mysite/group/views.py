from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from itertools import chain
from operator import attrgetter
from itertools import islice, chain
from django.db.models import Q
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from search.models import Testdj, Testdj2
from search.models import Testdj
# from search.forms import SearchForm

from functools import reduce
import operator

import time
from keyw.models import keyw, keyrank, creator_rank

from search.views import Pages
from django.http import Http404  





def group(request, group_name):


	group_q = {}

	#group
	if group_name == 'genesis': 
		group_q['group1'] = 'genesis'

	elif group_name == 'voter':  
		group_q['group2'] = 'v'

	elif group_name == 'bp': 
		group_q['group3'] = 'BP'

	elif group_name == 'frozen':  
		group_q['group4'] = 'f'

	elif group_name == 'premium': 
		group_q['group1'] = 'p'

	elif group_name == 'contract': 
		group_q['group5'] = 'c'

	elif group_name == 'forsale': 
		group_q['group6'] = 's'
	else:
		raise Http404  


	#search keyword
	if request.method == "GET":

		#keyword
		if (request.GET.get('q')): 
			keyword = request.GET.get('q', 1)
			keyword = keyword.lower()
		else:
			keyword = ''

		if keyword != '': 

			#ip
			if 'HTTP_X_FORWARDED_FOR' in request.META:
			    v_ip =  request.META['HTTP_X_FORWARDED_FOR']
			else:
			    v_ip = request.META['REMOTE_ADDR']

			v_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

			# keyw.objects.using('keyw').all()
			keyw.objects.create(ip=v_ip, keyword=keyword, time = v_time)


			#page
			if (request.GET.get('page')): 
				page = request.GET.get('page', 1)
			else:
				page = 1

			#range
			if (request.GET.get('sr')): 
				s_range = request.GET.get('sr', 1)
			else:
				s_range = '3'


			#sort
			if (request.GET.get('s')): 
				sort2 = request.GET.get('s', 1)
			else:
				sort2 = 'd2'


			#get query
			Testdj.objects.using('gosql').all()
			# Testdj2.objects.using('gosql').all()


			#filter range: 1=acct, 2=creator, 3=all
			if s_range == '1':

				q1 = Testdj.objects.filter(Q(name__icontains=keyword))
				# q2 = Testdj2.objects.filter(Q(name__icontains=keyword))

			elif s_range == '2':
				q1 = Testdj.objects.filter(Q(creator__icontains=keyword))
				# q2 = Testdj2.objects.filter(Q(creator__icontains=keyword))

			else:
				q1 = Testdj.objects.filter(Q(name__icontains=keyword) | 
					Q(creator__icontains=keyword))

				# q2 = Testdj2.objects.filter(Q(name__icontains=keyword) | 
				# 	Q(creator__icontains=keyword))


			#filter groups
			q1 = q1.filter(Q(**group_q))
			# q2 = q2.filter(Q(**group_q))


			#sort
			if(sort2 == 'd2'):
				sort_by = 'time_created'
				rev_order = True

			elif(sort2 == 'd1'):
				sort_by = 'time_created'
				rev_order = False

			elif(sort2 == 'n1'):
				sort_by = 'name'
				rev_order = False

			elif(sort2 == 'n2'):
				sort_by = 'name'
				rev_order = True


			if rev_order:
				q1 = q1.order_by('-' + sort_by)
			else:
				q1 = q1.order_by(sort_by)


			p3 = Pages(q1, 40)

			presult1 = p3.pages.count

			try:
				p4 = p3.pages.page(page)
			except PageNotAnInteger:
				p4 = p3.pages.page(1)
			except EmptyPage:
				p4 = p3.pages.page(p.pages.num_pages)


			pages3 = p3.pages_to_show(int(page))

			context = {
			'p4' : p4,
			'presult1' : presult1,
			'keyword' : keyword,
			'pages3' : pages3,
			'sort2': sort2,
			's_range' : s_range,
			'group_name' : group_name,
			}

			return render(request, 'group/group_result.html', context)

		else:
			#keyword  = blank

			#page
			if (request.GET.get('page')): 
				page = request.GET.get('page', 1)
			else:
				page = 1


			#sort
			if (request.GET.get('s')): 
				sort2 = request.GET.get('s', 1)
			else:
				sort2 = 'd2'


			#range
			if (request.GET.get('sr')): 
				s_range = request.GET.get('sr', 1)
			else:
				s_range = '3'

			#sort
			if(sort2 == 'd2'):
				sort_by = 'time_created'
				rev_order = True

			elif(sort2 == 'd1'):
				sort_by = 'time_created'
				rev_order = False

			elif(sort2 == 'n1'):
				sort_by = 'name'
				rev_order = False

			elif(sort2 == 'n2'):
				sort_by = 'name'
				rev_order = True


			#get query
			Testdj.objects.using('gosql').all()
			# Testdj2.objects.using('gosql').all()


			#filter groups
			q1 = Testdj.objects.filter(reduce(operator.or_, 
		                    (Q(**d) for d in [dict([i]) for i in group_q.items()])))

			# q2 = Testdj2.objects.filter(reduce(operator.or_, 
		 #                    (Q(**d) for d in [dict([i]) for i in group_q.items()])))



			if s_range == '1':

				q1 = q1.filter(Q(name__icontains=keyword))
				# q2 = q2.filter(Q(name__icontains=keyword))

			elif s_range == '2':
				q1 = q1.filter(Q(creator__icontains=keyword))
				# q2 = q2.filter(Q(creator__icontains=keyword))

			else:
				q1 = q1.filter(Q(name__icontains=keyword) | 
					Q(creator__icontains=keyword))

				# q2 = q2.filter(Q(name__icontains=keyword) | 
				# 	Q(creator__icontains=keyword))


			# qc1 = sorted(
			#     chain(q1, q2),
			#     key=attrgetter(sort_by), reverse=rev_order)

			if rev_order:
				q1 = q1.order_by('-'+sort_by)
			else:
				q1 = q1.order_by(sort_by)

			p3 = Pages(q1, 40)

			presult1 = p3.pages.count

			try:
				p4 = p3.pages.page(page)
			except PageNotAnInteger:
				p4 = p3.pages.page(1)
			except EmptyPage:
				p4 = p3.pages.page(p3.pages.num_pages)


			pages3 = p3.pages_to_show(int(page))

			context = {
			'p4' : p4,
			'presult1' : presult1,
			'pages3' : pages3,
			'sort2': sort2,
			's_range' : s_range,
			'group_name' : group_name,
			}

			return render(request, 'group/group_result.html', context)



	#form is not valid ie front page
	else:

		#page
		if (request.GET.get('page')): 
			page = request.GET.get('page', 1)
		else:
			page = 1


		#sort
		if (request.GET.get('s')): 
			sort2 = request.GET.get('s', 1)
		else:
			sort2 = 'd2'


		#sort


		if(sort2 == 'd2'):
			sort_by = 'time_created'
			rev_order = True

		elif(sort2 =='d1'):
			sort_by = 'time_created'
			rev_order = False

		elif(sort2 == 'n1'):
			sort_by = 'name'
			rev_order = False

		elif(sort2 == 'n2'):
			sort_by = 'name'
			rev_order = True


		#get query
		Testdj.objects.using('gosql').all()



		#filter groups
		q1 = Testdj.objects.filter(reduce(operator.or_, 
	                    (Q(**d) for d in [dict([i]) for i in group_q.items()])))



		if rev_order:
			q1 = q1.order_by(sort_by)
		else:
			q1 = q1.order_by('-'+sort_by)



		p3 = Pages(q1, 40)

		presult1 = p3.pages.count

		try:
			p4 = p3.pages.page(page)
		except PageNotAnInteger:
			p4 = p3.pages.page(1)
		except EmptyPage:
			p4 = p3.pages.page(p3.pages.num_pages)


		pages3 = p3.pages_to_show(int(page))

		context = {
		'p4' : p4,
		'presult1' : presult1,
		'pages3' : pages3,
		'sort2': sort2,
		's_range' : s_range,
		}

		return render(request, 'group/group_result.html', context)














