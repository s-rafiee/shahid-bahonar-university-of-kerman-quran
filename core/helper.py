import datetime

from django import template
import re
import jdatetime
from jalali_date import datetime2jalali
from kavenegar import *
from core.settings import Kavenegar_ATP, Kavenegar_Number
from random import randint
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

register = template.Library()


def send_otp(mobile, otp):
    print(otp)
    return True
    mobile = [mobile, ]
    try:
        api = KavenegarAPI(Kavenegar_ATP)
        params = {
            'sender': Kavenegar_Number,
            'receptor': mobile,
            'message': 'your code is {}'.format(otp),
        }
        response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return 1234
    return randint(1000, 9999)


def isInt(code):
    try:
        if int(code) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def isPhone(phone):
    if re.match(r'^(09)([0-9]{9}){1}$', phone):
        return True
    else:
        return False


@register.simple_tag
def toJalali(date):
    return datetime2jalali(date).strftime('%Y/%m/%d %H:%M:%S')


def get_City():
    return ['کرمان', 'سیرجان', 'رفسنجان', 'بم', 'جیرفت', 'زرند', 'رودبار جنوب', 'کهنوج', 'شهربابک', 'ریگان',
            'بافت', 'عنبر آباد', 'بردسیر', 'قلعه گنج', 'فهرج', 'منوجان', 'نرماشیر', 'راور', 'ارزوئیه', 'انار',
            'رابر', 'فاریاب', 'کوهبنان']


def is_National_Code(code):
    code = code.strip()
    if re.match(r'[0-9]{10}$', code) and not re.match(r'' + code[0] + '{10}$', code):
        try:
            sum = 0
            for i in range(9):
                sum = sum + ((10 - i) * int(code[i]))
            ret = sum % 11
            parity = int(code[-1])
            if ((ret < 2 and ret is parity) or (ret >= 2 and ret is (11 - parity))):
                return True
            return False
        except:
            return False
    else:
        return False


def isDate(date):
    try:
        jdatetime.datetime.strptime(date, '%d/%m/%Y')
        return True
    except:
        return False


def isTel(tel):
    if re.match(r'^0[1-9]{1}[0-9]{9}$', tel):  # ^0\d{10}$
        return True
    else:
        return False


def isPostalCode(tel):
    if re.match(r'^[0-9]{10}$', tel):
        return True
    else:
        return False


def isMail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
