from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']

    def save(self, **kwargs):
        self.is_valid()
        user = MyUser.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = MyUser.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
        return new_user


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height', ]


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.CharField()

    class Meta:
        model = Images
        fields = ['title', 'data']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class PerevalSerializer(WritableNestedModelSerializer):
    user_id = MyUserSerializer()
    coord_id = CoordSerializer()
    level_id = LevelSerializer(allow_null=True, default=False)
    images = ImagesSerializer(many=True)

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user_id
            data_user = data.get('user_id')
            user_fields_for_validation = [
                instance_user.email != data_user['email'],
                instance_user.phone != data_user['phone'],
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Ошибка': 'Нельзя редактировать данные о пользователе!',
                    }
                )
        return data

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user_id', 'coord_id',
                  'level_id', 'images', 'status']
        # read_only_fields = ['status']
