# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, DateTimeField, CharField, TextField, ForeignKey, CASCADE, FloatField, \
    IntegerField, SlugField
from django.utils.text import slugify


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    slug = SlugField(unique=True)

    class Meta:
        abstract = True

    def save( self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert,force_update,using,update_fields)





class C(BaseModel):
    class Meta:
        verbose_name_plural = 'Cs'
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class P(BaseModel):
    name = CharField(max_length=60)
    image = CharField(max_length=100)
    description = TextField()
    price = FloatField()
    c = ForeignKey('apps.C',on_delete=CASCADE,related_name='products',to_field='slug')
    shipping_price = FloatField()
    quantity = IntegerField()
    discount = IntegerField()

    @property
    def discount_price(self):
        return self.price - (self.discount * self.price / 100)

    def __str__(self):
        return self.name


class Icon(Model):
    c_icon = CharField(max_length=100)
    category = ForeignKey('apps.C',CASCADE,'iconic')

    def __str__(self):
        return self.c_icon




class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    phone_number = CharField(max_length=100,unique=True)
    objects = CustomUserManager()
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    @property
    def wishlist_all(self):
        return self.wishlists.values_list('product__slug', flat=True)


class W(Model):
    user = ForeignKey('apps.User', CASCADE,related_name='wishlists')
    product = ForeignKey('apps.P', CASCADE,related_name='wishlists', to_field='slug')




class Booking(Model):
    product = ForeignKey('apps.P', CASCADE, related_name='orders')
    quantity = IntegerField(default=1)
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    name = CharField(max_length=100)
    phone_number = CharField(max_length=20)
