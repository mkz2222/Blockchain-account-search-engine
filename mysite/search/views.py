from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from itertools import chain
from operator import attrgetter
from itertools import islice, chain
from django.db.models import Q
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from .models import Testdj, Testdj2
from .models import Testdj
from .forms import SearchForm

from functools import reduce
import operator

import time
from keyw.models import keyw, keyrank, creator_rank, kw_ad
from django.http import JsonResponse
import json


class Pages:

    def __init__(self, objects, count):
        self.pages = Paginator(objects, count)

    def pages_to_show(self, page):
        # pages_wanted stores the pages we want to see, e.g.
        #  - first and second page always
        #  - two pages before selected page
        #  - the selected page
        #  - two pages after selected page
        #  - last two pages always
        #
        # Turning the pages into a set removes duplicates for edge
        # cases where the "context pages" (before and after the
        # selected) overlap with the "always show" pages.
        pages_wanted = set([1,
                            page-2, page-1,
                            page,
                            page+1, page+2,
                            self.pages.num_pages])

        # The intersection with the page_range trims off the invalid
        # pages outside the total number of pages we actually have.
        # Note that includes invalid negative and >page_range "context
        # pages" which we added above.
        pages_to_show = set(self.pages.page_range).intersection(pages_wanted)
        pages_to_show = sorted(pages_to_show)

        # skip_pages will keep a list of page numbers from
        # pages_to_show that should have a skip-marker inserted
        # after them.  For flexibility this is done by looking for
        # anywhere in the list that doesn't increment by 1 over the
        # last entry.
        skip_pages = [ x[1] for x in zip(pages_to_show[:-1],
                                         pages_to_show[1:])
                       if (x[1] - x[0] != 1) ]

        # Each page in skip_pages should be follwed by a skip-marker
        # sentinel (e.g. -1).
        for i in skip_pages:
            pages_to_show.insert(pages_to_show.index(i), -1)

        return pages_to_show






def hello(request):

	# form = SearchForm()
	group_p = {}
	group_b = {}

	if request.method == "GET":

		form = SearchForm(request.GET)

		if form.is_valid():

			#keyword
			keyword = form.cleaned_data['q']
			keyword = keyword.lower()

			#ip
			if 'HTTP_X_FORWARDED_FOR' in request.META:
			    v_ip =  request.META['HTTP_X_FORWARDED_FOR']
			else:
			    v_ip = request.META['REMOTE_ADDR']

			v_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

			# keyw.objects.using('keyw').all()
			keyw.objects.create(ip=v_ip, keyword=keyword, time = v_time)

			#get keyword AD
			try:
				ad_r = kw_ad.objects.get(keyword = keyword)
			except kw_ad.DoesNotExist:
				ad_r = None


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


			#group_mode: 1 = AND 2 = XND
			if (request.GET.get('m')): 
				mode1 = request.GET.get('m', 1)
			else:
				mode1 = 'm2'

			#group
			if (request.GET.get('g1')): 
				group_b['group1'] = 'genesis'

			if (request.GET.get('g2')): 
				group_b['group2'] = 'v'

			if (request.GET.get('g3')): 
				group_b['group3'] = 'BP'

			if (request.GET.get('g4')): 
				group_b['group4'] = 'f'

			if (request.GET.get('g5')): 
				group_b['group1'] = 'p'

			if (request.GET.get('g6')): 
				group_b['group5'] = 'c'

			if (request.GET.get('g7')): 
				group_b['group6'] = 's'


			if (request.GET.get('g1')): 
				group_p['g1'] = 'genesis'

			if (request.GET.get('g2')): 
				group_p['g2'] = 'v'

			if (request.GET.get('g3')): 
				group_p['g3'] = 'BP'

			if (request.GET.get('g4')): 
				group_p['g4'] = 'f'

			if (request.GET.get('g5')): 
				group_p['g5'] = 'p'

			if (request.GET.get('g6')): 
				group_p['g6'] = 'c'

			if (request.GET.get('g7')): 
				group_p['g7'] = 's'

			group_num = len(group_p)


			#sort
			if (request.GET.get('s')): 
				sort1 = request.GET.get('s', 1)
			else:
				sort1 = 'd2'


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

			if group_num != 0 and mode1 =='m1':

				q1 = q1.filter(reduce(operator.or_, 
                                (Q(**d) for d in [dict([i]) for i in group_b.items()])))

				# q2 = q2.filter(reduce(operator.or_, 
    #                             (Q(**d) for d in [dict([i]) for i in group_b.items()])))

			elif group_num != 0 and mode1 == 'm2':
				q1 = q1.filter(Q(**group_b))
				# q2 = q2.filter(Q(**group_b))





			#sort
			sort_by = 'time_created'
			rev_order = False

			if(sort1 == 'd2'):
				sort_by = 'time_created'
				rev_order = True

			elif(sort1 == 'n1'):
				sort_by = 'name'
				rev_order = False

			elif(sort1 == 'n2'):
				sort_by = 'name'
				rev_order = True

			if rev_order == True:
				q1 = q1.order_by('-'+sort_by)
			elif rev_order == False:
				q1 = q1.order_by(sort_by)

			# qc = sorted(
			#     chain(q1, q2),
			#     key=attrgetter(sort_by), reverse=rev_order)


			p = Pages(q1, 20)

			presult = p.pages.count

			try:
				p2 = p.pages.page(page)
			except PageNotAnInteger:
				p2 = p.pages.page(1)
			except EmptyPage:
				p2 = p.pages.page(p.pages.num_pages)


			pages2 = p.pages_to_show(int(page))

			context = {
			'ad_r' : ad_r,
			'p2' : p2,
			'presult' : presult,
			'keyword' : keyword,
			'pages2' : pages2,
			'sort1': sort1,
			'group_p' : group_p,
			'group_num' : group_num,
			'mode1' : mode1,
			's_range' : s_range,
			}

			return render(request, 'search/search_result.html', context)

		#form is not valid ie front page
		else:

			presult = 0 
			form = SearchForm()
			# form_s = SortForm()

			#Last recorded
			Testdj.objects.using('gosql').all()
			qlast = Testdj.objects.order_by('-id')[:10][::1]

			#Total number of records
			qmax1 = Testdj.objects.all().aggregate(Max('id'))
			# qmax2 = Testdj2.objects.all().aggregate(Max('id'))

			qmax = int(qmax1['id__max']) 

			qmax = '{:,}'.format(qmax)

			keyrank.objects.using('keyw').all()
			keyq = keyrank.objects.order_by('id')[:10][::1]
			keyvol = keyrank.objects.order_by('id').values_list('value', flat=True)
			vol_list=list(keyvol)

			# key_vol = keyrank.objects.order_by('-id').values('name', 'value')

			creator_rank.objects.using('keyw').all()
			creatorq = creator_rank.objects.order_by('id')[:10][::1]

			context = {
			'presult' : presult,
			'form' : form,
			'qlast': qlast,
			'qmax' : qmax,
			'keyq' : keyq,
			'key_vol' : vol_list,
			'creatorq' : creatorq,
			}

			return render(request, 'search/search_form.html', context)


		
		context = {
		'form' : form,
		}

		return render(request, 'search/search_form.html', context)



	else:

		context = {
		'form' : form,
		}

		return render(request, 'search/search_form.html', context)






