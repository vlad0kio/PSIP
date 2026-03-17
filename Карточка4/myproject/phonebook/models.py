from django.db import models

class Abonent(models.Model):
    """
    Модель Абоненты для телефонного узла связи (Задание №4.1)
    """
    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True)
    birth_date = models.DateField('Дата рождения')
    phone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес', max_length=200)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.phone}"

    class Meta:
        verbose_name = 'Абонент'
        verbose_name_plural = 'Абоненты'