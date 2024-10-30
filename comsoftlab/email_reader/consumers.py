# Асинхронность
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Сериализация
import json
from .serializers import EmailMessageSerializer

# Почта
from imap_tools import MailBox

# Модели
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import EmailMessage, EmailMessageFile, TargetEmail
from django.shortcuts import get_object_or_404


class WSEmailReader(AsyncWebsocketConsumer):
    async def load_messages(self, service):
        """
        :param service: код почтового сервиса, к примеру "GM", "YA"
        :return: отправляет вебсокету все сообщения из базы данных, отфильтрованных по сервису, по мере поступления
        """
        # Запрос, который собирает все сообщения из базы данных по сервису, сортирует по добавлению;
        # Сразу подгружаем файлы, так как информация о них тоже понадобится в теле сообщения
        query_set = await sync_to_async(list)(
            EmailMessage.objects.filter(service=service).order_by('-uid').prefetch_related('files'))
        # Перебираем полученные сообщения
        for count, message in enumerate(query_set):
            # Сериализуем
            serializer = EmailMessageSerializer(message)
            # В запрос также добавляем информацию о количестве загруженных сообщений и их общем количестве
            json_response = json.dumps({
                'message': serializer.data,
                'total_messages': len(query_set),
                'count': count + 1
            })
            await self.send(json_response)

    async def connect(self):
        # Получаем все нужные параметры get-запроса
        self.email = self.scope['url_route']['kwargs'].get('email')
        self.service = self.scope['url_route']['kwargs'].get('service')

        # Если какого-либо параметра не хватает, закрываем соединение
        if self.email is None or self.service is None:
            await self.close()

        # Находим в базе данных email, указанный в запросе, чтобы достать его данные в будущем для авторизации
        target_email = await sync_to_async(get_object_or_404)(TargetEmail, email=self.email)

        # Если почта не найдена в системе, также закрываем соединение
        if target_email is None or self.service is None:
            await self.close()

        # После того как предварительные проверки пройдены, принимаем запрос на соединение
        await self.accept()

        # Подключаемся к указанной электронной почте
        with MailBox(target_email.server).login(target_email.email, target_email.password) as mailbox:
            """
            Переменная, которая гарантирует, что если ни одного импортированного сообщения не было найдено в системе,
            загрузка все равно произойдет
            """
            load_started = False

            # Перебираем все входящие сообщения
            for count, msg in enumerate(mailbox.fetch()):
                # Сохраняем уникальный идентификатор ОТНОСИТЕЛЬНО почтового ящика
                uid = msg.uid
                # Форматируем дату, чтобы она удовлетворяла DateField Django
                formatted_date = msg.date.strftime('%Y-%m-%d %H:%M:%S%z')
                # Получаем код сервиса
                msg_service = (self.service[0:2]).upper()

                """
                Проверяем, импортировано сообщение в систему или нет. Если created = True, 
                значит до этого не было импортировано
                """
                obj, created = await sync_to_async(EmailMessage.objects.get_or_create)(uid=uid,
                                                                                       email_from=msg.from_,
                                                                                       subject=msg.subject,
                                                                                       text=msg.text,
                                                                                       date_sent=formatted_date,
                                                                                       service=msg_service)

                # И так, если не было импортировано, значит продолжается процесс чтения
                if created:
                    # Отправляем сведения о прочтении и импортировании сообщения
                    response = {"progress": count + 1}
                    json_response = json.dumps(response)
                    await self.send(json_response)

                    """
                    Если к сообщению также прилагаются файлы, загружаем их с помощью SimpleUploadedFile, так как
                    сам файл у нас представлял в payload
                    """
                    if msg.attachments:
                        for att in msg.attachments:
                            file = SimpleUploadedFile(
                                name=att.filename,
                                content=att.payload,
                                content_type=att.content_type
                            )
                            # Используем на всякий случай get_or_create, чтобы избежать репликантов
                            await sync_to_async(EmailMessageFile.objects.get_or_create)(message=obj,
                                                                                        file=file)

                    """Если сообщение уже импортировано в систему, значит, процесс чтения завершен,
                    можно переходить к отправке всех импортированных сообщений по вебсокету"""
                else:
                    # Указываем, что загрузка сообщений была начата
                    load_started = True
                    await self.load_messages(service=msg_service)
                    break
            # Если загрузка так и не началась, начинаем ее принудительно
            if not load_started:
                await self.load_messages(service=msg_service)
