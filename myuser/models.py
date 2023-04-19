from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
from posts.models import Post

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,phone,email,username,first_name,last_name,password):
        if not phone:
            raise ValueError('please import your phone')
        if not email:
            raise ValueError('please import your email')
        if not username:
            raise ValueError('please import your username')
        
        user = self.model(
            phone = phone,
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self,phone,email,username,first_name="", last_name="" , password=None ):
        user = self.model(
            phone = phone,
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=11 , unique=True , validators=[
        RegexValidator(regex="\A(09)(0|1|2|3)[0-9]{7}\d\Z", message="phone number is not correct")
    ] )
    email = models.EmailField(max_length=250)
    username = models.CharField(max_length=20 , unique=True)
    first_name = models.CharField(max_length=20 , blank=True , null=True)
    last_name = models.CharField(max_length=50 , blank=True , null=True)
    last_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    photo = models.ImageField(upload_to = 'users/%Y/%m/%d/' , default = 'users/blank-profile.png')
    date_of_birth = models.DateField(null=True , blank=True)
    bio = models.TextField(blank=True , null=True)
    following = models.ManyToManyField("self", through="Contact", related_name="followers", symmetrical=False)
    save_post = models.ManyToManyField(Post , related_name='save_post')
    
    
    
    USERNAME_FIELD ='phone'
    REQUIRED_FIELDS = ['username','email']
    
    objects = MyUserManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self , app_label):
        return True

    

class Contact(models.Model):
    user_from = models.ForeignKey(MyUser,related_name='rel_from_set',on_delete=models.CASCADE)
    user_to = models.ForeignKey(MyUser,related_name='rel_to_set',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)