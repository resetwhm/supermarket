from django import forms

from person.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['add_time', 'update_time', 'isdelete', 'log']

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

    def clean(self):
        user_id = self.data.get('id')
        count = Address.objects.filter(log_id=user_id, isdelete=False).count()
        if count >= 6:
            raise forms.ValidationError('地址不能超过6个')

        isDefault = self.cleaned_data.get('isDefault')
        if isDefault:
            Address.objects.filter(log_id=user_id).update(isDefault=False)
        return self.cleaned_data


class AddresseditForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['add_time', 'update_time', 'isdelete', 'log']

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

    def clean(self):
        user_id = self.data.get('id')

        isDefault = self.cleaned_data.get('isDefault')
        if isDefault:
            Address.objects.filter(log_id=user_id).update(isDefault=False)
        return self.cleaned_data
