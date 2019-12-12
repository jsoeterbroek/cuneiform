from django.contrib import admin
#from django.contrib.postgres import fields
#from django_json_widget.widgets import JSONEditorWidget
from .models import Drug, Doctor, Client, Prescription
#from .forms import PrescriptionAdminForm
#from .models import Profile

#class PrescriptionAdmin(admin.ModelAdmin):
#    form = PrescriptionAdminForm

admin.site.register(Drug)
admin.site.register(Doctor)
admin.site.register(Client)
admin.site.register(Prescription)

#class ProfileInline(admin.StackedInline):
#    model = Profile
#    can_delete = False
#    verbose_name_plural = 'Profile'
#    fk_name = 'user'
#
#class CustomUserAdmin(UserAdmin):
#    inlines = (ProfileInline, )
#
#    def get_inline_instances(self, request, obj=None):
#        if not obj:
#            return list()
#        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
#
#
#admin.site.unregister(User)
#admin.site.register(User, CustomUserAdmin)
