from rest_framework import serializers
from .models import *
from .utils import *
from rest_framework.exceptions import ValidationError
from django.db.models import Q


class SignUpSerializer(serializers.ModelSerializer):
    auth_phone_country = serializers.CharField(required=False, read_only=True)
    auth_status = serializers.CharField(required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['phone_country'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('auth_phone_country', 'auth_status')

    def validate_phone_country(self, phone_country):
        user = User.objects.filter(phone_number=phone_country)
        if user.exists():
            data = {'status': False, 'message': "Ushbu foydalanuvchi oldin ro'yhatdan o'tgan!"}
            raise ValidationError(data)
        return phone_country

    def validate(self, data):
        user_input = data.get('phone_country')
        phone_number_country = check_country_phone_number(user_input)

        if phone_number_country == 'UZB':
            data = {'auth_phone_country':UZB, 'phone_number': user_input}
        elif phone_number_country == 'KAZ':
            data = {'auth_phone_country':KAZ, 'phone_number': user_input}
        elif phone_number_country == 'USA':
            data = {'auth_phone_country':USA, 'phone_number': user_input}
        elif phone_number_country == 'RUS':
            data = {'auth_phone_country':RUS, 'phone_number': user_input}
        elif phone_number_country == 'KOR':
            data = {'auth_phone_country':KOR, 'phone_number': user_input}
        else:
            data = {'status': False, 'message': 'Your data is incorrect!'}
            raise ValidationError(data)
        return data
    
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        auth_type = validated_data.get('auth_phone_country')
        if auth_type == UZB:
            code = user.create_confirmation_code(UZB)
            send_sms(code)
        elif auth_type == KAZ:
            code = user.create_confirmation_code(KAZ)
            send_sms(code)
        elif auth_type == USA:
            code = user.create_confirmation_code(USA)
            send_sms(code)
        elif auth_type == RUS:
            code = user.create_confirmation_code(RUS)
            send_sms(code)
        elif auth_type == KOR:
            code = user.create_confirmation_code(KOR)
            send_sms(code)
        else: 
            data = {'status': False, 'message': 'Code yuborishda xatolik yuz berdi!'}
            raise ValidationError(data)
        return user
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data['access'] = instance.token()['access']
        data['refresh'] = instance.token()['refresh']
        return data