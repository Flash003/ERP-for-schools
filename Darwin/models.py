from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    #User
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    #Personal Details
    profile_picture = models.ImageField(upload_to='profiles', default='profiles/default_user.jpg')
    gender = models.CharField(max_length=7, choices = (('male', 'male'),('female', 'female')))
    #Contact Information
    class_teacher = models.CharField(max_length = 20, choices = (('pre-nursery', 'pre-nursery'),
                                                                ('nursery', 'nursery'),
                                                                ('kinder-garten', 'kinder-garten'),
                                                                ('Grade - 1', 'Grade - 1'),
                                                                ('Grade - 2', 'Grade - 2'),
                                                                ('Grade - 3', 'Grade - 3'),
                                                                ('Grade - 4', 'Grade - 4'),
                                                                ('Grade - 5', 'Grade - 5'),
                                                                ('Grade - 6', 'Grade - 6'),
                                                                ('Grade - 7', 'Grade - 7'),
                                                                ('Grade - 8', 'Grade - 8'),
                                                                ('Grade - 9', 'Grade - 9'),
                                                                ('Grade - X', 'Grade - X'),
                                                                ('Grade - XI', 'Grade - XI'),
                                                                ('Grade - XII', 'Grade - XII'),
                                                                ('none', 'none')), default = 'none')
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    #Other Details
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    aadhar_number = models.BigIntegerField()
    qualification = models.CharField(max_length=200)
    salary = models.IntegerField()

    def __str__(self):
        return self.user.first_name

class Student(models.Model):
    #User
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    #student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    attendance_count = models.PositiveIntegerField(default=0)
    total_attendance = models.PositiveIntegerField(default = 0)
    #Personal Details
    profile_picture = models.ImageField(upload_to='profiles', default='profiles/default_user.jpg')
    gender = models.CharField(max_length=7, choices = (('male', 'male'),('female', 'female')))
    class_studying = models.CharField(max_length = 20, choices = (('pre-nursery', 'pre-nursery'),
                                                                ('nursery', 'nursery'),
                                                                ('kinder-garten', 'kinder-garten'),
                                                                ('Grade - 1', 'Grade - 1'),
                                                                ('Grade - 2', 'Grade - 2'),
                                                                ('Grade - 3', 'Grade - 3'),
                                                                ('Grade - 4', 'Grade - 4'),
                                                                ('Grade - 5', 'Grade - 5'),
                                                                ('Grade - 6', 'Grade - 6'),
                                                                ('Grade - 7', 'Grade - 7'),
                                                                ('Grade - 8', 'Grade - 8'),
                                                                ('Grade - 9', 'Grade - 9'),
                                                                ('Grade - X', 'Grade - X'),
                                                                ('Grade - XI', 'Grade - XI'),
                                                                ('Grade - XII', 'Grade - XII'),
                                                                ('none', 'none')), default = 'none')
    #Contact Information
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    #Other Details
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    aadhar_number = models.BigIntegerField()
    fee_status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name

class Announcement(models.Model):
    heading = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    date_and_time = models.DateTimeField()
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ["-date_and_time"]
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

class TeacherSchedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time = models.TimeField()
    monday = models.CharField(max_length=50)
    tuesday = models.CharField(max_length=50)
    wednesday = models.CharField(max_length=50)
    thursday = models.CharField(max_length=50)
    friday = models.CharField(max_length=50)

    def __str__(self):
        return self.teacher.user.first_name + " 's Schedule"


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

class LeaveRequest(models.Model):
    user = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=400)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.user.user.first_name

    class Meta:
        ordering = ["-date"]
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'

class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length = 10, choices = (('present', 'present'),('absent', 'absent')))
    marked_by = models.ForeignKey(Teacher, on_delete = models.CASCADE)

    def __str__(self):
        return self.student.user.first_name + " - " + str(self.date)

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length = 10, choices = (('present', 'present'),('absent', 'absent')))

    def __str__(self):
        return self.teacher.user.first_name + " - " + str(self.date)

class Subjects(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=20)
    taught_in_class = models.CharField(max_length = 30, choices = (('pre-nursery', 'pre-nursery'),
                                                                ('nursery', 'nursery'),
                                                                ('kinder-garten', 'kinder-garten'),
                                                                ('Grade - 1', 'Grade - 1'),
                                                                ('Grade - 2', 'Grade - 2'),
                                                                ('Grade - 3', 'Grade - 3'),
                                                                ('Grade - 4', 'Grade - 4'),
                                                                ('Grade - 5', 'Grade - 5'),
                                                                ('Grade - 6', 'Grade - 6'),
                                                                ('Grade - 7', 'Grade - 7'),
                                                                ('Grade - 8', 'Grade - 8'),
                                                                ('Grade - 9', 'Grade - 9'),
                                                                ('Grade - X', 'Grade - X'),
                                                                ('Grade - XI', 'Grade - XI'),
                                                                ('Grade - XII', 'Grade - XII'),
                                                                ('none', 'none')), default = 'none')
    def __str__(self):
        return self.name + ' - ' + self.taught_in_class

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=30, default='')
    exam_date = models.DateField(default='2000-01-1')
    marks_obtained = models.IntegerField(default = 0)
    total_marks = models.IntegerField(default = 0)
    uploaded_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    uploaded_on = models.DateField(default='2000-01-1')
    def __str__(self):
        return self.student.user.first_name

    class Meta:
        verbose_name = 'Marks'
        verbose_name_plural = 'Marks'

class ClassSchedule(models.Model):
    class_name = models.CharField(max_length = 30, choices = (('pre-nursery', 'pre-nursery'),
                                                                ('nursery', 'nursery'),
                                                                ('kinder-garten', 'kinder-garten'),
                                                                ('Grade - 1', 'Grade - 1'),
                                                                ('Grade - 2', 'Grade - 2'),
                                                                ('Grade - 3', 'Grade - 3'),
                                                                ('Grade - 4', 'Grade - 4'),
                                                                ('Grade - 5', 'Grade - 5'),
                                                                ('Grade - 6', 'Grade - 6'),
                                                                ('Grade - 7', 'Grade - 7'),
                                                                ('Grade - 8', 'Grade - 8'),
                                                                ('Grade - 9', 'Grade - 9'),
                                                                ('Grade - X', 'Grade - X'),
                                                                ('Grade - XI', 'Grade - XI'),
                                                                ('Grade - XII', 'Grade - XII'),
                                                                ('none', 'none')), default = 'none')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time = models.TimeField()
    monday = models.CharField(max_length=50)
    tuesday = models.CharField(max_length=50)
    wednesday = models.CharField(max_length=50)
    thursday = models.CharField(max_length=50)
    friday = models.CharField(max_length=50)

    def __str__(self):
        return self.class_name + " 's " + str(self.time)
