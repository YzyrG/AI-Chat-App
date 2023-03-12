from django.contrib import admin
from .models import PreviousChat

admin.site.register(PreviousChat)


class PostAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    