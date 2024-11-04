from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.views import LoginView
from django.db.models import Sum

def home(request):
    return render(request, 'index.html')

def feedback_view(request):
    grievance_count = Grievance.objects.count()
    feedback_count = Feedback.objects.count()
    enquiry_count = Enquiry.objects.count()
    # Initialize all forms
    context = {
        'add_grievance_form': AddGrievanceForm(),
        'update_grievance_form': UpdateGrievanceForm(),
        'delete_grievance_form': DeleteGrievanceForm(),
        'add_feedback_form': AddFeedbackForm(),
        'update_feedback_form': UpdateFeedbackForm(),
        'delete_feedback_form': DeleteFeedbackForm(),
        'add_enquiry_form': AddEnquiryForm(),
        'update_enquiry_form': UpdateEnquiryForm(),
        'delete_enquiry_form': DeleteEnquiryForm(),
        'grievance_count': grievance_count,
        'feedback_count': feedback_count,
        'enquiry_count': enquiry_count,
    }

    # Process form submissions
    if request.method == 'POST':
        forms = {
            'add_grievance': AddGrievanceForm(request.POST),
            'update_grievance': UpdateGrievanceForm(request.POST),
            'delete_grievance': DeleteGrievanceForm(request.POST),
            'add_feedback': AddFeedbackForm(request.POST),
            'update_feedback': UpdateFeedbackForm(request.POST),
            'delete_feedback': DeleteFeedbackForm(request.POST),
            'add_enquiry': AddEnquiryForm(request.POST),
            'update_enquiry': UpdateEnquiryForm(request.POST),
            'delete_enquiry': DeleteEnquiryForm(request.POST),
        }

        for key, form in forms.items():
            if form.is_valid():
                if key == 'add_grievance':
                    # Get the student ID from the form
                    student_id = request.POST.get('student')
                    try:
                        student = RegisteredStudent.objects.get(id=student_id)
                        # Create the grievance
                        grievance = form.save(commit=False)
                        grievance.student = student  # Set the foreign key
                        grievance.save()
                        messages.success(request, 'Grievance added successfully.')
                    except RegisteredStudent.DoesNotExist:
                        messages.error(request, 'Invalid Student ID.')

                elif key == 'update_grievance':
                    if form.update_grievance():  # Assuming form has an update method
                        messages.success(request, 'Grievance updated successfully.')
                    else:
                        messages.error(request, 'Invalid Grievance ID.')

                elif key == 'delete_grievance':
                    if form.delete_grievance():  # Assuming form has a delete method
                        messages.success(request, 'Grievance deleted successfully.')
                    else:
                        messages.error(request, 'Invalid Grievance ID.')

                elif key == 'add_feedback':
                    if form.save():
                        messages.success(request, 'Feedback added successfully.')
                    else:
                        messages.error(request, 'Invalid Student ID.')

                elif key == 'update_feedback':
                    if form.update_feedback():
                        messages.success(request, 'Feedback updated successfully.')
                    else:
                        messages.error(request, 'Invalid Feedback ID or Student ID.')

                elif key == 'delete_feedback':
                    if form.delete_feedback():
                        messages.success(request, 'Feedback deleted successfully.')
                    else:
                        messages.error(request, 'Invalid Feedback ID.')

                elif key == 'add_contact':
                    form.save()
                    messages.success(request, 'Contact added successfully.')

                elif key == 'update_contact':
                    if form.update_contact():
                        messages.success(request, 'Contact updated successfully.')
                    else:
                        messages.error(request, 'Invalid Contact ID.')

                elif key == 'delete_contact':
                    if form.delete_contact():
                        messages.success(request, 'Contact deleted successfully.')
                    else:
                        messages.error(request, 'Invalid Contact ID.') 

                elif key == 'add_enquiry':
                    form.save()
                    messages.success(request, 'Enquiry added successfully.')

                elif key == 'update_enquiry':
                    if form.update_enquiry():
                        messages.success(request, 'Enquiry updated successfully.')
                    else:
                        messages.error(request, 'Invalid Enquiry ID.')

                elif key == 'delete_enquiry':
                    if form.delete_enquiry():
                        messages.success(request, 'Enquiry deleted successfully.')
                    else:
                        messages.error(request, 'Invalid Enquiry ID.')               
 
                # Redirect after processing a valid form
                return redirect('/feedback/')  # Adjust this URL as needed

        # If any form was invalid, update the context with the forms
       

    return render(request, 'feedback.html', context)


