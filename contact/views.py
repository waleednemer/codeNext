from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )
        
        messages.success(request, 'تم إرسال رسالتك بنجاح!')
        return redirect('contact:contact')
    
    return render(request, 'contact/contact.html')