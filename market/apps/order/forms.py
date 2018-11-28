from django import forms

from person.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['add_time', 'update_time', 'isdelete', 'log','isDefault']

        error_messages = {
            'name': {
                'required': "请填写用户名！",
            },
            'tel': {
                'required': "请填写手机号码！",
            },
            'brief': {
                'required': "请填写详细地址！",
            },
            'hcity': {
                'required': "请填写完整地址！",
            },
            'hproper': {
                'required': "请填写完整地址！",
            },
            'harea': {
                'required': "请填写完整地址！",
            },
        }