def certificate_view(request):
    # Fetch all certificates to display
    applications = CertificateApplication.objects.all()
    certificates = CertificateType.objects.all() 
    total_certificates = CertificateType.objects.count()
    total_applications = CertificateApplication.objects.count()
    # Initialize all forms
    context = {
        'add_certificate_form': AddCertificateForm(),
        'update_certificate_form': UpdateCertificateForm(),
        'delete_certificate_form': DeleteCertificateForm(),
        'add_certificate_application_form': AddCertificateApplicationForm(),
        'update_certificate_application_form': UpdateCertificateApplicationForm(),
        'delete_certificate_application_form': DeleteCertificateApplicationForm(),
        'applications': applications,
        'certificates': certificates,
        'total_certificates': total_certificates,
        'total_applications': total_applications,
    }

    # Process form submissions
    if request.method == 'POST':
        forms = {
            'add_certificate': AddCertificateForm(request.POST),
            'update_certificate': UpdateCertificateForm(request.POST),
            'delete_certificate': DeleteCertificateForm(request.POST),
            'add_certificate_application': AddCertificateApplicationForm(request.POST),
            'update_certificate_application': UpdateCertificateApplicationForm(request.POST),
            'delete_certificate_application': DeleteCertificateApplicationForm(request.POST),

        }

        for key, form in forms.items():
            if form.is_valid():
                if key == 'add_certificate':
                    # Save the new certificate
                    form.save()
                    messages.success(request, 'Certificate added successfully.')
                     # Adjust this URL as needed

                elif key == 'update_certificate':
                    if form.update_certificate():
                        messages.success(request, 'Certificate updated successfully.')
                    else:
                        messages.error(request, 'Invalid Certificate ID.')
                      # Adjust this URL as needed

                elif key == 'delete_certificate':
                    if form.delete_certificate():
                        messages.success(request, 'Certificate deleted successfully.')
                    else:
                        messages.error(request, 'Invalid Certificate ID.')

                elif key == 'add_certificate_application':
                    # Save the new certificate application
                    form.save()
                    messages.success(request, 'Certificate application added successfully.')

                elif key == 'update_certificate_application':
                    if form.update_certificate_application():
                        messages.success(request, 'Certificate application updated successfully.')
                    else:
                        messages.error(request, 'Invalid Application ID.')

                elif key == 'delete_certificate_application':
                    application_id = form.cleaned_data['application_id']
                    try:
                        application = CertificateApplication.objects.get(id=application_id)
                        application.delete()
                        messages.success(request, 'Certificate application deleted successfully.')
                    except CertificateApplication.DoesNotExist:
                        messages.error(request, 'Invalid Application ID.')

                     # Adjust this URL as needed
                return redirect('/certificate/') 

        context.update(forms)     

    # Render the certificate management page
    return render(request, 'certificate.html', context)

