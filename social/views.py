from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView #createview provide us an end point where we can get and post 
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin 

from django.db.models import Q

from social import models,forms
# Create your views here.
class Wall(LoginRequiredMixin, ListView):

    context_object_name='posts'
    template_name='social/wall.html'
    login_url='auth/login'
    

    # hume queryset ko update krna h based on the current logged in 
    #user(i.e self.request.user mtlb current logged in user)
    # we want all the post jahan hum friendship ke part h
    def get_queryset(self):
        friendIds=[ friend.person2.id for friend in models.Friends.objects.filter(person1=self.request.user)]   #we are selecting all the friends where i am the person1 of the friendship aur fir hum uss person2 ki id nikal re h 
        friendIds=friendIds+[ friend.person1.id for friend in models.Friends.objects.filter(person2=self.request.user)]  #then selecting all the ids where i am ther person two of the friendship
        return models.Post.objects.filter(user__in=friendIds).order_by('-created_at') #find all the posts where user is in the list

        # return models.Post.objects.filter(         #self.request.user mujhe string object return kr ra lekin mujhe user object chahiye isliye hum pk i.e. primary key user kr re h taaki ye id return kare

        #    (Q(user__person1=self.request.user.pk) | Q(user__person2=self.request.user.pk)) & 
        #     ~Q(user=self.request.user) #ye hum apni post hatane ke liye laga re h 
        # ).order_by('-created_at')
        #__ means  attribute 
        # we connect with frontend by rest api

       #foreign key jo banti h wo  point krti h primary key of other table
       #yahan primary key ke basis pr filter hora h 
    
#for example hum friendship ko table consider kr re h 
#jahan pr there are two entities ek person1 aur person2 
#so we wnt all the post jiska user in saari friendjip ka part ho
#jahan pr ya to person1 me h ya person2 me h 
#so we filtered out all the friendship rows where either person 1 or person2 is me


#user table
#green are foreign key constraint h 

class Home(LoginRequiredMixin,ListView):
    context_object_name='posts'
    template_name='social/home.html'
    login_url='auth/login.html'

    def get_queryset(self):
        return models.Post.objects.filter(user=self.request.user)
#Listview fetches all the info from queryset and stores it in context_object_name variable
#but if we want to add our custom data we can overwrite the function n add our own data in the data dictionary
    def get_context_data(self, *args, **kwargs):
        data= super().get_context_data(*args,**kwargs)  #what super() does is it will use parent class to make context data and in context data
        data['post_form']=forms.PostForm()  #we'll add post_form as forms.postForm ..jo bhi humne context data bnaya tha hum usko postforms mei add kr re h 
        return data

#
#interviwe questions--class based view google karo aur read documentary
# as_view() , dispatch ke ander kya hota h **options kya hota h
# pre flight request-cors wala error ->
#how does cookies work
#local storage used in front end
#hume agr ek url milta h to how will we identify whether image is jpg or png 
# import rquests
#r=requests.get(url)
#r.headers   content_type tells the mime type of the image
#hum sirf headers se hi pehle check kr lete h image ka size type wgrh wgrh



class Post(View):
    def post(self,request):
        form=forms.PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False) #it will return us the object of model 
            post.user=request.user #now we can request the user id to the object of model and then save that object in database
            post.save()
            return redirect('/home/')


#IF WE WANT TO UPLOAD A FILE IN MODEL WE HAVE TO REQUEST TO FILES kyunki jo files upload hoti h 
#wo request.FILES se aari hoti h..... 

#Mixins dont send the request but they plug and play they functionalities in intermediate process
#SingleObjectMixin extracts the pk from the url and get the object
class PostLike( View):
    model=models.Post

    def post(self,request,pk):
        post=self.model.objects.get(pk=pk)
        models.Like.objects.create(post=post,user=request.user)
        return HttpResponse(code=204)  #204 request is we are not sending any content but your work is done (httpstatuses.com)
    

class PostComment(View):
    model=models.Post
    form=forms.PostComment

    def post(self,request,pk):
        post=self.model.objects.get(pk=pk)
        form=self.form(request.POST)

        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.user=request.user
            comment.save()
            return HttpResponse(code=204)
        print(form.errors)
        return HttpResponse('Error')
