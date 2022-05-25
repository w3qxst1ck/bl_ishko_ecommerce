from captcha.widgets import ReCaptchaV2Invisible
from django import forms
from captcha.fields import ReCaptchaField


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible(attrs={
            'data-size': 'compact',
        }))