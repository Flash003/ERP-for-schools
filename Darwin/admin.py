from django.contrib import admin
from Darwin import models
# Register your models here.
admin.site.register(models.Announcement)
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.TeacherSchedule)
admin.site.register(models.Event)
admin.site.register(models.LeaveRequest)
#admin.site.register(models.StudentClass)
admin.site.register(models.StudentAttendance)
admin.site.register(models.Subjects)
admin.site.register(models.Marks)
admin.site.register(models.TeacherAttendance)
admin.site.register(models.ClassSchedule)
