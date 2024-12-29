import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from registration_app.forms.form_course import CourseForm
from registration_app.services_fabric.services_course import Course
from registration_app.services_fabric.services_student_course_grade import StudentCourseGrade


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})


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


def modify_course(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        course_id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Modify the course
        # TODO: Update the course in the database
        try:
            course = Course.get_course(course_id)
            if course:
                course.name = name
                course.description = description
                course.start_date = start_date
                course.end_date = end_date
                course.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Course not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)


def remove_course(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        course_id = data.get('id', [])

        # Remove the selected courses
        # TODO
        # Course.get_course(course_id).delete()

        return JsonResponse({'status': 'success'})
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
