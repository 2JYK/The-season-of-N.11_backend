from django.db import models

class Style(models.Model):
    category = models.CharField("카테고리 이름", max_length=100)
    
    def __str__(self):
        return self.category

class Image(models.Model):
    style = models.ForeignKey('Style', verbose_name="스타일", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', verbose_name="게시글", on_delete=models.CASCADE)
    output_img = models.ImageField("결과사진", upload_to="nst/output", height_field=None, width_field=None, max_length=200)
    
    def __str__(self):
        return f'{self.user} --> {self.output}'