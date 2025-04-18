from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, Gender


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            ('Permissions'),
            {'fields':
                (
                    'username',
                    'line_id',
                    'line_name',
                    'gender',
                    'is_barrier_free',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'username', 'line_id', 'line_name', 'gender', 'is_barrier_free', 'is_staff', 'is_deleted', 'deleted_at')
    list_filter = ('is_staff', 'is_superuser', 'is_barrier_free', 'is_active', 'is_deleted', 'groups')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, MyUserAdmin)
admin.site.register(Gender)