def library_management_view(request):
    inventory_count = LibraryInventory.objects.count()
    member_count = LibraryMember.objects.count()
    total_fines = LibraryFineCollection.objects.aggregate(total_collected=Sum('amount'))['total_collected'] or 0
    total_issued_books = BookIssued.objects.count()
    
    # Initialize forms and context
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
        'inventory_count': inventory_count,
        'member_count': member_count,
        'total_fines': total_fines,
        'total_issued_books': total_issued_books,
    }

    if request.method == 'POST':
        # Process each form based on a unique submit button key in POST data
        if 'add_inventory' in request.POST:
            form = AddInventoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Inventory added successfully.')
        
        elif 'update_inventory' in request.POST:
            form = UpdateInventoryForm(request.POST)
            if form.is_valid() and form.update_inventory():
                messages.success(request, 'Book updated successfully.')
            else:
                messages.error(request, 'Invalid Book ID.')

        elif 'delete_inventory' in request.POST:
            form = DeleteInventoryForm(request.POST)
            if form.is_valid():
                if form.delete_inventory():
                    messages.success(request, 'Book deleted successfully.')
                else:
                    messages.error(request, 'Invalid Book ID.')

        elif 'add_member' in request.POST:
            form = AddMemberForm(request.POST)
            if form.is_valid():
                student_id = form.cleaned_data.get('student_id')
                
                try:
                    # Check if the student exists
                    student = RegisteredStudent.objects.get(id=student_id)
                    
                    # Create the LibraryMember instance manually to set `member`
                    library_member = form.save(commit=False)
                    library_member.member = student  # Assign the ForeignKey field
                    library_member.save()  # Now save it to the database
                    messages.success(request, 'Member added successfully.')
                
                except RegisteredStudent.DoesNotExist:
                    messages.error(request, "Student not found. Please check the Student ID.")
            else:
                messages.error(request, "Invalid data in form.")

        elif 'update_member' in request.POST:
            form = UpdateMemberForm(request.POST)
            if form.is_valid() and form.update_member():
                messages.success(request, 'Member updated successfully.')
            else:
                messages.error(request, 'Invalid Member ID or Student ID.')

        elif 'delete_member' in request.POST:
            form = DeleteMemberForm(request.POST)
            if form.is_valid():
                member_id = form.cleaned_data['member_id']
                member = LibraryMember.objects.filter(id=member_id).first()
                if member:
                    member.delete()
                    messages.success(request, 'Member deleted successfully.')
                else:
                    messages.error(request, 'Member with the provided ID does not exist.')

        elif 'add_fine' in request.POST:
            form = AddFineForm(request.POST)
            member_id = form.cleaned_data.get('member_id') if form.is_valid() else None
            
            try:
                # Check if the student exists
                member = LibraryMember.objects.get(id=member_id) if member_id else None

                if form.is_valid() and member:  # Proceed if the form is valid and student exists
                    form.save_fine()
                    messages.success(request, 'Fine added successfully.')
                else:
                    messages.error(request, "Member not present for the provided Member ID.")
            except LibraryMember.DoesNotExist:
                messages.error(request, "Member not found. Please check the Member ID.")

        elif 'update_fine' in request.POST:
            form = UpdateFineForm(request.POST)
            if form.is_valid() and form.update_fine():
                messages.success(request, 'Fine updated successfully.')
            else:
                messages.error(request, 'Invalid Fine ID.')

        elif 'delete_fine' in request.POST:
            form = DeleteFineForm(request.POST)
            if form.is_valid() and form.delete_fine():
                messages.success(request, 'Fine deleted successfully.')
            else:
                messages.error(request, 'Invalid Fine ID.')

        elif 'add_book_issued' in request.POST:
            add_book_issued_form = AddIssuedBookForm(request.POST)
            if add_book_issued_form.is_valid():
                success, message = add_book_issued_form.save_book()
                if success:
                    messages.success(request, message)
                else:
                    messages.error(request, message)
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'update_book_issued' in request.POST:
            form = UpdateBookIssuedForm(request.POST)
            if form.is_valid() and form.update_issued_book():
                messages.success(request, 'Issued book updated successfully.')
            else:
                messages.error(request, 'Invalid Book Issue ID.')

        elif 'delete_book_issued' in request.POST:
            form = DeleteBookIssuedForm(request.POST)
            if form.is_valid() and form.delete_issued_book():
                messages.success(request, 'Issued book deleted successfully.')
            else:
                messages.error(request, 'Invalid Issued ID.')

        # Redirect after form submission to clear form data
        return redirect('/library/')

    # Render the library management template with context data
    return render(request, 'library.html', context)


