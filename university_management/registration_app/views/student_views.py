import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from registration_app.services_fabric.services_student import Student


def create_student(request):
    """
    Handle the creation of a new student.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the student creation.
        HttpResponse: A rendered HTML response for the student creation form.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            student = Student(first_name=first_name, last_name=last_name, email=email)
            student.save()

            return JsonResponse({"success": True, "message": "Student created successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return render(request, 'students/create_student.html')


def student_list(request):
    """
    Display a list of students with optional filters and pagination.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the paginated list of students if the request is AJAX.
        HttpResponse: A rendered HTML response for the student list.
    """
    # Filters
    title_filter = request.GET.get('title', None)
    course_filter = request.GET.get('course', None)

    # Prepare the students list
    # TODO
    # students = Student.all()
    # Mock data for demonstration purposes
    students = [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com"
        },
        {
            "id": 3,
            "first_name": "Robert",
            "last_name": "Johnson",
            "email": "robert.johnson@example.com"
        },
        {
            "id": 4,
            "first_name": "Emily",
            "last_name": "Davis",
            "email": "emily.davis@example.com"
        },
        {
            "id": 5,
            "first_name": "Michael",
            "last_name": "Brown",
            "email": "michael.brown@example.com"
        },
        {
            "id": 6,
            "first_name": "Sarah",
            "last_name": "Wilson",
            "email": "sarah.wilson@example.com"
        },
        {
            "id": 7,
            "first_name": "David",
            "last_name": "Taylor",
            "email": "david.taylor@example.com"
        },
        {
            "id": 8,
            "first_name": "Olivia",
            "last_name": "Anderson",
            "email": "olivia.anderson@example.com"
        },
        {
            "id": 9,
            "first_name": "Daniel",
            "last_name": "Thomas",
            "email": "daniel.thomas@example.com"
        },
        {
            "id": 10,
            "first_name": "Sophia",
            "last_name": "Moore",
            "email": "sophia.moore@example.com"
        }
    ]

    # If invalid or empty, reset to None
    title_filter = None if title_filter in [None, '', 'None'] else title_filter
    course_filter = None if course_filter in [None, '', 'None'] else course_filter

    # Filter by title if provided
    if title_filter:
        students = Student.get_students_by_title(title_filter)

    # Filter by course if provided
    if course_filter:
        students = Student.get_students_by_course(course_filter)

    # Pagination setup
    paginator = Paginator(students, 5)  # 25 students per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page param
    try:
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        print(f"Error while getting page: {e}")
        page_obj = paginator.get_page(1)  # Default to first page if there's an issue

    # Get filters for titles and courses
    # TODO
    # titles = Title.all()
    # Mock data for demonstration purposes
    titles = [
        {"id": 1, "name": "Master in Artificial Intelligence"},
        {"id": 2, "name": "Master in Data Analytics"},
        {"id": 3, "name": "Master in Robotics"},
        {"id": 4, "name": "Master in Business Administration"}
    ]

    # Todo
    # courses = Course.all()
    # Mock data for demonstration purposes
    courses = [
        {"id": 1, "name": "Introduction to Programming",
         "description": "Learn the basics of programming using Python.", "start_date": "2024-01-10",
         "end_date": "2024-05-10"},
        {"id": 2, "name": "Advanced Web Development",
         "description": "Explore advanced concepts in web development with Django and React.",
         "start_date": "2024-02-15", "end_date": "2024-06-30"},
        {"id": 3, "name": "Database Management Systems",
         "description": "Understand the design, implementation, and management of database systems.",
         "start_date": "2024-03-01", "end_date": "2024-07-15"},
        {"id": 4, "name": "Machine Learning Basics",
         "description": "An introduction to machine learning concepts and algorithms.", "start_date": "2024-04-05",
         "end_date": "2024-08-20"}
    ]

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        student_data = []
        for student in page_obj:
            # TODO: Update the student data to match the actual model fields
            student_data.append({
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
            })

        return JsonResponse({
            'students': student_data,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'has_previous': page_obj.has_previous(),
            'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None
        })

    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'titles': titles,
        'courses': courses,
        'title_filter': title_filter,
        'course_filter': course_filter,
    })


def student_record(request, pk):
    """
    Display the details of a specific student and their related courses.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): The primary key of the student.

    Returns:
        HttpResponse: A rendered HTML response for the student record.
    """

    # TODO
    # student = Student.get_student(pk)
    # Mock data for demonstration purposes
    student = {'id': 5, 'first_name': 'Michael', 'last_name': 'Brown', 'email': 'michael.brown@example.com'}

    # Todo
    # courses = StudentCourse.get_courses_by_student(pk)
    # Mock data for demonstration purposes
    courses = [
        {"id": 1, "name": "Introduction to Programming",
         "description": "Learn the basics of programming using Python.", "start_date": "2024-01-10",
         "end_date": "2024-05-10", "title": 1},
        {"id": 2, "name": "Advanced Web Development",
         "description": "Explore advanced concepts in web development with Django and React.",
         "start_date": "2024-02-15", "end_date": "2024-06-30", "title": 1},
        {"id": 3, "name": "Database Management Systems",
         "description": "Understand the design, implementation, and management of database systems.",
         "start_date": "2024-03-01", "end_date": "2024-07-15", "title": 2},
        {"id": 4, "name": "Machine Learning Basics",
         "description": "An introduction to machine learning concepts and algorithms.", "start_date": "2024-04-05",
         "end_date": "2024-08-20", "title": 4}
    ]

    # TODO
    # titles = services_title.get_all_titles()
    # Mock data for demonstration purposes
    titles = [
        {"id": 1, "name": "Master in Artificial Intelligence"},
        {"id": 2, "name": "Master in Data Analytics"},
        {"id": 3, "name": "Master in Robotics"},
        {"id": 4, "name": "Master in Business Administration"}
    ]

    # TODO
    # course_grades = StudentCourse.get_courses_by_student(pk)
    # Mock data for demonstration purposes
    course_grades = [
        {"id": 1, "course_id": 1, "grade": 90},
        {"id": 2, "course_id": 2, "grade": 85},
        {"id": 3, "course_id": 3, "grade": 95},
        {"id": 4, "course_id": 4, "grade": 88}
    ]

    # TODO
    # activities_grades = StudentActivityGrade.get_student_activity_grades(pk)
    # Mock data for demonstration purposes
    activities_grades = [
        {"id": 1, "student": 5, "activity": 1, "grade": 90},
        {"id": 2, "student": 5, "activity": 2, "grade": 85},
        {"id": 3, "student": 5, "activity": 3, "grade": 95},
        {"id": 4, "student": 5, "activity": 4, "grade": 88}
    ]

    return render(request, 'students/student_record.html', {'student': student,
                                                            'titles': titles, 'courses': courses,
                                                            'course_grades': course_grades,
                                                            'activity_grades': activities_grades})


def modify_student(request):
    """
    Handle the modification of an existing student.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the student modification.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        student_id = data.get('id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        try:
            student = Student.get_student(student_id)
            if student:
                student.first_name = first_name
                student.last_name = last_name
                student.email = email
                student.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'failed'}, status=400)


