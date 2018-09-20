from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User
from .models import UserProfile

# Registering your new class to be used by Django admin for your new User model.
@admin.register(User)
# Extending the original UserAdmin class that Django admin provides.
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    # Replacing the use of username for email.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'city', 'phone', 'website')

    def user_info(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        # 첫번째 인자를 기준으로 정렬시킨후 같은값이 나왔을 경우 두번째인자를 기준으로 정렬
        queryset = queryset.order_by('website', 'user')
        return queryset

    # user_info 이름을 info라고 변경해 나타내기
    user_info.short_description = 'info'

admin.site.register(UserProfile, UserProfileAdmin)