def student_view(request):
    courses = StreamCourse.objects.all()
    student_count = RegisteredStudent.objects.count()
    course_count = StreamCourse.objects.count()
    admission_count = AdmissionStat.objects.count()
    fee_count = FeeCollection.objects.count()
    # Initialize all forms
    context = {
        'add_student_form': AddStudentForm(),
        'update_student_form': UpdateStudentForm(),
        'delete_student_form': DeleteStudentForm(),
        'add_admission_form': AddAdmissionForm(),
        'update_admission_form': UpdateAdmissionForm(),
        'delete_admission_form': DeleteAdmissionForm(),
        'add_fee_form': AddFeeForm(),
        'update_fee_form': UpdateFeeForm(),
        'delete_fee_form': DeleteFeeForm(),
        'add_course_form' : AddStreamCourseForm(),
        'update_course_form' : UpdateStreamCourseForm(),
        'delete_course_form' : DeleteStreamCourseForm(),
        'courses': courses,
        'student_count': student_count,
        'admission_count': admission_count,
        'course_count': course_count,
        'fee_count': fee_count,
        'students': RegisteredStudent.objects.all(),
        'admissions': AdmissionStat.objects.all(),
        'fees': FeeCollection.objects.all(),
    }

    # Process form submissions
    if request.method == 'POST':
        forms = {
            'add_student': AddStudentForm(request.POST),
            'update_student': UpdateStudentForm(request.POST),
            'delete_student': DeleteStudentForm(request.POST),
            'add_admission': AddAdmissionForm(request.POST),
            'update_admission': UpdateAdmissionForm(request.POST),
            'delete_admission': DeleteAdmissionForm(request.POST),
            'add_fee': AddFeeForm(request.POST),
            'update_fee': UpdateFeeForm(request.POST),
            'delete_fee': DeleteFeeForm(request.POST),
            'add_course': AddStreamCourseForm(request.POST),
            'update_course': UpdateStreamCourseForm(request.POST),
            'delete_course': DeleteStreamCourseForm(request.POST),
        }

        for key, form in forms.items():
            if form.is_valid():
                if key == 'add_student':
                    student = form.save(commit=False)
                    student.course = StreamCourse.objects.get(id=request.POST['course'])
                    student.save()
                    messages.success(request, 'Student added successfully.')

                
                elif key == 'update_student':
                    update_student_form = forms['update_student']
                    if update_student_form.is_valid():
                        if update_student_form.update_student():
                            messages.success(request, 'student updated successfully.')
                        else:
                            messages.error(request, 'Invalid student ID.')
                     

    
                elif key == 'delete_student':
                    delete_student_form = forms['delete_student']
                    if delete_student_form.is_valid():
                        student_id = delete_student_form.cleaned_data['student_id']
                        try:
                            student = RegisteredStudent.objects.get(id=student_id)
                            student.delete()
                            messages.success(request, 'Student deleted successfully.')
                        except RegisteredStudent.DoesNotExist:
                            messages.error(request, 'Student with the provided ID does not exist.')

                elif key == 'add_admission':
                    form.save()
                    messages.success(request, 'Admission added successfully.')

                elif key == 'update_admission':
                    update_admission_form = forms['update_admission']
                    if update_admission_form.is_valid():
                        if update_admission_form.update_admission():
                            messages.success(request, 'admission updated successfully.')
                        else:
                            messages.error(request, 'Invalid admission ID.')

                elif key == 'delete_admission':
                    delete_admission_form = forms['delete_admission']
                    if delete_admission_form.is_valid():
                        admission_id = delete_admission_form.cleaned_data.get('admission_id')
                        try:
                            admission = AdmissionStat.objects.get(id=admission_id)
                            admission.delete()
                            messages.success(request, "Admission deleted successfully!")
                        except AdmissionStat.DoesNotExist:
                            messages.error(request, "Admission ID not found.")
            

                elif key == 'add_fee':
                    form.save()
                    messages.success(request, 'Fee added successfully.')     

                elif key == 'update_fee':
                    update_fee_form = forms['update_fee']
                    if update_fee_form.is_valid():
                        if update_fee_form.update_fee():
                            messages.success(request, 'Fee updated successfully.')
                        else:
                            messages.error(request, 'Invalid fee ID or Student ID.')

                elif key == 'delete_fee':
                    delete_fee_form = forms['delete_fee']
                    if delete_fee_form.is_valid():
                        try:
                            fee_id = delete_fee_form.cleaned_data.get('fee_id')
                            fee = get_object_or_404(FeeCollection, id=fee_id)
                            fee.delete()
                            messages.success(request, "Fee deleted successfully!")
                        except :
                            messages.error(request,"Fee ID not found")
                    else :
                        messages.error(request,"Fee ID not found")

                elif key == "add_course":
                    form.save()
                    messages.success(request, 'Course added successfully.')

                elif key == 'update_course':
                    update_course_form = forms['update_course']
                    if update_course_form.is_valid():
                        if update_course_form.update_stream_course():
                            messages.success(request, 'course updated successfully.')
                        else:
                            messages.error(request, 'Invalid course ID.')    

                elif key == 'delete_course':
                    delete_course_form = forms['delete_course']
                    if delete_course_form.is_valid():
                        course_id = delete_course_form.cleaned_data.get('course_id')
                        try:
                            course = StreamCourse.objects.get(id=course_id)
                            course.delete()
                            messages.success(request, "Course deleted successfully!")
                        except StreamCourse.DoesNotExist:
                            messages.error(request, "Course not found.")
                

                return redirect('/student/')  # Use a named URL for better maintainability

   
    # Render the student management page
    return render(request, 'student.html', context)

