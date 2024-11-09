# forms.py
from django import forms
from .models import Ticker,LibraryInventory,FacultyCourseAssignment, CertificateType, CertificateApplication, LibraryMember,CourseMarks, LibraryFineCollection, BookIssued, Department, NewsNotice, Faculty, ImageGallery, VideoGallery, LibraryInventory, LibraryMember, Grievance, Feedback, RegisteredStudent,StreamCourse,AdmissionStat,FeeCollection,Slider
from django.core.exceptions import ValidationError
from django.db import transaction
from django import forms
from django.utils import timezone
from django import forms
from .models import Enquiry
from django.db import connection

# Library Inventory Forms
class AddInventoryForm(forms.ModelForm):
    class Meta:
        model = LibraryInventory
        fields = ['book_name', 'author', 'quantity', 'category']

class UpdateInventoryForm(forms.Form):
    book_id = forms.IntegerField(label="Book ID")
    new_book_name = forms.CharField(max_length=255, label="New Book Name")
    new_author = forms.CharField(max_length=255, label="New Author")
    new_quantity = forms.IntegerField(label="New Quantity")
    new_category = forms.CharField(max_length=255, label="New Category")

    def update_inventory(self):
        book_id = self.cleaned_data['book_id']
        new_book_name = self.cleaned_data['new_book_name']
        new_author = self.cleaned_data['new_author']
        new_quantity = self.cleaned_data['new_quantity']
        new_category = self.cleaned_data['new_category']
        
        book = LibraryInventory.objects.filter(id=book_id).first()
        if book:
            book.book_name = new_book_name
            book.author = new_author
            book.quantity = new_quantity
            book.category = new_category
            book.save()
            return True
        return False 

class DeleteInventoryForm(forms.Form):
    book_id = forms.IntegerField(label="Book ID")

    def delete_inventory(self):
        book_id = self.cleaned_data['book_id']
        book = LibraryInventory.objects.filter(id=book_id).first()
        if book:
            book.delete()
            return True
        return False  

# Library Member Forms
class AddMemberForm(forms.ModelForm):
    student_id = forms.IntegerField(label="Student ID")  

    class Meta:
        model = LibraryMember
        fields = ['membership_date'] 

    def save(self, commit=True):
        student_id = self.cleaned_data['student_id']
        student = RegisteredStudent.objects.get(id=student_id)
        self.instance.member = student  
        return super().save(commit=commit)

class UpdateMemberForm(forms.Form):
    member_id = forms.IntegerField(label="Member ID")
    updated_student_id = forms.IntegerField(label="Updated Student ID")
    updated_membership_date = forms.DateField(label="Updated Membership Date")

    def update_member(self):
        member_id = self.cleaned_data['member_id']
        updated_student_id = self.cleaned_data['updated_student_id']
        updated_membership_date = self.cleaned_data['updated_membership_date']
        
        # Fetch the existing LibraryMember instance
        member = LibraryMember.objects.filter(id=member_id).first()
        if member:
            # Update the member's attributes
            try:
                # Find the new student instance
                student = RegisteredStudent.objects.get(id=updated_student_id)
                member.student = student
                member.membership_date = updated_membership_date
                member.save()
                return True
            except RegisteredStudent.DoesNotExist:
                return False  # Student ID not found
        return False  # Member ID not found

class DeleteMemberForm(forms.Form):
    member_id = forms.IntegerField(label="Member ID")

    def delete_member(self):
        member_id = self.cleaned_data['member_id']
        member = LibraryMember.objects.filter(id=member_id).first()
        if member:
            member.delete()
            return True
        return False

# Fine Collection Forms
class AddFineForm(forms.Form):
    member_id = forms.IntegerField(label="Member ID")
    fine_amount = forms.DecimalField(label="Fine Amount", max_digits=10, decimal_places=2)
    date_paid = forms.DateField(label="Date Paid")

    def save_fine(self):
        member_id = self.cleaned_data['member_id']
        fine_amount = self.cleaned_data['fine_amount']
        date_paid = self.cleaned_data['date_paid']
        
        # Attempt to get the registered student by ID
        try:
            member = LibraryMember.objects.get(id=member_id)
            # Create and save the fine record with `member`
            fine_record = LibraryFineCollection(member=member, amount=fine_amount, date_paid=date_paid)
            fine_record.save()
            return True  # Successfully saved
        except LibraryMember.DoesNotExist:
            return False  # Member ID not found


class UpdateFineForm(forms.Form):
    fine_id = forms.IntegerField(label="Fine ID")
    new_fine_amount = forms.DecimalField(label="New Fine Amount", max_digits=10, decimal_places=2)
    new_date = forms.DateField(label="New Date")

    def update_fine(self):
        fine_id = self.cleaned_data['fine_id']
        new_fine_amount = self.cleaned_data['new_fine_amount']
        
        new_date = self.cleaned_data['new_date']

        # Attempt to get the fine record by ID
        try:
            fine_record = LibraryFineCollection.objects.get(id=fine_id)
            fine_record.amount = new_fine_amount
            fine_record.date_paid = new_date
            fine_record.save()
            return True  # Successfully updated
        except LibraryFineCollection.DoesNotExist:
            return False  # Fine ID not found
        
