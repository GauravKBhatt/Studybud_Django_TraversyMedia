from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChatmessageCreateForm
from django.shortcuts import redirect

class ChatView(LoginRequiredMixin,View):
    chat_group=ChatGroup.objects.get(group_name="public-chat")
    chat_messages=chat_group.groupmessage_set.all()[:30]
    form=ChatmessageCreateForm()
    context={
            'chat_messages':chat_messages,
            'form':form
        }
    
    def get(self,request):
        return render(request,'rtchat/chat.html',self.context,)
    
    def post(self,request):
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message=form.save(commit=False)
            message.author=request.user
            message.body = form.cleaned_data['body']
            message.group=self.chat_group
            message.save()
            return redirect('chat')