def website_management_view(request):
    news_notices = NewsNotice.objects.all()  # Fetch all news/notice items
    total_notices = news_notices.count()
    departments = Department.objects.all()  # Fetch all department records
    total_departments = departments.count()
    sliders = Slider.objects.all()  # Fetch all slider records
    total_sliders = sliders.count()
    tickers = Ticker.objects.all()  # Fetch all ticker records
    total_tickers = tickers.count()
    images = ImageGallery.objects.all() 
    videos = VideoGallery.objects.all()  # Fetch all videos from the gallery
    total_videos = videos.count()
    faculties = Faculty.objects.all()  # Fetch all faculty records
    departments = Department.objects.all()  # Fetch all departments for the dropdown
    total_faculty = faculties.count()
    # Initialize forms and context with data
    context = {
        'add_news_form': AddNewsNoticeForm(),
        'update_news_form': UpdateNewsNoticeForm(),
        'delete_news_form': DeleteNewsNoticeForm(),
        'add_department_form': AddDepartmentForm(),
        'update_department_form': UpdateDepartmentForm(),
        'delete_department_form': DeleteDepartmentForm(),
        'add_slider_form': AddSliderForm(),
        'update_slider_form': UpdateSliderForm(),
        'delete_slider_form': DeleteSliderForm(),
        'add_ticker_form': AddTickerForm(),
        'update_ticker_form': UpdateTickerForm(),
        'delete_ticker_form': DeleteTickerForm(),
        'add_image_form': AddImageForm(),
        'update_image_form': UpdateImageForm(),
        'delete_image_form': DeleteImageForm(),
        'add_video_form': AddVideoForm(),
        'update_video_form': UpdateVideoForm(),
        'delete_video_form': DeleteVideoForm(),
        'add_faculty_form': AddFacultyForm(),
        'update_faculty_form': UpdateFacultyForm(),
        'delete_faculty_form': DeleteFacultyForm(),
        # Fetch objects for display
        'departments': Department.objects.all(),
        'sliders': Slider.objects.all(),
        'courses': StreamCourse.objects.all(),
        'tickers': Ticker.objects.all(),
        'images': ImageGallery.objects.all(),
        'videos': VideoGallery.objects.all(),
        'faculty_members': Faculty.objects.all(),
        'news_notices': news_notices,
        'total_notices': total_notices,
        'departments': departments,
        'total_departments': total_departments,
        'sliders': sliders,
        'total_sliders': total_sliders,
        'tickers': tickers,
        'total_tickers': total_tickers,
        'images': images,
        'total_images': images.count(),
        'videos': videos,
        'total_videos': total_videos,
        'faculties': faculties,
        'departments': departments,
        'total_faculty': total_faculty,
    }

    if request.method == 'POST':
        # Check and process each form individually based on the unique submit button in POST data
        if 'add_news_notice' in request.POST:
            form = AddNewsNoticeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'News/Notice added successfully.')

        elif 'update_news_notice' in request.POST:
            form = UpdateNewsNoticeForm(request.POST)
            if form.is_valid() and form.update_notice():
                messages.success(request, 'News updated successfully.')
            else:
                messages.error(request, 'Invalid News ID.')

        elif 'delete_news_notice' in request.POST:
            form = DeleteNewsNoticeForm(request.POST)
            if form.is_valid():
                notice_id = form.cleaned_data['notice_id']
                try:
                    news_notice = NewsNotice.objects.get(id=notice_id)
                    news_notice.delete()
                    messages.success(request, 'News/Notice deleted successfully.')
                except NewsNotice.DoesNotExist:
                    messages.error(request, 'News/Notice with the provided ID does not exist.')

        elif 'add_department' in request.POST:
            form = AddDepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Department added successfully.')

        elif 'update_department' in request.POST:
            form = UpdateDepartmentForm(request.POST)
            if form.is_valid() and form.update_department():
                messages.success(request, 'Department updated successfully.')
            else:
                messages.error(request, 'Invalid Department ID.')

        elif 'delete_department' in request.POST:
            form = DeleteDepartmentForm(request.POST)
            if form.is_valid():
                department_id = form.cleaned_data['department_id']
                try:
                    department = Department.objects.get(id=department_id)
                    department.delete()
                    messages.success(request, 'Department deleted successfully.')
                except Department.DoesNotExist:
                    messages.error(request, 'Department with the provided ID does not exist.')

        elif 'add_slider' in request.POST:
            form = AddSliderForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Slider added successfully.')

        elif 'update_slider' in request.POST:
            form = UpdateSliderForm(request.POST)
            if form.is_valid() and form.update_slider():
                messages.success(request, 'Slider updated successfully.')
            else:
                messages.error(request, 'Invalid Slider ID.')

        elif 'delete_slider' in request.POST:
            form = DeleteSliderForm(request.POST)
            if form.is_valid():
                slider_id = form.cleaned_data['slider_id']
                try:
                    slider = Slider.objects.get(id=slider_id)
                    slider.delete()
                    messages.success(request, 'Slider deleted successfully.')
                except Slider.DoesNotExist:
                    messages.error(request, 'Slider with the provided ID does not exist.')

        elif 'add_ticker' in request.POST:
            form = AddTickerForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ticker added successfully.')

        elif 'update_ticker' in request.POST:
            form = UpdateTickerForm(request.POST)
            if form.is_valid() and form.update_ticker():
                messages.success(request, 'Ticker updated successfully.')
            else:
                messages.error(request, 'Invalid Ticker ID.')

        elif 'delete_ticker' in request.POST:
            form = DeleteTickerForm(request.POST)
            if form.is_valid():
                ticker_id = form.cleaned_data['ticker_id']
                try:
                    ticker = Ticker.objects.get(id=ticker_id)
                    ticker.delete()
                    messages.success(request, 'Ticker deleted successfully.')
                except Ticker.DoesNotExist:
                    messages.error(request, 'Ticker with the provided ID does not exist.')

        elif 'add_image' in request.POST:
            form = AddImageForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Image added successfully.')

        elif 'update_image' in request.POST:
            form = UpdateImageForm(request.POST)
            if form.is_valid() and form.update_image():
                messages.success(request, 'Image updated successfully.')
            else:
                messages.error(request, 'Invalid Image ID.')

        elif 'delete_image' in request.POST:
            form = DeleteImageForm(request.POST)
            if form.is_valid():
                image_id = form.cleaned_data['image_id']
                try:
                    image = ImageGallery.objects.get(id=image_id)
                    image.delete()
                    messages.success(request, 'Image deleted successfully.')
                except ImageGallery.DoesNotExist:
                    messages.error(request, 'Image with the provided ID does not exist.')

        elif 'add_video' in request.POST:
            form = AddVideoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Video added successfully.')

        elif 'update_video' in request.POST:
            form = UpdateVideoForm(request.POST)
            if form.is_valid() and form.update_video():
                messages.success(request, 'Video updated successfully.')
            else:
                messages.error(request, 'Invalid Video ID.')

        elif 'delete_video' in request.POST:
            form = DeleteVideoForm(request.POST)
            if form.is_valid():
                video_id = form.cleaned_data['video_id']
                try:
                    video = VideoGallery.objects.get(id=video_id)
                    video.delete()
                    messages.success(request, 'Video deleted successfully.')
                except VideoGallery.DoesNotExist:
                    messages.error(request, 'Video with the provided ID does not exist.')

        elif 'add_faculty' in request.POST:
            form = AddFacultyForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Faculty member added successfully.')

        elif 'update_faculty' in request.POST:
            form = UpdateFacultyForm(request.POST)
            if form.is_valid() and form.update_faculty():
                messages.success(request, 'Faculty updated successfully.')
            else:
                messages.error(request, 'Invalid Faculty ID.')

        elif 'delete_faculty' in request.POST:
            form = DeleteFacultyForm(request.POST)
            if form.is_valid():
                faculty_id = form.cleaned_data['faculty_id']
                try:
                    faculty = Faculty.objects.get(id=faculty_id)
                    faculty.delete()
                    messages.success(request, 'Faculty member deleted successfully.')
                except Faculty.DoesNotExist:
                    messages.error(request, 'Faculty with the provided ID does not exist.')

        # Redirect to the management page after any form submission
        return redirect('/management/')

    # Render the management template with context data
    return render(request, 'management.html', context)


