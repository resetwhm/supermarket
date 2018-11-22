import hashlib

from django import forms
from django.core import validators

# 注册验证
from django_redis import get_redis_connection

from person.helper import set_password
from person.models import register


class MyregisterFrom(forms.Form):
    tel = forms.CharField(validators=[validators.RegexValidator(r'1[3456789]\d{9}', message='手机号格式不正确')],
                          error_messages={'required': '手机号必须填写'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'required': '密码必须填写', 'max_length': '密码不能大于20位',
                                               'min_length': '密码不能少于6位'})
    repassword = forms.CharField(max_length=20, min_length=6,
                                 error_messages={'required': '密码必须填写', 'max_length': '密码不能大于20位',
                                                 'min_length': '密码不能少于6位'})

    code = forms.CharField(error_messages={'required': '验证码必须填写'})

    # 验证两次输入的密码是否一致
    def clean(self):
        data = self.cleaned_data
        if data.get('password') and data.get('repassword') and data.get('password') != data.get('repassword'):
            raise forms.ValidationError({'repassword': '两次密码不一致'})
        return data

    # 验证手机号是否已经被注册过
    def clean_tel(self):
        data = self.cleaned_data
        tel = data.get('tel')
        rs = register.objects.filter(tel=tel).exists()
        if rs:
            raise forms.ValidationError("手机号码已经被注册")
        return tel

    # 验证验证码是否正确
    def clean_code(self):
        tel = self.cleaned_data.get("tel")
        code = self.cleaned_data.get('code')
        # 获取redis中的
        r = get_redis_connection("default")
        if tel:
            # 获取 redis中获取的值 是二进制编码,必须解码
            r_code = r.get(tel)
            r_code = r_code.decode("utf-8")
            if code is None:
                raise forms.ValidationError("验证码错误!")
            if code != r_code:
                raise forms.ValidationError("验证码填写错误!")
            return code
        else:
            return code


# 登录验证
class MyloginForm(forms.Form):
    tel = forms.CharField(validators=[validators.RegexValidator(r'1[3456789]\d{9}', message='手机号格式不正确')],
                          error_messages={'required': '用户名必须填写'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'required': '密码必须填写', 'min_length': '密码格式不符合要求'})

    # 综合验证手机号码是否注册过和密码是否正确
    def clean(self):
        data = self.cleaned_data
        # 获取用手机和密码
        tel = data.get('tel')
        password = data.get('password')
        # 验证手机号码是否存在
        if all([tel, password]):
            # 根据手机号码获取用户
            try:
                user = register.objects.get(tel=tel)
            except register.DoesNotExist:
                raise forms.ValidationError({"tel": "该用户不存在!"})

            # 判断密码是否正确
            if user.password != set_password(password):
                raise forms.ValidationError({"password": "密码填写错误!"})

            # 正确
            # 将用户信息保存到data中
            data['user'] = user
            return data
        else:
            return data


# 忘记密码
class ForgetFrom(forms.Form):
    tel = forms.CharField(validators=[validators.RegexValidator(r'1[3456789]\d{9}', message='手机号格式不正确')],
                          error_messages={'required': '手机号必须填写'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'required': '密码必须填写', 'max_length': '密码不能大于20位',
                                               'min_length': '密码不能少于6位'})
    repassword = forms.CharField(max_length=20, min_length=6,
                                 error_messages={'required': '密码必须填写', 'max_length': '密码不能大于20位',
                                                 'min_length': '密码不能少于6位'})
    code = forms.CharField(error_messages={'required': '验证码必须填写'})

    def clean(self):
        data = self.cleaned_data
        if data.get('password') and data.get('repassword') and data.get('password') != data.get('repassword'):
            raise forms.ValidationError({'repassword': '两次密码不一致'})
        else:
            return data

        # 验证验证码是否正确
    def clean_code(self):
        tel = self.cleaned_data.get("tel")
        code = self.cleaned_data.get('code')
        # 获取redis中的
        r = get_redis_connection("default")
        if tel:
            # 获取 redis中获取的值 是二进制编码,必须解码
            r_code = r.get(tel)
            r_code = r_code.decode("utf-8")
            if code is None:
                raise forms.ValidationError("验证码错误!")
            if code != r_code:
                raise forms.ValidationError("验证码填写错误!")
            return code
        else:
            return code