class DeleteFineForm(forms.Form):
    fine_id = forms.IntegerField(label="Fine ID")
    
    def delete_fine(self):
        fine_id = self.cleaned_data['fine_id']
        try:
            fine_record = LibraryFineCollection.objects.get(id=fine_id)
            fine_record.delete()
            return True  # Successfully deleted
        except LibraryFineCollection.DoesNotExist:
            return False  # Fine ID not found


class AddIssuedBookForm(forms.Form):
    book_id = forms.CharField(max_length=255, label="Book ID")
    student_id = forms.CharField(max_length=255, label="Student ID")
    issue_date = forms.DateField(label="Issue Date")
    return_date = forms.DateField(label="Return Date")

    def save_book(self):
        book_id = self.cleaned_data['book_id']
        student_id = self.cleaned_data['student_id']
        issue_date = self.cleaned_data['issue_date']
        return_date = self.cleaned_data['return_date']

        try:
            # Attempt to get the library member by student ID
            student = LibraryMember.objects.get(id=student_id)
            print("Student found:", student)
        except LibraryMember.DoesNotExist:
            print("Student ID not found.")
            return False, "Student ID not found in LibraryMember records."

        try:
            # Get the book from inventory
            book = LibraryInventory.objects.get(id=book_id)
            print("Book found:", book)
        except LibraryInventory.DoesNotExist:
            print("Book ID not found.")
            return False, "Book ID not found in inventory."

        # Check if there is sufficient quantity available
        if book.quantity < 1:
            print("Insufficient quantity to issue the book.")
            return False, "Insufficient quantity to issue the book."

        try:
            with transaction.atomic():  # Ensures atomic transaction for both operations
                # Print current quantity before decrementing
                print("Current book quantity:", book.quantity)

                # Decrement the quantity in inventory
                book.quantity -= 1
                book.save()

                # Print quantity after decrementing
                print("Book quantity after decrement:", book.quantity)

                # Use raw SQL to insert the issued book record
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO dbms_BookIssued (student_id, book_id, issue_date, return_date)
                        VALUES (%s, %s, %s, %s)
                        """,
                        [student.id, book.id, issue_date, return_date]
                    )
                    print("Issued book record inserted via raw SQL.")

                return True, "Book issued successfully."
        except Exception as e:
            print("Error during issuing:", e)
            return False, f"An error occurred: {str(e)}"


class UpdateBookIssuedForm(forms.Form):
    book_issue_id = forms.IntegerField(label="Book Issue ID")
    new_book_id = forms.IntegerField(label="New Book ID")

    def update_issued_book(self):
        book_issue_id = self.cleaned_data['book_issue_id']
        new_book_id = self.cleaned_data['new_book_id']
        
        try:
            # Retrieve the issued book record
            issued_book = BookIssued.objects.get(id=book_issue_id)
            
            # Get the current book and increment its quantity
            current_book = issued_book.book
            current_book.quantity += 1
            current_book.save()
            
            # Get the new book and check if it exists
            try:
                new_book = LibraryInventory.objects.get(id=new_book_id)
            except LibraryInventory.DoesNotExist:
                return False, "New Book ID not found in inventory."

            # Ensure there’s enough quantity to issue the new book
            if new_book.quantity < 1:
                return False, "Insufficient quantity to issue the new book."

            # Update the issued book record and quantity in an atomic transaction
            with transaction.atomic():
                # Use raw SQL to update the issued book record
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE dbms_BookIssued
                        SET book_id = %s
                        WHERE id = %s
                        """,
                        [new_book.id, book_issue_id]
                    )
                    print("Issued book record updated via raw SQL.")

                # Adjust quantities for both books
                new_book.quantity -= 1
                new_book.save()
                print("New book quantity updated.")

            return True, "Book issued record updated successfully."
        except BookIssued.DoesNotExist:
            return False, "Book Issue ID not found."


class DeleteBookIssuedForm(forms.Form):
    issued_id = forms.IntegerField(label="Issued ID")
    
    def delete_issued_book(self):
        issued_id = self.cleaned_data['issued_id']
        try:
            # Retrieve the issued book record
            issued_book_record = BookIssued.objects.get(id=issued_id)
            
            # Get the associated book from the issued record
            book = issued_book_record.book
            
            # Increment the quantity of the associated book
            book.quantity += 1
            book.save()
            
            # Now delete the issued book record
            issued_book_record.delete()
            return True  # Successfully deleted
        except BookIssued.DoesNotExist:
            return False  # Issued ID not found




