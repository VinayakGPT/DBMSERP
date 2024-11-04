from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView
from dbms.views import (
    home,
    student,
    library_management_view,
    management_view,
    department_list, department_create,
    news_notice_list, news_notice_create,
    faculty_list, faculty_create,
    image_gallery_list, image_gallery_create,
    video_gallery_list, video_gallery_create,
    library_inventory_list, library_member_list,
    grievance_list,
    feedback_list,
    contact_us_list
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),   
    path('library/', library_management_view, name='library'),
   path('student/', student , name='student'),
   
    # path('add_inventory/', add_inventory_form, name='add_inventory_form'),
    path('management/', management_view, name='management'),
    path('departments/', department_list, name='department_list'),
    path('departments/create/', department_create, name='department_create'),
    path('news-notices/', news_notice_list, name='news_notice_list'),
    path('news-notices/create/', news_notice_create, name='news_notice_create'),
    path('faculty/', faculty_list, name='faculty_list'),
    path('faculty/create/', faculty_create, name='faculty_create'),
    path('image-gallery/', image_gallery_list, name='image_gallery_list'),
    path('image-gallery/create/', image_gallery_create, name='image_gallery_create'),
    path('video-gallery/', video_gallery_list, name='video_gallery_list'),
    path('video-gallery/create/', video_gallery_create, name='video_gallery_create'),
    path('library/inventory/', library_inventory_list, name='library_inventory_list'),
    path('library/members/', library_member_list, name='library_member_list'),
    path('grievances/', grievance_list, name='grievance_list'),
    path('feedback/', feedback_list, name='feedback_list'),
    path('contact-us/', contact_us_list, name='contact_us_list'),
]
