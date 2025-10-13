from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active', 'user_role', 'groups')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais e status', {'fields': ('profile_picture', 'user_role', 'is_approved')}),
        ('Permissões', {'fields': ('is_active', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'user_role', 'password', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
        
    @admin.action(description='Aprovar empresas selecionadas')
    def approve_enterprise(self, request, queryset):
        """
        Ação que ativa e aprova as empresas com cadastro pendente.
        """
        queryset.filter(user_role=User.UserRole.ENTERPRISE, is_approved=False).update(is_active=True, is_approved=True)
        self.message_user(request, "Empresas selecionadas foram aprovadas e ativadas.")