# Stream Course Forms
class AddStreamCourseForm(forms.ModelForm):
    class Meta:
        model = StreamCourse
        fields = ['stream_name', 'course_name']

class UpdateStreamCourseForm(forms.Form):
    course_id = forms.IntegerField(label="Stream Course ID")
    new_stream_name = forms.CharField(max_length=255, label="Updated Stream Name")
    new_course_name = forms.CharField(max_length=255, label="Updated Course Name")

    def update_stream_course(self):
        course_id = self.cleaned_data['course_id']
        new_stream_name = self.cleaned_data['new_stream_name']
        new_course_name = self.cleaned_data['new_course_name']
        
        # Fetch the existing StreamCourse instance
        stream_course = StreamCourse.objects.filter(id=course_id).first()
        if stream_course:
            stream_course.stream_name = new_stream_name
            stream_course.course_name = new_course_name
            stream_course.save()
            return True
        return False  # Return False if the stream course ID is not found

class DeleteStreamCourseForm(forms.Form):
    course_id = forms.IntegerField(label="Course ID")

    def delete_course(self):
        course_id = self.cleaned_data['course_id']
        try:
            course = StreamCourse.objects.get(id=course_id)
            course.delete()
            return True
        except StreamCourse.DoesNotExist:
            return False


# Registered Student Forms
class AddStudentForm(forms.ModelForm):
    class Meta:
        model = RegisteredStudent
        fields = ['student_name', 'course', 'admission_date', 'fee_status']
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Override the course field to be a checkbox for each StreamCourse
    course = forms.ModelMultipleChoiceField(
        queryset=StreamCourse.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )


from django import forms
from .models import RegisteredStudent, StreamCourse

class UpdateStudentForm(forms.Form):
    student_id = forms.IntegerField(label="Student ID")
    new_student_name = forms.CharField(max_length=255, label="New Student Name")
    new_courses = forms.ModelMultipleChoiceField(
        queryset=StreamCourse.objects.all(),
        label="New Courses",
        widget=forms.CheckboxSelectMultiple
    )
    new_admission_date = forms.DateField(label="New Admission Date", widget=forms.SelectDateWidget)
    new_fee_status = forms.ChoiceField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], label="New Fee Status")

    def update_student(self):
        student_id = self.cleaned_data['student_id']
        new_student_name = self.cleaned_data['new_student_name']
        new_courses = self.cleaned_data['new_courses']
        new_admission_date = self.cleaned_data['new_admission_date']
        new_fee_status = self.cleaned_data['new_fee_status']
        
        # Fetch the existing RegisteredStudent instance
        student = RegisteredStudent.objects.filter(id=student_id).first()
        if student:
            student.student_name = new_student_name
            student.admission_date = new_admission_date
            student.fee_status = new_fee_status
            student.save()
            
            # Update the courses for the many-to-many relationship
            student.course.set(new_courses)
            
            return True
        return False  # Return False if the student ID is not found



class DeleteStudentForm(forms.Form):
    student_id = forms.IntegerField(label="Student ID")

    def delete_student(self):
        student_id = self.cleaned_data['student_id']
        try:
            student = RegisteredStudent.objects.get(id=student_id)
            student.delete()
            return True
        except RegisteredStudent.DoesNotExist:
            return False


# Marks Form





from django import forms
from .models import CourseMarks, FacultyCourseAssignment, RegisteredStudent, StreamCourse
from django.core.exceptions import ValidationError

