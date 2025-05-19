from django.db import models
from search.models import Testdj


class Acct_info(models.Model):

    #link EOS Account
    acct = models.OneToOneField(Testdj, on_delete=models.DO_NOTHING)

    #acount name
    acct_name = models.CharField(max_length=20, null=False)

    #comments #
    comm_num = models.IntegerField(default=0)

    #additonal account info
    #sale price
    acct_info1 =  models.CharField(max_length=50, default=None, null=True)
    #vender1
    acct_info2 =  models.CharField(max_length=10, default=None, null=True)
    #vender2
    acct_info3 =  models.CharField(max_length=10, default=None, null=True)
    #vender3
    acct_info4 =  models.CharField(max_length=10, default=None, null=True)
    
    acct_info5 =  models.CharField(max_length=10, default=None, null=True)

    #Dapp?
    dapp = models.CharField(max_length=20, default=None, null=True)
    dapp_desc = models.TextField(blank=True, default='', null=True)
    dapp_name =  models.CharField(max_length=50, default='', null=True)
    dapp_url =  models.CharField(max_length=50, default='', null=True)



    class Meta:
        app_label = 'acct'
