from django.contrib import admin
from .models import (
    NewsNotice, Slider, Ticker, ImageGallery, VideoGallery, Faculty, Department,
    StreamCourse, RegisteredStudent, AdmissionStat, FeeCollection,
    CertificateType, CertificateApplication,
    LibraryInventory, LibraryMember, LibraryFineCollection, BookIssued,
    Grievance, Feedback, Enquiry
)

# Website Management
admin.site.register(NewsNotice)
admin.site.register(Slider)
admin.site.register(Ticker)
admin.site.register(ImageGallery)
admin.site.register(VideoGallery)

# Faculty & Department
admin.site.register(Faculty)
admin.site.register(Department)

# Administration & Student Admission Management
admin.site.register(StreamCourse)
admin.site.register(RegisteredStudent)
admin.site.register(AdmissionStat)
admin.site.register(FeeCollection)

# Certificate Management
admin.site.register(CertificateType)
admin.site.register(CertificateApplication)

# Library Management
admin.site.register(LibraryInventory)
admin.site.register(LibraryMember)
admin.site.register(LibraryFineCollection)
admin.site.register(BookIssued)

# Grievances & Feedback
admin.site.register(Grievance)
admin.site.register(Feedback)
admin.site.register(Enquiry)