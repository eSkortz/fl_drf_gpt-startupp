from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from drf_yasg import openapi
from rest_framework.parsers import JSONParser
import json
from datetime import datetime
from fundraising.models import *
from .config import Openapi_token
import openai
import random
import Levenshtein

openai.api_key = Openapi_token


class MyView(viewsets.ViewSet):

    def levenshtein_ratio(text1, text2):
        distance = Levenshtein.distance(text1, text2)
        max_length = max(len(text1), len(text2))
        similarity = (max_length - distance) / max_length * 100
        return similarity

    def request_gpt_with_model(gpt_model, request):
        if request.method == 'POST':
            request_data = json.loads(request.body)
            name = request_data.get('name')
            content = request_data.get('content')
            role = 'user'

            qa_bool = False
            qa_mas = []
            qa_objects = QA.objects.all()
            for object in qa_objects:
                if levenshtein_ratio(content, object.question) >= 80:
                    qa_mas.append(object)
                    qa_bool = True
                    break
                elif object.tags:
                    object_tags = object.tags.split(';')
                    for tag_counter in range(len(object_tags)):
                        if object_tags[tag_counter] in content.lower():
                            qa_mas.append(object)
                            qa_bool = True
                
            if qa_bool:
                try:
                    completion = openai.ChatCompletion.create(
                        model=f'{gpt_model}',
                        messages=[
                            {'role': f'{role}', 'content': f'Act like a startup mentor, make a response with one-sentence points and add a one-sentence intro\n\n{content}', 'name': f'{name}'}
                        ]
                    )
                except Exception:
                    return Response(data = {'status': 'error',
                                            'content': 'Invalid data'}, status = 422)
                else:
                    completion_response = completion.choices[0].message.content

                print(qa_mas)
                question = random.choice(qa_mas)

                services_bool = False
                services_mas = []
                services_objects = Services.objects.all()
                for object in services_objects:
                    if object.qa_id:
                        if str(question.id) in object.qa_id.split(';'):
                            services_mas.append([object.name, object.link, object.how_to_use])
                            services_bool = True
                            break

                videos_bool = False
                videos_mas = []
                videos_objects = Videos.objects.all()
                for object in videos_objects:
                    if object.qa_id:
                        if str(question.id) in object.qa_id.split(';'):
                            videos_mas.append([object.name, object.link])
                            videos_bool = True
                            break
                
                guides_bool = False
                guides_mas = []
                guides_objects = Guides.objects.all()
                for object in guides_objects:
                    if object.qa_id:
                        if str(question.id) in object.qa_id.split(';'):
                            guides_mas.append([object.name, object.link, object.summary])
                            guides_bool = True
                            break
                
                books_bool = False
                books_mas = []
                books_objects = Books.objects.all()
                for object in books_objects:
                        if object.qa_id:
                            if str(question.id) in object.qa_id.split(';'):
                                books_mas.append([object.name, object.link, object.summary])
                                books_bool = True
                                break
                
            else:
                try:
                    completion = openai.ChatCompletion.create(
                        model=f'{gpt_model}',
                        messages=[
                            {'role': f'{role}', 'content': f'{content}', 'name': f'{name}'}
                        ]
                    )
                except Exception:
                    return Response(data = {'status': 'error',
                                            'content': 'Invalid data'}, status = 422)
                else:
                    completion_response = completion.choices[0].message.content

                services_bool = False
                services_mas = []
                services_objects = Services.objects.all()
                for object in services_objects:
                    if object.tags:
                        object_tags = object.tags.split(';')
                        for tag_counter in range(len(object_tags)):
                            if object_tags[tag_counter] in completion_response.lower() or object_tags[tag_counter] in content.lower():
                                services_mas.append([object.name, object.link, object.how_to_use])
                                services_bool = True
                                break
                
                videos_bool = False
                videos_mas = []
                videos_objects = Videos.objects.all()
                for object in videos_objects:
                    if object.tags:
                        object_tags = object.tags.split(';')
                        for tag_counter in range(len(object_tags)):
                            if object_tags[tag_counter] in completion_response.lower() or object_tags[tag_counter] in content.lower():
                                videos_mas.append([object.name, object.link])
                                videos_bool = True
                                break
                
                guides_bool = False
                guides_mas = []
                guides_objects = Guides.objects.all()
                for object in guides_objects:
                    if object.tags:
                        object_tags = object.tags.split(';')
                        for tag_counter in range(len(object_tags)):
                            if object_tags[tag_counter] in completion_response.lower() or object_tags[tag_counter] in content.lower():
                                guides_mas.append([object.name, object.link, object.summary])
                                guides_bool = True
                                break
                
                books_bool = False
                books_mas = []
                books_objects = Books.objects.all()
                for object in books_objects:
                    if object.tags:
                        object_tags = object.tags.split(';')
                        for tag_counter in range(len(object_tags)):
                            if object_tags[tag_counter] in completion_response.lower() or object_tags[tag_counter] in content.lower():
                                books_mas.append([object.name, object.link, object.summary])
                                books_bool = True
                                break
                
                completion_response = completion_response.replace('\n\n', '\n')

            if services_bool or videos_bool or guides_bool or books_bool:
                completion_response = f"{completion_response}\n\n**I've prepared some helpful materials for you**"

            if services_bool:
                completion_response = f"{completion_response}\n\n*You can use the following services:*"
                if len(services_mas) > 3:
                    response_services = random.sample(services_mas, 3)
                else:
                    response_services = services_mas
                for service in response_services:
                    if service[2] != None:
                        completion_response = f'{completion_response}\n[{service[0]}]({service[1]}) {service[2]}'
                    else:
                        completion_response = f'{completion_response}\n[{service[0]}]({service[1]})'
            
            if videos_bool:
                completion_response = f"{completion_response}\n\n*You can watch the following videos:*"
                if len(videos_mas) > 3:
                    response_videos = random.sample(videos_mas, 3)
                else:
                    response_videos = videos_mas
                for video in response_videos:
                    completion_response = f'{completion_response}\n[{video[0]}]({video[1]})'

            if guides_bool:
                response_guide = random.choice(guides_mas)
                if response_guide[2]:
                    completion_response = f'{completion_response}\n\nHere’s the [{response_guide[0]}]({response_guide[1]}) guide and the summary of it:\n{response_guide[2]}'
                else:
                    completion_response = f'{completion_response}\n\nHere’s the [{response_guide[0]}]({response_guide[1]}) guide'

            if books_bool:
                completion_response = f"{completion_response}\n\n*You can look for useful information in these books*"
                if len(books_mas) > 3:
                    response_books = random.sample(books_mas, 3)
                else:
                    response_books = books_mas
                for book in response_books:
                    if book[2] != None:
                        completion_response = f'{completion_response}\n[{book[0]}]({book[1]}) - {book[2]}'
                    else:
                        completion_response = f'{completion_response}\n[{book[0]}]({book[1]})'
            
            new_request = RequestsHistory(user=name, content=content, model=f'{gpt_model}', date=datetime.now(), response=completion_response)
            new_request.save()

            return Response(data = {'status': 'success',
                                    'content': f'{completion_response}'},  
                                    status=200)
        else:
            return Response(data = {'status': 'error',
                                    'content': 'Invalid method'}, status=405)

    # Генерация ответа с помощью модели gpt-3.5-turbo
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['https://quado.pro/django_jain/gpt-35/'],
        operation_id = 'Генерация ответа с помощью модели gpt-3.5-turbo',
        operation_description = 'Эта функция используется получения ответа посредством gpt-3.5-turbo',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'content'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'status': 'success',
                        'content': '...'
                    }
                }
            ),
            422: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid data'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid method'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    @parser_classes([JSONParser])
    def gpt_35(request):
        response = request_gpt_with_model('gpt-3.5-turbo', request)
        return response


    # Генерация ответа с помощью модели gpt-3.5-turbo-16k
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['https://quado.pro/django_jain/gpt-35-16/'],
        operation_id = 'Генерация ответа с помощью модели gpt-3.5-turbo-16k',
        operation_description = 'Эта функция используется получения ответа посредством gpt-3.5-turbo-16k',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'content'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'status': 'success',
                        'content': '...'
                    }
                }
            ),
            422: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid data'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid method'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    @parser_classes([JSONParser])
    def gpt_35_16(request):
        response = request_gpt_with_model('gpt-3.5-turbo-16k', request)
        return response


    # Генерация ответа с помощью модели gpt-4
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['https://quado.pro/django_jain/gpt-4/'],
        operation_id = 'Генерация ответа с помощью модели gpt-4',
        operation_description = 'Эта функция используется получения ответа посредством gpt-4',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'content'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'status': 'success',
                        'content': '...'
                    }
                }
            ),
            422: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid data'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid method'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    @parser_classes([JSONParser])
    def gpt_4(request):
        response = request_gpt_with_model('gpt-4', request)
        return response


    # Генерация ответа с помощью модели gpt-4-32k
    @csrf_exempt
    @swagger_auto_schema(
        method='post',
        tags=['https://quado.pro/django_jain/gpt-4-32/'],
        operation_id = 'Генерация ответа с помощью модели gpt-4-32k',
        operation_description = 'Эта функция используется получения ответа посредством gpt-4-32k',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'content'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Успешное получение списка рекомендаций',
                examples={
                    'application/json': {
                        'status': 'success',
                        'content': '...'
                    }
                }
            ),
            422: openapi.Response(
                description='Некорректные данные запроса',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid data'
                    }
                }
            ),
            405: openapi.Response(
                description='Метод не разрешен',
                examples={
                    'application/json': {
                        'status': 'error',
                        'content': 'Invalid method'
                    }
                }
            ),
        }
    )
    @api_view(['POST'])
    @parser_classes([JSONParser])
    def gpt_4_32(request):
        response = request_gpt_with_model('gpt-4-32k', request)
        return response