class AddMarksForm(forms.ModelForm):
    student_id = forms.IntegerField(
        label="Student ID", 
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CourseMarks
        fields = ['course', 'marks']  # Exclude 'faculty' since it will be set automatically

    def __init__(self, *args, **kwargs):
        # Capture the faculty parameter passed from the view
        faculty = kwargs.pop('faculty', None)
        super(AddMarksForm, self).__init__(*args, **kwargs)

        # Filter courses based on the logged-in faculty’s assigned courses
        if faculty:
            assigned_courses = FacultyCourseAssignment.objects.filter(faculty=faculty).values_list('course', flat=True)
            self.fields['course'].queryset = StreamCourse.objects.filter(id__in=assigned_courses)
        
        # Update field attributes
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['marks'].widget.attrs.update({'class': 'form-control'})

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        try:
            # Ensure student exists
            student = RegisteredStudent.objects.get(id=student_id)
            self.cleaned_data['student'] = student  # Store student instance in cleaned data
        except RegisteredStudent.DoesNotExist:
            raise ValidationError("Student with this ID does not exist.")
        return student_id

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.student = self.cleaned_data.get('student')
        if commit:
            instance.save()
        return instance




class UpdateMarksForm(forms.Form):
    marks_id = forms.IntegerField(
        label="Marks ID", 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Marks ID'}),
        required=True
    )
    marks = forms.DecimalField(
        label="Marks", 
        max_digits=5, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Marks'}),
        required=True
    )
    course = forms.ModelChoiceField(
        queryset=None,  # To be set in __init__
        label="Course",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = CourseMarks
        fields = ['marks_id', 'course', 'marks']

    def __init__(self, *args, **kwargs):
        faculty = kwargs.pop('faculty', None)  # Expecting a faculty instance to be passed in
        super(UpdateMarksForm, self).__init__(*args, **kwargs)

        # Filter courses by the ones assigned to the faculty
        if faculty:
            assigned_courses = FacultyCourseAssignment.objects.filter(faculty=faculty).values_list('course', flat=True)
            self.fields['course'].queryset = StreamCourse.objects.filter(id__in=assigned_courses)

        # Add CSS classes
        self.fields['marks'].widget.attrs.update({'class': 'form-control'})

    def update_marks(self):
        # Get the cleaned data from the form
        marks_id = self.cleaned_data.get('marks_id')
        marks = self.cleaned_data.get('marks')
        course = self.cleaned_data.get('course')

        # Try to find the CourseMarks object
        try:
            course_marks = CourseMarks.objects.get(id=marks_id)
        except CourseMarks.DoesNotExist:
            self.add_error('marks_id', "Marks ID not found.")
            return False

        # Update the course marks record
        course_marks.marks = marks
        course_marks.course = course
        course_marks.save()

        return True
from django import forms
from .models import CourseMarks

class DeleteMarksForm(forms.Form):
    marks_id = forms.IntegerField(
        label="Marks ID", 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Marks ID'}),
        required=True
    )

    class Meta:
        model = CourseMarks
        fields = ['marks_id']

    def delete_marks(self):
        # Get the cleaned data from the form
        marks_id = self.cleaned_data.get('marks_id')

        # Try to find the CourseMarks object
        try:
            course_marks = CourseMarks.objects.get(id=marks_id)
        except CourseMarks.DoesNotExist:
            self.add_error('marks_id', "Marks ID not found.")
            return False

        # Delete the CourseMarks record
        course_marks.delete()

        return True


from django import forms
from .models import Faculty, StreamCourse, FacultyCourseAssignment

class AddFacultyCourseAssignmentForm(forms.ModelForm):
    faculty_id = forms.IntegerField(label="Faculty ID")
    course_id = forms.IntegerField(label="Course ID")

    class Meta:
        model = FacultyCourseAssignment
        fields = []  # Keep fields empty to handle them manually

    def save(self, commit=True):
        faculty_id = self.cleaned_data['faculty_id']
        course_id = self.cleaned_data['course_id']

        try:
            # Fetch the related instances
            faculty = Faculty.objects.get(id=faculty_id)
            course = StreamCourse.objects.get(id=course_id)

            # Create a new FacultyCourseAssignment instance and assign values
            assignment = FacultyCourseAssignment(faculty=faculty, course=course)
            if commit:
                assignment.save()
            return assignment
        except Faculty.DoesNotExist:
            raise forms.ValidationError("Invalid Faculty ID provided.")
        except StreamCourse.DoesNotExist:
            raise forms.ValidationError("Invalid Course ID provided.")

class UpdateFacultyCourseAssignmentForm(forms.Form):
    assignment_id = forms.IntegerField(label="Assignment ID")
    updated_faculty_id = forms.IntegerField(label="Updated Faculty ID")
    updated_course_id = forms.IntegerField(label="Updated Course ID")

    def update_assignment(self):
        assignment_id = self.cleaned_data.get('assignment_id')
        updated_faculty_id = self.cleaned_data.get('updated_faculty_id')
        updated_course_id = self.cleaned_data.get('updated_course_id')

        # Find the assignment by ID
        assignment = FacultyCourseAssignment.objects.filter(id=assignment_id).first()
        if not assignment:
            self.add_error('assignment_id', "Assignment ID not found.")
            return False

        # Fetch updated faculty and course objects with error handling
        try:
            faculty = Faculty.objects.get(id=updated_faculty_id)
        except Faculty.DoesNotExist:
            self.add_error('updated_faculty_id', "Invalid Faculty ID provided.")
            return False

        try:
            course = StreamCourse.objects.get(id=updated_course_id)
        except StreamCourse.DoesNotExist:
            self.add_error('updated_course_id', "Invalid Course ID provided.")
            return False

        # Update the assignment with the fetched faculty and course
        assignment.faculty = faculty
        assignment.course = course
        assignment.save()
        return True

# Delete FacultyCourseAssignment Form
class DeleteFacultyCourseAssignmentForm(forms.Form):
    assignment_id = forms.IntegerField(label="Assignment ID")

    def delete_assignment(self):
        assignment_id = self.cleaned_data.get('assignment_id')
        # Check if the assignment exists and delete it if found
        assignment = FacultyCourseAssignment.objects.filter(id=assignment_id).first()
        if assignment:
            assignment.delete()
            return True
        else:
            self.add_error('assignment_id', "Assignment with the provided ID does not exist.")
            return False


# Admission Stat Forms
class AddAdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionStat
        fields = ['year', 'total_admissions', 'course']

class UpdateAdmissionForm(forms.Form):
    admission_id = forms.IntegerField(label="Admission ID")
    updated_year = forms.IntegerField(label="Updated Year")
    updated_total_admissions = forms.IntegerField(label="Updated Total Admissions")
    updated_course = forms.ModelChoiceField(queryset=StreamCourse.objects.all(), label="New Course")

    def update_admission(self):
        admission_id = self.cleaned_data['admission_id']
        updated_year = self.cleaned_data['updated_year']
        updated_total_admissions = self.cleaned_data['updated_total_admissions']
        updated_course = self.cleaned_data['updated_course']
        
        # Fetch the existing AdmissionStat instance
        admission = AdmissionStat.objects.filter(id=admission_id).first()
        if admission:
            admission.year = updated_year
            admission.total_admissions = updated_total_admissions
            admission.course = updated_course
            admission.save()
            return True
        return False  # Return False if the admission ID is not found

class DeleteAdmissionForm(forms.Form):
    admission_id = forms.IntegerField(label="admission_id")

    def delete_stat(self):
        admission_id = self.cleaned_data['admission_id']
        try:
            stat = AdmissionStat.objects.get(id=admission_id)
            stat.delete()
            return True
        except AdmissionStat.DoesNotExist:
            return False


# Fee Collection Forms
class AddFeeForm(forms.ModelForm):
    class Meta:
        model = FeeCollection 
        fields = ['student', 'amount', 'date_paid']

    
class UpdateFeeForm(forms.Form):
    fee_id = forms.IntegerField(label="fee ID")
    new_student_id = forms.IntegerField(label="New Student ID")  # Change to IntegerField
    new_amount = forms.DecimalField(max_digits=10, decimal_places=2, label="New Amount")
    new_date_paid = forms.DateField(label="New Date Paid")

    def update_fee(self):
        fee_id = self.cleaned_data.get('fee_id')
        new_student_id = self.cleaned_data.get('new_student_id')  # Use the student ID directly
        new_amount = self.cleaned_data.get('new_amount')
        new_date_paid = self.cleaned_data.get('new_date_paid')

        try:
            # Try to retrieve the FeeCollection instance
            fee = FeeCollection.objects.get(id=fee_id)

            new_student = RegisteredStudent.objects.get(id=new_student_id)  

            fee.student = new_student
            fee.amount = new_amount
            fee.date_paid = new_date_paid
            fee.save()
            return True
        except FeeCollection.DoesNotExist:
            return False
        except RegisteredStudent.DoesNotExist:
            return False  

class DeleteFeeForm(forms.Form):
    fee_id = forms.IntegerField(label="fee_id")

    def delete_stat(self):
        fee_id = self.cleaned_data['fee_id']
        try:
            stat = FeeCollection.objects.get(id=fee_id)
            stat.delete()
            return True
        except FeeCollection.DoesNotExist:
            return False


# News and Notices Management
class AddNewsNoticeForm(forms.ModelForm):
    class Meta:
        model = NewsNotice
        fields = ['title', 'content', 'date_posted', 'posted_by']

class UpdateNewsNoticeForm(forms.Form):
    notice_id = forms.IntegerField(label="Notice ID")
    new_title = forms.CharField(max_length=255, label="New Title")
    new_content = forms.CharField(widget=forms.Textarea, label="New Content")
    new_date_posted = forms.DateField(widget=forms.SelectDateWidget, label="New Date Posted")
    new_posted_by = forms.CharField(max_length=100, label="New Posted By")

    def update_notice(self):
        notice_id = self.cleaned_data['notice_id']
        new_title = self.cleaned_data['new_title']
        new_content = self.cleaned_data['new_content']
        new_date_posted = self.cleaned_data['new_date_posted']
        new_posted_by = self.cleaned_data['new_posted_by']
        
        notice = NewsNotice.objects.filter(id=notice_id).first()
        if notice:
            notice.title = new_title
            notice.content = new_content
            notice.date_posted = new_date_posted
            notice.posted_by = new_posted_by
            notice.save()
            return True
        return False

class DeleteNewsNoticeForm(forms.Form):
    notice_id = forms.IntegerField(label="Notice ID")

    def delete_notice(self):
        notice_id = self.cleaned_data['notice_id']
        try:
            notice = NewsNotice.objects.get(id=notice_id)
            notice.delete()
            return True
        except NewsNotice.DoesNotExist:
            return False 

class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class UpdateDepartmentForm(forms.Form):
    department_id = forms.IntegerField(label="Department ID")
    new_name = forms.CharField(max_length=255, label="New Name")
    new_description = forms.CharField(required=False, label="New Description")

    def update_department(self):
        department_id = self.cleaned_data['department_id']
        new_name = self.cleaned_data['new_name']
        new_description = self.cleaned_data['new_description']
        
        department = Department.objects.filter(id=department_id).first()
        if department:
            department.name = new_name
            department.description = new_description
            department.save()
            return True
        return False 

class DeleteDepartmentForm(forms.Form):
    department_id = forms.IntegerField(label="Department ID")

    def delete_department(self):
        department_id = self.cleaned_data['department_id']
        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            return True
        except Department.DoesNotExist:
            return False 

class AddSliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['image_url', 'caption', 'order'] 

class UpdateSliderForm(forms.Form):
    slider_id = forms.IntegerField(label="Slider ID")
    new_image_url = forms.CharField(max_length=255, label="New Image URL")
    new_caption = forms.CharField(max_length=255, label="New Caption")
    new_order = forms.IntegerField(label="New Order")

    def update_slider(self):
        slider_id = self.cleaned_data['slider_id']
        new_image_url = self.cleaned_data['new_image_url']
        new_caption = self.cleaned_data['new_caption']
        new_order = self.cleaned_data['new_order']
        
        slider = Slider.objects.filter(id=slider_id).first()
        if slider:
            slider.image_url = new_image_url
            slider.caption = new_caption
            slider.order = new_order
            slider.save()
            return True
        return False  

class DeleteSliderForm(forms.Form):
    slider_id = forms.IntegerField(label="Slider ID")

    def delete_slider(self):
        slider_id = self.cleaned_data['slider_id']
        try:
            slider = Slider.objects.get(id=slider_id)
            slider.delete()
            return True
        except Slider.DoesNotExist:
            return False  
class AddTickerForm(forms.ModelForm):
    class Meta:
        model = Ticker
        fields = ['message', 'date_created']  

class UpdateTickerForm(forms.Form):
    ticker_id = forms.IntegerField(label="Ticker ID")
    new_message = forms.CharField(max_length=255, label="New Message")
    new_date = forms.DateField(widget=forms.SelectDateWidget, label="New Date")

    def update_ticker(self):
        ticker_id = self.cleaned_data['ticker_id']
        new_message = self.cleaned_data['new_message']
        new_date = self.cleaned_data['new_date']
        
        ticker = Ticker.objects.filter(id=ticker_id).first()
        if ticker:
            ticker.message = new_message
            ticker.date_created = new_date
            ticker.save()
            return True
        return False 

class DeleteTickerForm(forms.Form):
    ticker_id = forms.IntegerField(label="Ticker ID")

    def delete_ticker(self):
        ticker_id = self.cleaned_data['ticker_id']
        try:
            ticker = Ticker.objects.get(id=ticker_id)
            ticker.delete()
            return True
        except Ticker.DoesNotExist:
            return False 

class AddImageForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = ['image_url', 'caption', 'uploaded_by']

class UpdateImageForm(forms.Form):
    image_id = forms.IntegerField(label="Image ID")
    new_image_url = forms.CharField(max_length=255, required=False, label="New Image URL")
    new_caption = forms.CharField(max_length=255, required=False, label="New Caption")
    new_uploaded_by = forms.CharField(max_length=255, required=False, label="New Uploaded By")
    def update_image(self):
        image_id = self.cleaned_data['image_id']
        new_image_url = self.cleaned_data.get('new_image_url')
        new_caption = self.cleaned_data.get('new_caption')
        new_uploaded_by = self.cleaned_data.get('new_uploaded_by')
        image = ImageGallery.objects.filter(id=image_id).first()
        if image:
            if new_image_url:
                image.image_url = new_image_url
            if new_caption:
                image.caption = new_caption
            if new_uploaded_by:
                image.uploaded_by = new_uploaded_by    
            image.save()
            return True
        return False  

class DeleteImageForm(forms.Form):
    image_id = forms.IntegerField()

    def delete_image(self):
        image_id = self.cleaned_data['image_id']
        try:
            image = ImageGallery.objects.get(id=image_id)
            image.delete()
            return True
        except ImageGallery.DoesNotExist:
            return False

class AddVideoForm(forms.ModelForm):
    class Meta:
        model = VideoGallery
        fields = ['video_url', 'description', 'uploaded_by']

class UpdateVideoForm(forms.Form):
    video_id = forms.IntegerField()
    new_video_url = forms.CharField(max_length=255)
    new_description = forms.CharField(widget=forms.Textarea)
    new_uploaded_by = forms.CharField(max_length=100)

    def update_video(self):
        video_id = self.cleaned_data['video_id']
        try:
            video = VideoGallery.objects.get(id=video_id)
            video.video_url = self.cleaned_data['new_video_url']
            video.description = self.cleaned_data['new_description']
            video.uploaded_by = self.cleaned_data['new_uploaded_by']
            video.save()
            return True
        except VideoGallery.DoesNotExist:
            return False

class DeleteVideoForm(forms.Form):
    video_id = forms.IntegerField()

    def delete_video(self):
        video_id = self.cleaned_data['video_id']
        try:
            video = VideoGallery.objects.get(id=video_id)
            video.delete()
            return True
        except VideoGallery.DoesNotExist:
            return False


class AddFacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'designation', 'department', 'contact', 'photo_url']

class UpdateFacultyForm(forms.Form):
    faculty_id = forms.IntegerField()
    new_name = forms.CharField(max_length=255)
    new_designation = forms.CharField(max_length=255)
    new_department = forms.ModelChoiceField(queryset=Department.objects.all()) 
    new_contact = forms.CharField(max_length=100)
    new_photo_url = forms.CharField(max_length=255)

    def update_faculty(self):
        faculty_id = self.cleaned_data['faculty_id']
        try:
            faculty = Faculty.objects.get(id=faculty_id)
            faculty.name = self.cleaned_data['new_name']
            faculty.designation = self.cleaned_data['new_designation']
            faculty.department = self.cleaned_data['new_department']
            faculty.contact = self.cleaned_data['new_contact']
            faculty.photo_url = self.cleaned_data['new_photo_url']
            faculty.save()
            return True
        except Faculty.DoesNotExist:
            return False

class DeleteFacultyForm(forms.Form):
    faculty_id = forms.IntegerField()

    def delete_faculty(self):
        faculty_id = self.cleaned_data['faculty_id']
        try:
            faculty = Faculty.objects.get(id=faculty_id)
            faculty.delete()
            return True
        except Faculty.DoesNotExist:
            return False
        
class AddCertificateForm(forms.ModelForm):
    class Meta:
        model = CertificateType
        fields = ['certificate_name', 'fee']
        widgets = {
            'certificate_name': forms.TextInput(attrs={'placeholder': 'Certificate Name'}),
            'fee': forms.NumberInput(attrs={'placeholder': 'Fee', 'step': '0.01'}),
        }

class UpdateCertificateForm(forms.Form):
    certificate_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Certificate ID'}))
    new_certificate_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'New Certificate Name'}))
    new_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'New Fee', 'step': '0.01'}))

    def update_certificate(self):
        certificate_id = self.cleaned_data['certificate_id']
        new_certificate_name = self.cleaned_data['new_certificate_name']
        new_fee = self.cleaned_data['new_fee']

        try:
            certificate = CertificateType.objects.get(id=certificate_id)
            certificate.certificate_name = new_certificate_name
            certificate.fee = new_fee
            certificate.save()
            return True
        except CertificateType.DoesNotExist:
            return False

