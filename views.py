from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import (
    AddInventoryForm, UpdateInventoryForm, DeleteInventoryForm,
    AddMemberForm, UpdateMemberForm, DeleteMemberForm,
    AddFineForm, UpdateFineForm, DeleteFineForm,
    AddIssuedBookForm, UpdateBookIssuedForm, DeleteBookIssuedForm,
    DepartmentForm, NewsNoticeForm, FacultyForm, ImageGalleryForm, 
    VideoGalleryForm, LibraryInventoryForm, LibraryMemberForm, 
    GrievanceForm, FeedbackForm, ContactUsForm,AddStudentForm, UpdateStudentForm, DeleteStudentForm,
    AddAdmissionForm, UpdateAdmissionForm, DeleteAdmissionForm,
    AddCourseForm, UpdateCourseForm, DeleteCourseForm,
    AddFeeForm, UpdateFeeForm, DeleteFeeForm
)
from .models import LibraryInventory, LibraryMember, LibraryFineCollection, BookIssued, Department, NewsNotice, Faculty, ImageGallery, VideoGallery, LibraryInventory, LibraryMember, Grievance, Feedback, ContactUs,Student, Admission, StreamCourse, FeeCollection

def home(request):
    return render(request, 'index.html')

def student(request):
    return render(request, 'student.html')

# Student Views
def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = AddStudentForm()
    return render(request, 'add_student.html', {'form': form})

def update_student(request):
    if request.method == 'POST':
        form = UpdateStudentForm(request.POST)
        if form.is_valid():
            student = Student.objects.get(id=form.cleaned_data['student_id'])
            student.student_name = form.cleaned_data['student_name']
            student.course = form.cleaned_data['course']
            student.admission_date = form.cleaned_data['admission_date']
            student.fee_status = form.cleaned_data['fee_status']
            student.save()
            return redirect('success')
    else:
        form = UpdateStudentForm()
    return render(request, 'update_student.html', {'form': form})

def delete_student(request):
    if request.method == 'POST':
        form = DeleteStudentForm(request.POST)
        if form.is_valid():
            Student.objects.filter(id=form.cleaned_data['student_id']).delete()
            return redirect('success')
    else:
        form = DeleteStudentForm()
    return render(request, 'delete_student.html', {'form': form})

# Admission Views
def add_admission(request):
    if request.method == 'POST':
        form = AddAdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = AddAdmissionForm()
    return render(request, 'add_admission.html', {'form': form})

def update_admission(request):
    if request.method == 'POST':
        form = UpdateAdmissionForm(request.POST)
        if form.is_valid():
            admission = Admission.objects.get(id=form.cleaned_data['admission_id'])
            admission.year = form.cleaned_data['updated_year']
            admission.total_admissions = form.cleaned_data['updated_total_admissions']
            admission.course = form.cleaned_data['updated_course']
            admission.save()
            return redirect('success')
    else:
        form = UpdateAdmissionForm()
    return render(request, 'update_admission.html', {'form': form})

def delete_admission(request):
    if request.method == 'POST':
        form = DeleteAdmissionForm(request.POST)
        if form.is_valid():
            Admission.objects.filter(id=form.cleaned_data['admission_id']).delete()
            return redirect('success')
    else:
        form = DeleteAdmissionForm()
    return render(request, 'delete_admission.html', {'form': form})

# Course Views
def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = AddCourseForm()
    return render(request, 'add_course.html', {'form': form})

def update_course(request):
    if request.method == 'POST':
        form = UpdateCourseForm(request.POST)
        if form.is_valid():
            course = StreamCourse.objects.get(id=form.cleaned_data['course_id'])
            course.stream_name = form.cleaned_data['new_stream_name']
            course.course_name = form.cleaned_data['new_course_name']
            course.save()
            return redirect('success')
    else:
        form = UpdateCourseForm()
    return render(request, 'update_course.html', {'form': form})

def delete_course(request):
    if request.method == 'POST':
        form = DeleteCourseForm(request.POST)
        if form.is_valid():
            StreamCourse.objects.filter(id=form.cleaned_data['course_id']).delete()
            return redirect('success')
    else:
        form = DeleteCourseForm()
    return render(request, 'delete_course.html', {'form': form})

