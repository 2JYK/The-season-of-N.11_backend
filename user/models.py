from django.db import models
from django.contrib.auth.models import AbstractBaseUser
        
class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=30)
    password = models.CharField("비밀번호", max_length=128)
    email = models.EmailField("이메일", max_length=100)
    fullname = models.CharField("사용자 이름", max_length=20)
    join_date = models.DateTimeField("가입일자", auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label): 
        return True

    @property
    def is_staff(self):
        return self.is_admin