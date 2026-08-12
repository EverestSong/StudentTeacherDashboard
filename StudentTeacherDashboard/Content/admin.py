from django.contrib import admin

from .models import Student
from .models import Teacher
from .models import Subject 
#from .models import Unit 

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
#admin.site.register(Unit)