# Fee Views
def add_fee(request):
    if request.method == 'POST':
        form = AddFeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = AddFeeForm()
    return render(request, 'add_fee.html', {'form': form})

def update_fee(request):
    if request.method == 'POST':
        form = UpdateFeeForm(request.POST)
        if form.is_valid():
            fee = FeeCollection.objects.get(id=form.cleaned_data['fee_id'])
            fee.amount = form.cleaned_data['new_amount']
            fee.date_paid = form.cleaned_data['new_date_paid']
            fee.save()
            return redirect('success')
    else:
        form = UpdateFeeForm()
    return render(request, 'update_fee.html', {'form': form})

def delete_fee(request):
    if request.method == 'POST':
        form = DeleteFeeForm(request.POST)
        if form.is_valid():
            FeeCollection.objects.filter(id=form.cleaned_data['fee_id']).delete()
            return redirect('success')
    else:
        form = DeleteFeeForm()
    return render(request, 'delete_fee.html', {'form': form})





def library_management_view(request):
    # Initialize all forms
    context = {
        'add_inventory_form': AddInventoryForm(),
        'update_inventory_form': UpdateInventoryForm(),
        'delete_inventory_form': DeleteInventoryForm(),
        'add_member_form': AddMemberForm(),
        'update_member_form': UpdateMemberForm(),
        'delete_member_form': DeleteMemberForm(),
        'add_fine_form': AddFineForm(),
        'update_fine_form': UpdateFineForm(),
        'delete_fine_form': DeleteFineForm(),
        'add_book_issued_form': AddIssuedBookForm(),
        'update_book_issued_form': UpdateBookIssuedForm(),
        'delete_book_issued_form': DeleteBookIssuedForm(),
    }

    # Process form submissions
    if request.method == 'POST':
        forms = {
            'add_inventory': AddInventoryForm(request.POST),
            'update_inventory': UpdateInventoryForm(request.POST),
            'delete_inventory': DeleteInventoryForm(request.POST),
            'add_member': AddMemberForm(request.POST),
            'update_member': UpdateMemberForm(request.POST),
            'delete_member': DeleteMemberForm(request.POST),
            'add_fine': AddFineForm(request.POST),
            'update_fine': UpdateFineForm(request.POST),
            'delete_fine': DeleteFineForm(request.POST),
            'add_book_issued': AddIssuedBookForm(request.POST),
            'update_book_issued': UpdateBookIssuedForm(request.POST),
            'delete_book_issued': DeleteBookIssuedForm(request.POST),
        }

        for key, form in forms.items():
            if form.is_valid():
                if key == 'add_inventory':
                    form.save()
                    messages.success(request, 'Inventory added successfully.')
                    
                elif key == 'update_inventory':
                    update_inventory_form = forms['update_inventory']
                    if update_inventory_form.is_valid():
                        if update_inventory_form.update_inventory():
                            messages.success(request, 'Book updated successfully.')
                        else:
                            messages.error(request, 'Invalid Book ID.')
                            
                elif key == 'delete_inventory':
                    delete_inventory_form = forms['delete_inventory']
                    if delete_inventory_form.is_valid():
                        if delete_inventory_form.delete_inventory():
                            messages.success(request, 'Book deleted successfully.')
                        else:
                            messages.error(request, 'Invalid Book ID.')
                    
                elif key == 'add_member':
                    add_member_form = forms['add_member']
                    if add_member_form.is_valid():
                        add_member_form.save()
                        messages.success(request, 'Member added successfully.')
                        
                elif key == 'update_member':
                    update_member_form = forms['update_member']
                    if update_member_form.is_valid():
                        if update_member_form.update_member():
                            messages.success(request, 'Member updated successfully.')
                        else:
                            messages.error(request, 'Invalid Member ID or Student ID.')
                    
                elif key == 'delete_member':
                    delete_member_form = forms['delete_member']
                    if delete_member_form.is_valid():
                        member_id = delete_member_form.cleaned_data['member_id']
                        member = LibraryMember.objects.filter(id=member_id).first()
                        if member:
                            member.delete()
                            messages.success(request, 'Member deleted successfully.')
                        else:
                            messages.error(request, 'Member with the provided ID does not exist.')

                elif key == 'add_fine':
                    add_fine_form = forms['add_fine']
                    if add_fine_form.is_valid():
                        if add_fine_form.save_fine():
                            messages.success(request, 'Fine added successfully.')
                        else:
                            messages.error(request, 'Invalid Student ID.')
                        
                elif key == 'update_fine':
                    update_fine_form = forms['update_fine']
                    if update_fine_form.is_valid():
                        if update_fine_form.update_fine():
                            messages.success(request, 'Fine updated successfully.')
                        else:
                            messages.error(request, 'Invalid Fine ID.')
                            
                elif key == 'delete_fine':
                    delete_fine_form = forms['delete_fine']
                    if delete_fine_form.is_valid():
                        if delete_fine_form.delete_fine():
                            messages.success(request, 'Fine deleted successfully.')
                        else:
                            messages.error(request, 'Invalid Fine ID.')
                            
                elif key == 'add_book_issued':
                    add_book_issued_form = AddIssuedBookForm(request.POST)
                    if add_book_issued_form.is_valid():
                        # Save the form and issue the book
                        try:
                            add_book_issued_form.save()
                            messages.success(request, 'Book issued successfully.')
                        except ValidationError as e:
                            messages.error(request, str(e))
                    else:
                        # Print form errors for debugging
                        print(add_book_issued_form.errors)
                        messages.error(request, 'Please correct the errors below.')

                        
                elif key == 'update_book_issued':
                    update_book_issued_form = forms['update_book_issued']
                    if update_book_issued_form.is_valid():
                        if update_book_issued_form.update_issued_book():
                            messages.success(request, 'Issued book updated successfully.')
                        else:
                            messages.error(request, 'Invalid Book Issue ID.')
                            
                elif key == 'delete_book_issued':
                    delete_issued_book_form = forms['delete_book_issued']
                    if delete_issued_book_form.is_valid():
                        if delete_issued_book_form.delete_issued_book():
                            messages.success(request, 'Issued book deleted successfully.')
                        else:
                            messages.error(request, 'Invalid Issued ID.')
                
                return redirect('/library/')  # Use a named URL for better maintainability

    # Render the library management page
    return render(request, 'library.html', context)

