from django.shortcuts import render
from .models import Message
from django.db.models import Q
from django.contrib import messages
from .forms import MessageReplyForm
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin




# Create your views here.
class MyMessages(LoginRequiredMixin, ListView):
    template_name = "message/message_list.html"
    model = Message
    paginate_by = 4
    context_object_name = 'new_message'

    # queryset = model.objects.filter(property__agent=self.request.user, new=True)

    def get_queryset(self):
       return super(MyMessages, self).get_queryset().filter(consumer=self.request.user).order_by("-message_date")


def message_detail(request, pk, conversation_id):

    message_reply_form = MessageReplyForm()
    conversation = Message.objects.filter(conversation_id=conversation_id)
    message = Message.objects.get(pk=pk)
    if message.new:
        message.new = False
        message.save()
    if request.method == "POST":
        form = MessageReplyForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.property = message.property
            save_form.sender = request.user #message.consumer
            save_form.consumer = message.sender
            if message.type == "response":
                save_form.type = "request"
            else:
                save_form.type = "response"
            save_form.conversation_id = conversation_id
            form.save()
            messages.success(request, "Message sent")
        else:
            messages.error(request, "Message not sent")
            message_reply_form = message_reply_form(request.POST)
    context={"message":message,"form":message_reply_form, "all_msgs":conversation}
    return render(request, "message/message_detail.html", context)
