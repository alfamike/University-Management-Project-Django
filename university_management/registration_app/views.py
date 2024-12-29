import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms.form_course import CourseForm
from .forms.form_student import StudentForm
from .forms.form_title import TitleForm
from .services_fabric.services_activity import Activity
from .services_fabric.services_course import Course
from .services_fabric.services_student import Student
from .services_fabric.services_student_course_grade import StudentCourseGrade


# login_hug("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")

# # Cargar el modelo y el tokenizador
# model_name = "meta-llama/Llama-3.1-405B"
# pipe = pipeline("text-generation", model=model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)


# def generate_response(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     outputs = model.generate(**inputs)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response


# def query_llama(request):
#     if request.method == "POST":
#         prompt = request.POST['prompt']
#         response = generate_response(prompt)
#         return JsonResponse({'response': response})
#
#     return render(request, 'templates/query_llama.html')

def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    return redirect('login')


def home(request):
    return render(request, 'home.html')


def chat_view(request):
    if request.method == 'POST':
        # Get the message from the POST request
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

            if not message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # You can process the message here (e.g., use a chatbot API like OpenAI or a custom response)
            response_message = f"Received your message: {message}"

            return JsonResponse({'response': response_message})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'students/create_student.html', {'form': form})


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})


def create_title(request):
    if request.method == 'POST':
        form = TitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('title_list')
    else:
        form = TitleForm()

    return render(request, 'titles/create_title.html', {'form': form})


def student_list(request):
    # Filters
    title_filter = request.GET.get('title', None)
    course_filter = request.GET.get('course', None)

    # Prepare the students list
    # TODO
    # students = Student.all()
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
    titles = [
        {"id": 1, "name": "Master in Artificial Intelligence"},
        {"id": 2, "name": "Master in Data Analytics"},
        {"id": 3, "name": "Master in Robotics"},
        {"id": 4, "name": "Master in Business Administration"}
    ]

    # Todo
    # courses = Course.all()
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


def title_list(request):
    # TODO
    # titles = Title.all()
    titles = [
        {
            "name": "Master in Artificial Intelligence",
            "description": "Test",
        },
        {
            "name": "Programación Lógica",
            "description": "Test",
        },
        {
            "name": "Master in Data Analytics",
            "description": "Test",
        },
        {
            "name": "Master in Business Administration",
            "description": "Test",
        }
    ]

    # Pagination setup
    paginator = Paginator(titles, 10)  # 10 titles per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page param
    try:
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        print(f"Error while getting page: {e}")
        page_obj = paginator.get_page(1)  # Default to first page if there's an issue

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        titles_data = []
        for title in page_obj:
            # TODO: Update the title data to match the actual model fields
            titles_data.append({
                'name': title["name"],
                'description': title["description"]
            })

        return JsonResponse({
            'titles': titles_data,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'has_previous': page_obj.has_previous(),
            'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'current_page': page_obj.number,
            'total_pages': page_obj.paginator.num_pages,
        })

    return render(request, 'titles/title_list.html', {
        'page_obj': page_obj,
    })


def course_list(request):
    # Todo
    # courses = Course.all()
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

    # Filters
    title_filter = request.GET.get('title', None)
    year_filter = request.GET.get('year', None)

    # Get filters for titles
    # TODO
    # titles = Title.all()
    titles = [
        {"id": 1, "name": "Master in Artificial Intelligence"},
        {"id": 2, "name": "Master in Data Analytics"},
        {"id": 3, "name": "Master in Robotics"},
        {"id": 4, "name": "Master in Business Administration"}
    ]

    # If invalid or empty, reset to None
    title_filter = None if title_filter in [None, '', 'None'] else title_filter
    year_filter = None if year_filter in [None, '', 'None'] else year_filter

    # Filter by title and year if provided
    if title_filter or year_filter:
        courses = Course.get_courses_by_title_year(title_filter, year_filter)

    # Filter for years
    years = list(range(2024, 2031))

    # Pagination setup
    paginator = Paginator(courses, 5)  # 5 courses per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page param
    try:
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        print(f"Error while getting page: {e}")
        page_obj = paginator.get_page(1)  # Default to first page if there's an issue

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        course_data = []
        for course in page_obj:
            # TODO: Update the course data to match the actual model fields
            course_data.append({
                'id': course["id"],
                'name': course["name"],
                'description': course["description"],
                'start_date': course["start_date"],
                'end_date': course["end_date"]
            })

        return JsonResponse({
            'courses': course_data,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'has_previous': page_obj.has_previous(),
            'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'current_page': page_obj.number,
            'total_pages': page_obj.paginator.num_pages,
        })

    return render(request, 'courses/course_list.html', {
        'page_obj': page_obj,
        'titles': titles,
        'years': years,
        'title_filter': title_filter,
        'year_filter': year_filter,
    })