# Management View
def management_view(request):
    return render(request, 'management.html')

# Department Management
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})

# News Notice Management
def news_notice_list(request):
    news_notices = NewsNotice.objects.all()
    return render(request, 'news_notice_list.html', {'news_notices': news_notices})

def news_notice_create(request):
    if request.method == 'POST':
        form = NewsNoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_notice_list')
    else:
        form = NewsNoticeForm()
    return render(request, 'news_notice_form.html', {'form': form})

# Faculty Management
def faculty_list(request):
    faculty_members = Faculty.objects.all()
    return render(request, 'faculty_list.html', {'faculty_members': faculty_members})

def faculty_create(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'faculty_form.html', {'form': form})

# Image Gallery Management
def image_gallery_list(request):
    images = ImageGallery.objects.all()
    return render(request, 'image_gallery_list.html', {'images': images})

def image_gallery_create(request):
    if request.method == 'POST':
        form = ImageGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_gallery_list')
    else:
        form = ImageGalleryForm()
    return render(request, 'image_gallery_form.html', {'form': form})

# Video Gallery Management
def video_gallery_list(request):
    videos = VideoGallery.objects.all()
    return render(request, 'video_gallery_list.html', {'videos': videos})

def video_gallery_create(request):
    if request.method == 'POST':
        form = VideoGalleryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('video_gallery_list')
    else:
        form = VideoGalleryForm()
    return render(request, 'video_gallery_form.html', {'form': form})

# Library Management
def library_inventory_list(request):
    inventory = LibraryInventory.objects.all()
    return render(request, 'library_inventory_list.html', {'inventory': inventory})

def library_member_list(request):
    members = LibraryMember.objects.all()
    return render(request, 'library_member_list.html', {'members': members})

# Grievance Management
def grievance_list(request):
    grievances = Grievance.objects.all()
    return render(request, 'grievance_list.html', {'grievances': grievances})

# Feedback Management
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

# Contact Us Management
def contact_us_list(request):
    contacts = ContactUs.objects.all()
    return render(request, 'contact_us_list.html', {'contacts': contacts})