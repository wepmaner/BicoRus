from django.db import models
from django.contrib.auth.models import User
from django  import utils

# Create your models here.
class UserTotp(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=32,default='')

class Group(models.Model):
    name = models.CharField('Название группы',max_length=100)
    year = models.SmallIntegerField('Курс')
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    def __str__(self):
        return self.name+str(self.year)

class Subject(models.Model):
    teacher_name = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
    def __str__(self):
        return f'{self.teacher_name}/{self.subject_name}'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    def __str__(self) -> str:
        return self.name

class Document(models.Model):
    name = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
    def __str__(self):
        return f'{self.name}'
