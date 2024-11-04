# College Management System

## Overview

The College Management System is a comprehensive application designed to manage various aspects of a college's operations. It includes features for managing departments, faculty, students, courses, library inventory, grievances, feedback, and more. This system aims to streamline administrative tasks, enhance communication, and improve overall efficiency in managing college activities.

## Features

- **Department Management**: Create and manage departments within the college.
- **News and Notices**: Post news and updates for students and faculty.
- **Slider Management**: Manage image sliders for announcements or events.
- **Ticker Management**: Display scrolling messages for important information.
- **Image and Video Galleries**: Maintain galleries for visual content.
- **Faculty Management**: Manage faculty details including contact information.
- **Course Management**: Define streams and associated courses.
- **Student Registration**: Manage registered students and their admission details.
- **Fee Collection**: Track fee payments and statuses.
- **Certificate Management**: Handle applications for certificates, including status tracking.
- **Library Management**: Maintain library inventory, manage memberships, fines, and issued books.
- **Grievance Handling**: Submit and track grievances raised by students.
- **Feedback System**: Collect feedback from students regarding various aspects of the college.
- **Enquiry Management**: Handle enquiries from prospective students.

## Entity-Relationship Diagram (ERD)

The ERD visually represents the relationships between various entities in the College Management System. Below is a brief description of the key entities and their relationships:

![dbmserp](https://github.com/user-attachments/assets/972befa6-1f61-4465-aef1-ae3bb1214b7c)

### Key Entities:

1. **Department**: Represents academic departments within the college.
2. **Faculty**: Contains details about faculty members, linked to their respective departments.
3. **StreamCourse**: Represents courses offered under various streams.
4. **RegisteredStudent**: Maintains information about enrolled students, linked to their respective courses.
5. **AdmissionStat**: Tracks admission statistics for courses.
6. **FeeCollection**: Manages fee payments made by registered students.
7. **CertificateType**: Defines types of certificates that can be applied for.
8. **CertificateApplication**: Tracks applications for certificates made by students.
9. **LibraryInventory**: Holds information about books available in the library.
10. **LibraryMember**: Represents students who are members of the library.
11. **LibraryFineCollection**: Manages fines for library members.
12. **BookIssued**: Tracks books issued to library members.
13. **Grievance**: Handles grievances submitted by students.
14. **Feedback**: Collects feedback from students.
15. **Enquiry**: Manages enquiries made by prospective students.

### Relationships:

- **One-to-Many**: 
  - A department can have many faculty members.
  - A course can have many registered students.
  - A student can have multiple fee records and grievances.
  
- **Many-to-One**: 
  - Many registered students can apply for one type of certificate.
  - Many books can be issued to one library member.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Astha-Pathak/Student_management.git
   ```

2. Navigate to the project directory:
   ```bash
   cd dbmserp
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`.

## Usage

- Log in to the admin panel to manage various entities.
- Use the provided interfaces to add, edit, and delete records as necessary.
- Monitor student registrations, fee statuses, and library operations.

## Contribution

Contributions to enhance the system are welcome. Please submit a pull request or open an issue for any suggestions or bug reports.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