# Management View
# def management_view(request):
#     return render(request, 'management.html')

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

# Student Management
def student_list(request):
    students = RegisteredStudent.objects.all()
    return render(request, 'student_list.html', {'students': students})

def admission_list(request):
    admissions = AdmissionStat.objects.all()
    return render(request, 'admission_list.html', {'admissions': admissions})

def fee_collection_list(request):
    fees = FeeCollection.objects.all()
    return render(request, 'fee_collection_list.html', {'fees': fees})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
def show_students(request):
    students = RegisteredStudent.objects.all()  # Retrieve all students
    context = {
        'students': students,
    }
    return render(request, 'show_students.html', context)

def show_admissions(request):
    admissions = AdmissionStat.objects.all()  # Fetch all admissions
    context = {
        'admissions': admissions,
    }
    return render(request, 'show_admissions.html', context)

def show_courses(request):
    courses = StreamCourse.objects.all()  # Fetch all stream courses
    context = {
        'courses': courses,
    }
    return render(request, 'show_courses.html', context)

def show_fees(request):
    fees = FeeCollection.objects.all()  # Fetch all fee collections
    context = {
        'fees': fees,
    }
    return render(request, 'show_fees.html', context)

def show_grievances(request):
    grievances = Grievance.objects.all()  # Fetch all grievances
    context = {
        'grievances': grievances,
    }
    return render(request, 'show_grievances.html', context)

