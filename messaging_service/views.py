from django.shortcuts import redirect, get_object_or_404
from .models import Message
from django.views.generic import DetailView
from django.contrib import messages


# Create your views here.

class MessageDetail(DetailView):
    model = Message


def delivered(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.mark_as_delivered()
    messages.success(request, 'Successfully marked as delivered')
    return redirect('detail', pk)
