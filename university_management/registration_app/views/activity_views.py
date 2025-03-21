import json

from django.http import JsonResponse

from registration_app.services_fabric.services_activity import Activity


def create_activity(request):
    """
    Handle the creation of a new activity.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the activity creation.
    """
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
    """
    Handle the removal of activities.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the activity removal.
    """
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
    """
    Handle the modification of an existing activity.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the activity modification.
    """
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


def manage_grade_to_activity(request):
    """
    Handle the assignment of a grade to a student for a specific activity.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the grade assignment.
    """
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
