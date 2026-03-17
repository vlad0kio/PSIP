from django import forms


class UserDataForm(forms.Form):
    """
    Форма для ввода имени, пола и девичьей фамилии
    """
    GENDER_CHOICES = [
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    ]

    user_name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Пол',
        widget=forms.RadioSelect,
        required=True
    )

    maiden_name = forms.CharField(
        max_length=100,
        label='Ваша девичья фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )