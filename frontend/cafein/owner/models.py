from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):

    def create_user(self, email,owner_id, password = None):
        if not email:
            raise ValueError("not email")

        user = self.model(
            email = self.normalize_email(email),
            owner_id = owner_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        print("create_user")
        return user
    

    def create_superuser(self, email,owner_id, password):
        user = self.create_user(
           email = self.normalize_email(email),
           owner_id = owner_id,
           password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        print("create_superuser")
        return user
     

class Owner(AbstractBaseUser):
    
    owner_id = models.EmailField(max_length = 100,primary_key=True ,default='')
    email = models.EmailField(verbose_name='email',max_length = 100 ,unique = True, default='')
    password = models.CharField(max_length=300, default='')
    phone = models.CharField(max_length=25, unique = True , default='')
    #username = models.CharField("사용자 계정", max_length=20, unique=True)

    is_admin    = models.BooleanField(default=False) # 관리자 권한 여부 (기본값은 False)
    is_active   = models.BooleanField(default=True)  # 활성화 여부 (기본값은 True)
    is_staff    = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['owner_id']

    
    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    # 일반적으로 선언만 해두고 건들지않는다
    def has_perm(self, perm, obj=None):
        return True

    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    # 일반적으로 선언만 해두고 건들지않는다
    def has_module_perms(self, app_label):
        return True
    
    #admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'owner'

    def __str__(self):
        return self.email

    objects = MyAccountManager() 
    
 

