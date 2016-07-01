from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import is_password_usable


class OpenspritesUserManager(BaseUserManager):

    def _create_user(self, username, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class OpenspritesUser(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[a-zA-Z0-9-_]+$', message='Only alphanumeric characters are allowed.')

    username = models.CharField(unique=True, max_length=20, validators=[alphanumeric])

    banned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    email = models.EmailField(_('email address'), max_length=254, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = OpenspritesUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):
            self.set_password(self.password)
        super(OpenspritesUser, self).save(*args, **kwargs)
        if len(self.groups.all()) > 0:
            auth_group = self.groups.all()[0].name
        else:
            auth_group = None
        return super(OpenspritesUser, self).save(*args, **kwargs)