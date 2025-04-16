from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChatmessageCreateForm
from django.shortcuts import redirect
from django.template.loader import render_to_string

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
    
    # CENTRAL method in django that decides which HTTP method to call. We can override it to call custom methods like def htmx()
    def dispatch(self, request, *args, **kwargs):
        # every HTMX sends a special header HX-Request: true on every HTMX request. 
        if request.method.lower() == 'post' and request.headers.get('HX-Request'):

            return self.htmx(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    # if the request is not a HTMX method it calls the default dispatch method. 

    def htmx(self,request):
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message=form.save(commit=False)
            message.author=request.user
            message.body = form.cleaned_data['body']
            message.group=self.chat_group
            message.save()
            context={
                'message':message,
                'user':request.user
            }
            html = render_to_string('rtchat/chat_message_partial.html',context,request=request)
            return HttpResponse(html)
        return HttpResponse("Form is invalid",status=400)