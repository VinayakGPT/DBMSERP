# forms.py
from django import forms
from .models import LibraryInventory, LibraryMember, LibraryFineCollection, BookIssued, Department, NewsNotice, Faculty, ImageGallery, VideoGallery, LibraryInventory, LibraryMember, Grievance, Feedback, ContactUs, RegisteredStudent, Student, Admission, StreamCourse, FeeCollection
from django.core.exceptions import ValidationError


# Student Forms
class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'fee_status',        # This should match the actual fields in the Student model
            'student_name',      # Ensure these fields exist in the model
            'course',
            'admission_date',
        ]


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'course', 'admission_date', 'fee_status']

class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'new_student_name', 'new_course', 'new_admission_date', 'new_fee_status']

class DeleteStudentForm(forms.Form):
    student_id = forms.CharField(max_length=20)

# Admission Forms
class AddAdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['year', 'total_admissions', 'course']

class UpdateAdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['admission_id', 'updated_year', 'updated_total_admissions', 'updated_course']

class DeleteAdmissionForm(forms.Form):
    admission_id = forms.IntegerField()

# Stream Course Forms
class AddCourseForm(forms.ModelForm):
    class Meta:
        model = StreamCourse
        fields = ['stream_name', 'course_name']

class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = StreamCourse
        fields = ['course_id', 'new_stream_name', 'new_course_name']

class DeleteCourseForm(forms.Form):
    course_id = forms.CharField(max_length=20)

# Fee Collection Forms
class AddFeeForm(forms.ModelForm):
    class Meta:
        model = FeeCollection
        fields = ['student_id', 'amount', 'date_paid']

class UpdateFeeForm(forms.ModelForm):
    class Meta:
        model = FeeCollection
        fields = ['fee_id', 'new_amount', 'new_date_paid']

class DeleteFeeForm(forms.Form):
    fee_id = forms.CharField(max_length=20)





# Form for StreamCourse
class StreamCourseForm(forms.ModelForm):
    class Meta:
        model = StreamCourse
        fields = ['stream_name', 'course_name']

# Form for RegisteredStudent
class RegisteredStudentForm(forms.ModelForm):
    class Meta:
        model = RegisteredStudent
        fields = ['student_name', 'course_id', 'admission_date', 'fee_status']

# Form for AdmissionStats
class AdmissionStatsForm(forms.ModelForm):
    class Meta:
        model = AdmissionStats
        fields = ['year', 'total_admissions', 'course_id']

# Form for FeeCollection
class FeeCollectionForm(forms.ModelForm):
    class Meta:
        model = FeeCollection
        fields = ['student_id', 'amount', 'date_paid']




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
        
        # Fetch the existing LibraryInventory instance
        book = LibraryInventory.objects.filter(id=book_id).first()
        if book:
            book.book_name = new_book_name
            book.author = new_author
            book.quantity = new_quantity
            book.category = new_category
            book.save()
            return True
        return False  # Return False if the book ID is not found

class DeleteInventoryForm(forms.Form):
    book_id = forms.IntegerField(label="Book ID")

    def delete_inventory(self):
        book_id = self.cleaned_data['book_id']
        # Attempt to delete the LibraryInventory instance
        book = LibraryInventory.objects.filter(id=book_id).first()
        if book:
            book.delete()
            return True
        return False  # Return False if the book ID is not found

# Library Member Forms
class AddMemberForm(forms.ModelForm):
    student_id = forms.IntegerField(label="Student ID")  # Define the student ID as a form field

    class Meta:
        model = LibraryMember
        fields = ['membership_date']  # Exclude 'student' from the form fields

    def save(self, commit=True):
        student_id = self.cleaned_data['student_id']
        student = RegisteredStudent.objects.get(id=student_id)
        self.instance.student = student  # Set the student instance
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
    student_id = forms.IntegerField(label="Student ID")
    fine_amount = forms.DecimalField(label="Fine Amount", max_digits=10, decimal_places=2)
    date_paid = forms.DateField(label="Date Paid")

    def save_fine(self):
        student_id = self.cleaned_data['student_id']
        fine_amount = self.cleaned_data['fine_amount']
        date_paid = self.cleaned_data['date_paid']
        
        # Attempt to get the registered student by ID
        try:
            student = RegisteredStudent.objects.get(id=student_id)
            # Create and save the fine record (assume you have a LibraryFineCollection model)
            fine_record = LibraryFineCollection(student=student, amount=fine_amount, date_paid=date_paid)
            fine_record.save()
            return True  # Successfully saved
        except RegisteredStudent.DoesNotExist:
            return False  # Student ID not found

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

class AddIssuedBookForm(forms.ModelForm):
    book_id = forms.CharField(max_length=255, label="Book ID")
    student_id = forms.CharField(max_length=255, label="Student ID")

    class Meta:
        model = BookIssued
        fields = ['issue_date', 'return_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        book_id = cleaned_data.get('book_id')
        student_id = cleaned_data.get('student_id')

        # Validate book and student IDs
        try:
            book = LibraryInventory.objects.get(id=book_id)
            if book.quantity <= 0:
                raise ValidationError("Cannot issue book: insufficient quantity available.")
            cleaned_data['book'] = book  # Store book object for use in save method
        except LibraryInventory.DoesNotExist:
            raise ValidationError("Library inventory item does not exist.")

        try:
            student = RegisteredStudent.objects.get(id=student_id)
            cleaned_data['student'] = student  # Store student object for use in save method
        except RegisteredStudent.DoesNotExist:
            raise ValidationError("Student does not exist.")

        return cleaned_data

    def save(self, commit=True):
        book_issued = super().save(commit=False)
        book_issued.book = self.cleaned_data['book']
        book_issued.student = self.cleaned_data['student']

        if commit:
            book_issued.save()
        return book_issued

        
class UpdateBookIssuedForm(forms.Form):
    book_issue_id = forms.IntegerField(label="Book Issue ID")
    new_book_id = forms.IntegerField(label="New Book ID")

    def update_issued_book(self):
        book_issue_id = self.cleaned_data['book_issue_id']
        new_book_id = self.cleaned_data['new_book_id']
        try:
            issued_book = BookIssued.objects.get(id=book_issue_id)
            issued_book.book_id = new_book_id  # Assuming you have a ForeignKey to Book model
            issued_book.save()
            return True  # Successfully updated
        except BookIssued.DoesNotExist:
            return False  # Book issue ID not found

class DeleteBookIssuedForm(forms.Form):
    issued_id = forms.IntegerField(label="Issued ID")
    
    def delete_issued_book(self):
        issued_id = self.cleaned_data['issued_id']
        try:
            issued_book_record = BookIssued.objects.get(id=issued_id)
            issued_book_record.delete()
            return True  # Successfully deleted
        except BookIssued.DoesNotExist:
            return False  # Issued ID not found

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

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'