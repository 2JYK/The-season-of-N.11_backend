from django.db import models

from user.models import User as UserModel
from article.models import Article as ArticleModel

class Style(models.Model):
    category = models.CharField("카테고리 이름", max_length=100)
    
    def __str__(self):
        return self.category

class Image(models.Model):
    style = models.ForeignKey('Style', verbose_name="스타일", on_delete=models.SET_NELL, null=True)
    user = models.ForeignKey('UserModel', verbose_name="사용자", on_delete=models.CASCADE)
    article = models.ForeignKey('Article', verbose_name="게시글", on_delete=models.CASCADE)
    input = models.ImageField("인풋사진", upload_to="nst/input", height_field=None, width_field=None, max_length=200)
    output = models.ImageField("결과사진", upload_to="nst/output", height_field=None, width_field=None, max_length=200)
    
    def __str__(self):
        return f'{self.input} --> {self.output}'