def show_feedback(request):
    feedbacks = Feedback.objects.all()  # Fetch all feedback entries
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'show_feedback.html', context)

def show_enquiries(request):
    enquiries = Enquiry.objects.all()  # Fetch all enquiry entries
    context = {
        'enquiries': enquiries,
    }
    return render(request, 'show_enquiries.html', context)

def show_inventory(request):
    inventory = LibraryInventory.objects.all()  # Fetch all inventory entries
    context = {
        'inventory': inventory,
    }
    return render(request, 'show_inventory.html', context)

def show_members(request):
    members = LibraryMember.objects.all()  # Fetch all member entries
    context = {
        'members': members,
    }
    return render(request, 'show_members.html', context)

def show_fines(request):
    fines = LibraryFineCollection.objects.all()  # Fetch all fine entries
    context = {
        'fines': fines,
    }
    return render(request, 'show_fines.html', context)

def show_issued_books(request):
    issued_books = BookIssued.objects.all()  # Fetch all issued book entries
    context = {
        'issued_books': issued_books,
    }
    return render(request, 'show_issued_books.html', context)

def show_certificates(request):
    certificates = CertificateType.objects.all()  # Fetch all certificate entries
    context = {
        'certificates': certificates,
    }
    return render(request, 'show_certificates.html', context)

def show_applications(request):
    applications = CertificateApplication.objects.select_related('certificate').all()  # Fetch all applications
    context = {
        'applications': applications,
    }
    return render(request, 'show_applications.html', context)

def show_news_notices(request):
    news_notices = NewsNotice.objects.all()  # Fetch all news/notice records
    context = {
        'news_notices': news_notices,
    }
    return render(request, 'show_news_notices.html', context)

def show_departments(request):
    departments = Department.objects.all()  # Fetch all department records
    context = {
        'departments': departments,
    }
    return render(request, 'show_departments.html', context)

def show_sliders(request):
    sliders = Slider.objects.all()  # Fetch all slider records
    context = {
        'sliders': sliders,
    }
    return render(request, 'show_sliders.html', context)

def show_tickers(request):
    tickers = Ticker.objects.all()  # Fetch all ticker records
    context = {
        'tickers': tickers,
    }
    return render(request, 'show_tickers.html', context)

def show_gallery(request):
    images = ImageGallery.objects.all()  # Fetch all ticker records
    context = {
        'images': images,
    }
    return render(request, 'show_gallery.html', context)

def show_videos(request):
    videos = VideoGallery.objects.all()  # Fetch all ticker records
    context = {
        'videos': videos,
    }
    return render(request, 'show_videos.html', context)

def show_faculty(request):
    faculties = Faculty.objects.all()  # Fetch all faculty records
    context = {
        'faculties': faculties,
    }
    return render(request, 'show_faculty.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')