from django.contrib import admin

from academy.models import Academy
from association.models import Association

# Register your models here.

admin.site.register([Academy, Association])