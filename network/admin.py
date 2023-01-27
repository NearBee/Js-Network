from django.contrib import admin
from network.models import User, New_Post

# Register your models here.


admin.site.register(User)

# TODO: Eventually create CLASS ManyToManyInline(admin.TabularInline)


class NewPostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post_field",
    )

    # inlines =[]

    # exclude = (said inlines)


admin.site.register(New_Post, NewPostAdmin)
