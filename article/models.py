from django.db import models
import article


class Article(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    # image = models.models.ForeignKey()
    title = models.CharField("제목", max_length=30)
    content = models.CharField("내용", max_length=100)
    created_at = models.DateTimeField("등록 일자", auto_now_add=True)
    modlfied_at = models.DateTimeField("수정 일자", auto_now=True)
    def __str__(self):
        return f'id [ {self.id} ] {self.user.username} 님이 작성한 Article'


class Comment(models.Model):
    article =  models.ForeignKey('Article', verbose_name="게시글", on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    content = models.CharField("내용", max_length=100)
    modlfied_at = models.DateTimeField("수정 일자", auto_now=True)
    def __str__(self):
        return f'id [ {self.id} ] {self.article.title} : {self.content} / {self.user.username}님이 작성한 댓글'

    
class Like(models.Model):
    article = models.ForeignKey('Article', verbose_name="게시글", on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    def __str__(self):
        return f'id [ {self.id} ] {self.user.username}가 {self.article.title}글을 좋아합니다.'


class BookMark(models.Model):
    article = models.ForeignKey('Article', verbose_name="게시글", on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    def __str__(self):
        return f'id [ {self.id} ] {self.user.username} 유저가 {self.article.title}글을 북마크 했습니다.'