from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    faculty_id = models.IntegerField(null=True, blank=True)  # Only for faculty
    student_id = models.IntegerField(null=True, blank=True)  # Only for students

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class NewsNotice(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateField()
    posted_by = models.CharField(max_length=100) 

    def __str__(self):
        return self.title
    
class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return self.caption

class Ticker(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=255)
    date_created = models.DateField()

    def __str__(self):
        return self.message

class ImageGallery(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

class VideoGallery(models.Model):
    id = models.AutoField(primary_key=True)
    video_url = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)  # FK to department
    contact = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class StreamCourse(models.Model):
    id = models.AutoField(primary_key=True)
    stream_name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name 

class RegisteredStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255)
    course = models.ManyToManyField(StreamCourse)  # FK to StreamCourse
    admission_date = models.DateField()
    fee_status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])

    def __str__(self):
        return self.student_name
    
class FacultyCourseAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(StreamCourse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty.name} - {self.course.course_name}"

class CourseMarks(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(RegisteredStudent, on_delete=models.CASCADE)  # FK to RegisteredStudent
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)  # FK to Faculty
    course = models.ForeignKey(StreamCourse, on_delete=models.CASCADE)  # FK to StreamCourse
    marks = models.DecimalField(max_digits=5, decimal_places=2)  # Marks with up to two decimal points

    def save(self, *args, **kwargs):
        # Validate that the faculty is assigned to the course
        if not FacultyCourseAssignment.objects.filter(faculty=self.faculty, course=self.course).exists():
            raise ValidationError("The specified faculty is not assigned to the specified course.")

        # Validate that the student's course includes the specified course
        if not self.student.course.filter(id=self.course.id).exists():
            raise ValidationError("The student's course must match the specified course in CourseMarks.")

        super().save(*args, **kwargs)  # Call the original save method

    def _str_(self):
        return f"{self.student.student_name} - {self.course.course_name} - {self.marks}"


class AdmissionStat(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    total_admissions = models.IntegerField()
    course = models.ForeignKey(StreamCourse, on_delete=models.CASCADE)  # FK to StreamCourse

    def __str__(self):
        return self.course

class FeeCollection(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(RegisteredStudent, on_delete=models.CASCADE)  # FK to RegisteredStudent
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()

    def __str__(self):
        return str(self.student)

class CertificateType(models.Model):
    id = models.AutoField(primary_key=True)
    certificate_name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.certificate_name

class CertificateApplication(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(RegisteredStudent, on_delete=models.CASCADE)  # FK to RegisteredStudent
    certificate = models.ForeignKey(CertificateType, on_delete=models.CASCADE)  # FK to CertificateType
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    application_date = models.DateField()
    issued_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.student)

class LibraryInventory(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    quantity = models.IntegerField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.book_name

class LibraryMember(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(RegisteredStudent, on_delete=models.CASCADE)  # FK to RegisteredStudent
    membership_date = models.DateField()

    def __str__(self):
        return str(self.student)

class LibraryFineCollection(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(LibraryMember, on_delete=models.CASCADE)  # FK to RegisteredStudent
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()

    def __str__(self):
        return str(self.member_id)

class BookIssued(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(LibraryInventory, on_delete=models.PROTECT)  # FK to LibraryInventory
    student = models.ForeignKey(LibraryMember, on_delete=models.CASCADE)  # FK to LibraryMember
    issue_date = models.DateField()
    return_date = models.DateField()
    
    def save(self, *args, **kwargs):
        # Check if the book has sufficient quantity
        if self.book.quantity <= 0:
            raise ValidationError("Cannot issue book: insufficient quantity available.")

        # Decrement the quantity in LibraryInventory, but do not delete
        self.book.quantity -= 1
        self.book.save()  # Only save the updated quantity to the database

        super().save(*args, **kwargs)  # Call the original save method
        
    def __str__(self):
        return str(self.student)

class Grievance(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(RegisteredStudent, on_delete=models.CASCADE)  # FK to RegisteredStudent
    grievance_type = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected')])
    submitted_date = models.DateField()
    resolved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.student)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(RegisteredStudent, on_delete=models.CASCADE)  # FK to RegisteredStudent
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)  # FK to Faculty
    feedback_text = models.TextField()
    submitted_date = models.DateField()

    def __str__(self):
        return str(self.student)

class Enquiry(models.Model):
    id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255)
    enquiry_text = models.TextField()
    submitted_date = models.DateField()

    def __str__(self):
        return self.student_name