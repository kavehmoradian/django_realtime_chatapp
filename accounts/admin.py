from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'username', 'is_admin')
	list_filter = ('is_admin',)
	readonly_fields = ('last_login',)

	fieldsets = (
		('Main', {'fields':('email', 'username', 'password')}),
		('Permissions', {'fields':('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
	)

	add_fieldsets = (
		(None, {'fields':('username', 'email', 'password1', 'password2')}),
	)

	search_fields = ('email', 'username')
	ordering = ('username',)
	filter_horizontal = ('groups', 'user_permissions')

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser
		if not is_superuser:
			form.base_fields['is_superuser'].disabled = True
		return form


admin.site.register(User, UserAdmin)
