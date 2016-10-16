from django.shortcuts import render, get_object_or_404
from .models import Message

# Create your views here.

def details(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    return render(request, 'messages/detail.html', {'message' : message})