from rest_framework import serializers
from .models import *
from .utils import *
from rest_framework.exceptions import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
    auth_phone_country = serializers.CharField(required=False, read_only=True)
    auth_status = serializers.CharField(required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['phone_country'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('auth_phone_country', 'auth_status')

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