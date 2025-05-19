from django.db import models
from django.contrib.auth.models import User


class Comments(models.Model):
    #EOS Account
    acct = models.CharField(max_length=20, null=False)

    #1=post 0=reply
    post = models.BooleanField(default=True) 

    #'1' = active, '0'=deleted/hidden
    active = models.CharField(max_length=10, null=False, default='1')

    #original post id if it is a reply
    parent_id = models.CharField(max_length=50, blank=True)

    date = models.DateTimeField(null=False)
    last_update = models.DateTimeField(null=True)

    #comment/reply writer
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    #Maxlength?
    content = models.TextField(null=False, blank=False)

    #up/down vote
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)

    #number of replies
    reply_num = models.IntegerField(default=0)


    def children(self):
        return Comments.objects.filter(parent_id=self.id).filter(post=False).filter(active='1')

    class Meta:
        app_label = 'msg'





class Likes(models.Model):

    #which comment this like/dislike is about
    # comment_id = models.CharField(max_length=250, null=False)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)

    #1=like 0=dislike 2=canceled
    like = models.CharField(max_length=10, null=False, default='1')

    #post user
    user_id = models.CharField(max_length=250, null=False)

    #post date
    date = models.DateTimeField(null=False)


    class Meta:
        app_label = 'msg'




# class Reply(models.Model):

#     #comment
#     comment = models.ForeignKey(Comments, on_delete=models.CASCADE)

#     #reply content
#     content = models.TextField(null=False, blank=False)

#     #post user
#     user_id = models.CharField(max_length=250, null=False)

#     #post date
#     date = models.DateTimeField(null=False)


#     class Meta:
#         app_label = 'msg'


