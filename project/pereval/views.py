from .models import *
from rest_framework import viewsets, status, generics
from .serializers import MyUserSerializer, CoordSerializer, LevelSerializer, ImagesSerializer, PerevalSerializer
from rest_framework.response import Response
from django.http import JsonResponse


class MyUserView(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class CoordsView(viewsets.ModelViewSet):
    queryset = Coord.objects.all()
    serializer_class = CoordSerializer


class ImagesView(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class LevelView(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def partial_update(self, request, *args, **kwargs):
        print('тест вьюшки')
        record = self.get_object()
        if record.status == 'NW':
            serializer = PerevalSerializer(record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'state': '1',
                        'message': 'Изменения внесены успешно'
                    }
                )
            else:
                return Response(
                    {
                        'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    'state': '0',
                    'message': f'При данном статусе: {record.get_status_display()}, данные изменить нельзя!'
                }
            )


class EmailAPIView(generics.ListAPIView):
    serializer_class = PerevalSerializer

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Pereval.objects.filter(user_id__email=email):
            data = PerevalSerializer(Pereval.objects.filter(user_id__email=email), many=True).data
            api_status = status.HTTP_200_OK
        else:
            data = {
                'message': f'Не существует пользователя с таким email - {email}'
            }
            api_status = 404
        return JsonResponse(data, status=api_status, safe=False)
