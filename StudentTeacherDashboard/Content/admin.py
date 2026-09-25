from django.contrib import admin
from .models import Student, Teacher, Subject, Unit, UnitOutline, CustomUser

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Unit)
admin.site.register(UnitOutline)
admin.site.register(CustomUser)