class DeleteCertificateForm(forms.Form):
    certificate_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Certificate ID'}))

    def delete_certificate(self):
        certificate_id = self.cleaned_data['certificate_id']

        try:
            certificate = CertificateType.objects.get(id=certificate_id)
            certificate.delete()
            return True
        except CertificateType.DoesNotExist:
            return False


class AddCertificateApplicationForm(forms.ModelForm):
    class Meta:
        model = CertificateApplication
        fields = ['student', 'certificate', 'status', 'application_date']

class UpdateCertificateApplicationForm(forms.Form):
    application_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Application ID'}))
    updated_student_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'New Student ID'}))
    updated_certificate = forms.ModelChoiceField(queryset=CertificateType.objects.all(),
                                                 required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    updated_status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
                                        required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    updated_application_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    updated_issued_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def update_certificate_application(self):
        application_id = self.cleaned_data['application_id']
        updated_student_id = self.cleaned_data['updated_student_id']
        updated_certificate = self.cleaned_data['updated_certificate']
        updated_status = self.cleaned_data['updated_status']
        updated_application_date = self.cleaned_data['updated_application_date']
        updated_issued_date = self.cleaned_data['updated_issued_date']

        try:
            # Retrieve the existing application
            application = CertificateApplication.objects.get(id=application_id)
            # Update fields
            application.student_id = updated_student_id  # Assign the student ID directly
            application.certificate = updated_certificate
            application.status = updated_status
            application.application_date = updated_application_date
            application.issued_date = updated_issued_date
            application.save()
            return True
        except CertificateApplication.DoesNotExist:
            return False

class DeleteCertificateApplicationForm(forms.Form):
    application_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Application ID'}))

    def delete_certificate_application(self):
        application_id = self.cleaned_data['application_id']

        try:
            application = CertificateApplication.objects.get(id=application_id)
            application.delete()
            return True
        except CertificateApplication.DoesNotExist:
            return False

class AddGrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['student', 'grievance_type', 'description', 'status', 'submitted_date']

class UpdateGrievanceForm(forms.Form):
    grievance_id = forms.IntegerField()
    new_student_id = forms.IntegerField()
    new_grievance_type = forms.CharField(max_length=255)
    new_description = forms.CharField(widget=forms.Textarea)
    new_status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected')])
    new_resolved_date = forms.DateField(required=False)

    def update_grievance(self):
        grievance_id = self.cleaned_data['grievance_id']
        try:
            grievance = Grievance.objects.get(id=grievance_id)

            # Validate the new student ID
            new_student_id = self.cleaned_data['new_student_id']
            try:
                # Ensure that the new student exists
                grievance.student = RegisteredStudent.objects.get(id=new_student_id)
            except RegisteredStudent.DoesNotExist:
                return False  # New student ID is invalid

            grievance.grievance_type = self.cleaned_data['new_grievance_type']
            grievance.description = self.cleaned_data['new_description']
            grievance.status = self.cleaned_data['new_status']
            grievance.resolved_date = self.cleaned_data.get('new_resolved_date', None)
            grievance.save()
            return True
        except Grievance.DoesNotExist:
            return False


class DeleteGrievanceForm(forms.Form):
    grievance_id = forms.IntegerField()

    def delete_grievance(self):
        grievance_id = self.cleaned_data['grievance_id']
        try:
            grievance = Grievance.objects.get(id=grievance_id)
            grievance.delete()
            return True
        except Grievance.DoesNotExist:
            return False

class AddFeedbackForm(forms.Form):
    student_id = forms.IntegerField()
    faculty_id = forms.IntegerField()  # New field for faculty ID
    feedback_text = forms.CharField(widget=forms.Textarea)
    submitted_date = forms.DateField()

    def save(self):
        student_id = self.cleaned_data['student_id']
        faculty_id = self.cleaned_data['faculty_id']  # Retrieve faculty_id from cleaned_data

        try:
            student = RegisteredStudent.objects.get(id=student_id)
            faculty = Faculty.objects.get(id=faculty_id)  # Retrieve Faculty instance by ID

            feedback = Feedback(
                student=student,
                faculty=faculty,  # Set the faculty field
                feedback_text=self.cleaned_data['feedback_text'],
                submitted_date=self.cleaned_data['submitted_date']
            )
            feedback.save()
            return True
        except (RegisteredStudent.DoesNotExist, Faculty.DoesNotExist):
            return False


class UpdateFeedbackForm(forms.Form):
    feedback_id = forms.IntegerField()
    new_student_id = forms.IntegerField()
    updated_feedback_text = forms.CharField(widget=forms.Textarea)
    updated_submitted_date = forms.DateField()

    def update_feedback(self):
        feedback_id = self.cleaned_data['feedback_id']
        try:
            feedback = Feedback.objects.get(id=feedback_id)

            # Validate the new student ID
            new_student_id = self.cleaned_data['new_student_id']
            try:
                # Ensure that the new student exists
                feedback.student = RegisteredStudent.objects.get(id=new_student_id)
            except RegisteredStudent.DoesNotExist:
                return False  # New student ID is invalid

            feedback.feedback_text = self.cleaned_data['updated_feedback_text']
            feedback.submitted_date = self.cleaned_data['updated_submitted_date']
            feedback.save()
            return True
        except Feedback.DoesNotExist:
            return False

class DeleteFeedbackForm(forms.Form):
    feedback_id = forms.IntegerField()

    def delete_feedback(self):
        feedback_id = self.cleaned_data['feedback_id']
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.delete()
            return True
        except Feedback.DoesNotExist:
            return False

class AddEnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['student_name', 'enquiry_text', 'submitted_date']

class UpdateEnquiryForm(forms.Form):
    enquiry_id = forms.IntegerField()
    new_student_name = forms.CharField(max_length=255)
    updated_enquiry_text = forms.CharField(widget=forms.Textarea)
    new_submitted_date = forms.DateField(required=False)

    def update_enquiry(self):
        enquiry_id = self.cleaned_data['enquiry_id']
        try:
            enquiry = Enquiry.objects.get(id=enquiry_id)
            enquiry.student_name = self.cleaned_data['new_student_name']
            enquiry.enquiry_text = self.cleaned_data['updated_enquiry_text']
            enquiry.submitted_date = self.cleaned_data.get('new_submitted_date', enquiry.submitted_date)
            enquiry.save()
            return True
        except Enquiry.DoesNotExist:
            return False

class DeleteEnquiryForm(forms.Form):
    enquiry_id = forms.IntegerField()

    def delete_enquiry(self):
        enquiry_id = self.cleaned_data['enquiry_id']
        try:
            enquiry = Enquiry.objects.get(id=enquiry_id)
            enquiry.delete()
            return True
        except Enquiry.DoesNotExist:
            return False

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class NewsNoticeForm(forms.ModelForm):
    class Meta:
        model = NewsNotice
        fields = '__all__'

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'

class ImageGalleryForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = '__all__'

class VideoGalleryForm(forms.ModelForm):
    class Meta:
        model = VideoGallery
        fields = '__all__'

class LibraryInventoryForm(forms.ModelForm):
    class Meta:
        model = LibraryInventory
        fields = '__all__'

class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = '__all__'

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'