# -*- coding: utf-8 -*-
from django.forms import ChoiceField, Form, EmailField, URLField, MultipleChoiceField
from .models import Browser, OperatingSystem, Resolution
from django import forms


class TestRequestForm(Form):
    BROWSER_CHOICES = [(operating_system, [(browser.id, browser) for browser in Browser.objects.filter(
            operating_system_id=operating_system.id).order_by('company', 'name', 'version')]) for operating_system in
                       OperatingSystem.objects.all().order_by('company', 'name', 'version')]
    RESOLUTION_CHOICES = [(resolution.id, resolution) for resolution in
                          Resolution.objects.all().order_by('width', 'height', 'aspect_ratio')]
    browsers = ChoiceField(widget=forms.SelectMultiple(attrs={'required': True}),
                           choices=BROWSER_CHOICES)
    resolutions = MultipleChoiceField(widget=forms.SelectMultiple(attrs={'required': True}),
                                      choices=RESOLUTION_CHOICES)
    email = EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
                       max_length=100,
                       error_messages={'required': 'Укажите логин'})
    urls = URLField(widget=forms.URLInput(attrs={'class': 'form-control', 'required': True}),
                    max_length=100,
                    error_messages={'required': 'Укажите пароль'})

    # Валидация проходит в этом методе
    def clean(self):
        # Определяем правило валидации
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_again'):
            # Выбрасываем ошибку, если пароли не совпали
            raise forms.ValidationError('Пароли должны совпадать!')
        return self.cleaned_data
