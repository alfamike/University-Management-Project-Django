import json
import traceback

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from registration_app.services_fabric.services_title import Title


def create_title(request):
    """
    Handle the creation of a new title.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the title creation.
        HttpResponse: A rendered HTML response for the title creation form.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('title_name')
            description = data.get('title_description', '')

            title = Title(name=name, description=description)
            title.save()

            return JsonResponse({"success": True, "message": "Title created successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e) + f"Traceback: {traceback.format_exc()}"}, status=500)
    else:
        return render(request, 'titles/create_title.html')


def title_list(request):
    """
    Display a list of titles with pagination.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the paginated list of titles if the request is AJAX.
        HttpResponse: A rendered HTML response for the title list.
    """
    # TODO
    # titles = Title.all()
    # Mock data for demonstration purposes
    titles = [
        {
            "id": 1,
            "name": "Master in Artificial Intelligence",
            "description": "Test",
        },
        {
            "id": 2,
            "name": "Programación Lógica",
            "description": "Test",
        },
        {
            "id": 3,
            "name": "Master in Data Analytics",
            "description": "Test",
        },
        {
            "id": 4,
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


def title_record(request, pk):
    """
    Display the details of a specific title and its related courses.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): The primary key of the title.

    Returns:
        HttpResponse: A rendered HTML response for the title record.
    """
    # TODO
    # title = Title.get_title(pk)
    # Mock data for demonstration purposes
    title = {
        'id': 1,
        'name': 'Master in Artificial Intelligence',
        'description': 'A comprehensive program covering the latest trends in AI.'
    }

    # Fetch the related courses
    # TODO
    # courses = Course.get_courses_by_title(pk)
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

    return render(request, 'titles/title_record.html', {'title': title, 'courses': courses})


def modify_title(request):
    """
    Handle the modification of an existing title.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the title modification.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        title_id = data.get('id')
        name = data.get('name')
        description = data.get('description')

        try:
            title = Title.get_title(title_id)
            if title:
                title.name = name
                title.description = description
                title.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Title not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)


def remove_title(request):
    """
    Handle the removal of a title.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the title removal.
    """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        title_id = data.get('id', [])

        # Remove the selected titles
        # TODO
        # Title.get_title(title_id).delete()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
