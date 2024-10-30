from django.shortcuts import render
from .models import EmailMessage, EmailMessageFile, TargetEmail
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

def index(request):
    emails_in_system = TargetEmail.objects.all()
    return render(request, 'index.html', {"emails_in_system": emails_in_system})

def detail(request, service, uid):
    try:
        message = EmailMessage.objects.filter(service=service).prefetch_related('files').get(uid=uid)
        return render(request, 'detail.html', {"message": message})
    except EmailMessageFile.DoesNotExist:
        raise Http404("Сообщение не найдено в системе")
        
def downoald(request, service, message, file_id):
    # Находим нужный файл
    file = get_object_or_404(EmailMessageFile, message__service = service, message__uid=message, id=file_id)
    # Получаем адрес его пути
    file_path = file.file.path
    # Подготавливаем его к отправке клиенту
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
        return response
