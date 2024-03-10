import re
from rest_framework.validators import ValidationError

uzb_phone_number_regex = r'^\+998\d{9}$'                             #'+998901234567'
kaz_phone_number_regex = r'^\+997\d{9}$'                             #'+997783567890'
usa_phone_number_regex = r'^\+1\(\d{3}\)\d{7}$'                      #'+1(212)5551234'
rus_phone_number_regex = r'^\+7\(\d{3}\)\d{7}$'                      #'+7(495)1234567'        
kor_phone_number_regex = r'^\+8210\d{8}$'                            #'+821012345678'

# Qulaylik uchun yuqoridagi telefon nomerlarini kiritib tekshirishingiz mumkin

def check_country_phone_number(user_input):
    if re.match(uzb_phone_number_regex, user_input) is not None:
        return 'UZB'
    elif re.match(kaz_phone_number_regex, user_input) is not None:
        return 'KAZ'
    elif re.match(usa_phone_number_regex, user_input) is not None:
        return 'USA'
    elif re.match(rus_phone_number_regex, user_input) is not None:
        return 'RUS'
    elif re.match(kor_phone_number_regex, user_input) is not None:
        return 'KOR'
    else:
        data = {'status': False, 'message': 'Please enter your phone number or incorrectly data!'}
        raise ValidationError(data)