def remove_student(request):
    """
    Handle the removal of a student.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the student removal.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        student_id = data.get('id')

        Student.delete(student_id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def de_enroll_courses(request):
    """
    Handle the de-enrollment of a student from courses.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the de-enrollment process.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        course_ids = data.get('course_ids', [])
        student = data.get('pk', None)

        Student.de_enroll_student_in_course(student, course_ids)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def enroll_courses(request):
    """
    Handle the enrollment of a student in courses.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the enrollment process.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        course_ids = data.get('course_ids', [])
        student = data.get('pk', None)
        Student.enroll_student_in_course(student, course_ids)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


# TODO Remove after testing
def get_activities_by_course_of_activity_grades(request):
    """
    Retrieve activities by course and their corresponding grades.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the activities and their grades.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        activities_grades = data.get('activities_grades', [])
        course_id = data.get('course_id', None)

        # activities = services_activity.get_activities_by_course(course_id)
        # Mock data for demonstration purposes
        activities = [
            {"id": 1, "name": "Assignment 1", "description": "Complete the first assignment.",
             "due_date": "2024-01-20", "course": 1},
            {"id": 2, "name": "Quiz 1", "description": "Take the first quiz.", "due_date": "2024-02-10", "course": 1},
            {"id": 3, "name": "Project Proposal", "description": "Submit the project proposal.",
             "due_date": "2024-03-05", "course": 1},
            {"id": 4, "name": "Midterm Exam", "description": "Prepare for the midterm exam.", "due_date": "2024-04-15",
             "course": 1},
            {"id": 5, "name": "Final Project", "description": "Complete the final project.", "due_date": "2024-05-30",
             "course": 1}
        ]

        activity_grades_dict = {grade['activity']: grade['grade'] for grade in activities_grades}

        activities_data = []
        for activity in activities:
            activities_data.append({
                'id': activity['id'],
                'name': activity['name'],
                'description': activity['description'],
                'due_date': activity['due_date'],
                'grade': activity_grades_dict.get(activity['id'], 'N/A')
            })

        return JsonResponse({'activities': activities_data})
    return JsonResponse({'status': 'failed'}, status=400)