def student_record(request, pk):
    student = {
        'id': 5, 'first_name': 'Michael', 'last_name': 'Brown', 'email': 'michael.brown@example.com', 'courses': [
            {"id": 1, "name": "Introduction to Programming",
             "description": "Learn the basics of programming using Python.", "start_date": "2024-01-10",
             "end_date": "2024-05-10"},
            {"id": 2, "name": "Advanced Web Development",
             "description": "Explore advanced concepts in web development with Django and React.",
             "start_date": "2024-02-15", "end_date": "2024-06-30"}, ]}

    # TODO
    # student = Student.get_student(pk)

    # Todo
    # courses = StudentCourse.get_courses_by_student(pk)
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
    titles = [
        {"id": 1, "name": "Master in Artificial Intelligence"},
        {"id": 2, "name": "Master in Data Analytics"},
        {"id": 3, "name": "Master in Robotics"},
        {"id": 4, "name": "Master in Business Administration"}
    ]

    # TODO
    # course_grades = StudentCourseGrade.get_student_course_grades(pk)
    course_grades = [
        {"id": 1, "course_id": 1, "grade": 90},
        {"id": 2, "course_id": 2, "grade": 85},
        {"id": 3, "course_id": 3, "grade": 95},
        {"id": 4, "course_id": 4, "grade": 88}
    ]

    # TODO
    # activities_grades = StudentActivityGrade.get_student_activity_grades(pk)
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


def delete_student(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        student_id = data.get('id')

        Student.delete(student_id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def de_enroll_courses(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        course_ids = data.get('course_ids', [])
        student = data.get('pk', None)

        Student.de_enroll_student_in_course(student, course_ids)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def enroll_courses(request):
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
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        activities_grades = data.get('activities_grades', [])
        course_id = data.get('course_id', None)

        # activities = services_activity.get_activities_by_course(course_id)
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


def manage_grade_to_course(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        grade = int(data.get('grade'))

        # TODO
        StudentCourseGrade(student_id=student_id, course_id=course_id, grade=grade).save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def course_record(request, pk):
    # Todo
    # course = Course.get_course(pk)
    course = {"id": 4, "name": "Machine Learning Basics",
              "description": "An introduction to machine learning concepts and algorithms.", "start_date": "2024-04-05",
              "end_date": "2024-08-20", "title": 4}

    # Fetch the related activities
    # TODO
    # activities = Activity.get_activities_by_course(pk)
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

    return render(request, 'courses/course_record.html', {
        'course': course,
        'activities': activities
    })


def manage_grade_to_activity(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        activity_id = data.get('activity_id')
        grade = int(data.get('grade'))

        # TODO
        # StudentActivityGrade(student_id=student_id, activity_id=activity_id, grade=grade).save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def create_activity(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        due_date = data.get('due_date')
        course_id = data.get('course_id')

        # Create the new activity
        # TODO
        Activity(name=name, description=description, due_date=due_date, course_id=course_id).save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def remove_activity(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        activity_ids = data.get('activity_ids', [])

        # Remove the selected activities
        # TODO
        # for activity in activity_ids:
        #  Activity.get_activity(activity['id']).delete()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def modify_activity(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        activity_id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        due_date = data.get('due_date')

        # Modify the activity
        # TODO: Update the activity in the database

        try:
            activity = Activity.get_activity(activity_id)
            if activity:
                activity.name = name
                activity.description = description
                activity.due_date = due_date
                activity.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)
