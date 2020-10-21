from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAPI
from .forms import CustomUserChangeForm, CustomUserCreationForm


class MyAdmin(UserAdmin):
    # model = UserAPI
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = UserAPI
    list_display = ('email', 'name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'name',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    # add_fieldsets = ()
    # fieldsets = (
    #     (None, {'fields': ('email',)}),
    #     ('Permissions', {'fields': ('is_admin',)}),
    # )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'fields': ('email','name','password1','password2',),
        }),
    )


admin.site.register(UserAPI, MyAdmin)
# Register your models here.
