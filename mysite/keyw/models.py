from django.db import models

# Create your models here.

class keyw(models.Model):
    ip = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'keyw'


class keyrank(models.Model):

    name = models.CharField(max_length=20)
    value = models.IntegerField()
    log_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'keyw'


class creator_rank(models.Model):

    creator = models.CharField(max_length=20)
    vol = models.IntegerField()
    log_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'keyw'


class kw_ad(models.Model):

    keyword = models.CharField(unique=True, max_length=20)
    
    #0 = disabled 1=text 2=pic
    ad_type = models.CharField(max_length=10, null=False, default='1')
    #ad_content
    content = models.TextField(null=True, blank=False)
    #ad_url
    url = models.TextField(null=True, blank=False)
    #filename
    filename = models.CharField(max_length=30, null=True)
    filename_m = models.CharField(max_length=30, null=True)

    provider = models.CharField(max_length=30, null=True)

    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    log_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'keyw'