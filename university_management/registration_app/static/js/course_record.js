// Get CSRF token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Get data from the data-container
const jsonData = JSON.parse(document.getElementById('data').textContent);
const course = JSON.parse(jsonData.course.replace(/'/g, '"'));
const activities = JSON.parse(jsonData.activities.replace(/'/g, '"'));

document.getElementById('add-activity-btn').addEventListener('click', function() {
    document.getElementById('add-activity-popup').style.display = 'block';
});

document.getElementById('add-activity-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('add-activity-popup').style.display = 'none';
});

document.getElementById('edit-course-btn').addEventListener('click', function() {
    document.getElementById('edit-course-popup').style.display = 'block';
});

document.getElementById('edit-course-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('edit-course-popup').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('add-activity-popup')) {
        document.getElementById('add-activity-popup').style.display = 'none';
    }

    if (event.target == document.getElementById('edit-course-popup')) {
        document.getElementById('edit-course-popup').style.display = 'none';
    }
});

document.getElementById('delete-activity-btn').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('.activity-checkbox:checked');
    const selectedActivities = Array.from(checkboxes).map(checkbox => checkbox.value);

    if (selectedActivities.length > 0) {
        if (confirm('Are you sure you want to remove the selected activities?')) {
            fetch(`/removeActivity/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({ activity_ids: selectedActivities })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove the selected activities from the table
                    selectedActivities.forEach(activityId => {
                        document.querySelector(`.course-checkbox[value="${activityId}"]`).closest('tr').remove();
                    });
                    location.reload();
                } else {
                    alert('Failed to remove activities.');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    } else {
        alert('No activities selected.');
    }

});


document.getElementById('add-activity-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const activity_name = document.getElementById('activity-name').value;
    const activity_description = document.getElementById('activity-description').value;
    const activity_due_date = document.getElementById('activity-due-date').value;

    fetch(`/createActivity/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ course_id: course_id, name: activity_name, description: activity_description,
        due_date: activity_due_date })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to add an activity.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('modify-activity-btn').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('.activity-checkbox:checked');
    if (checkboxes.length !== 1) {
        alert('Please select exactly one activity to modify.');
        return;
    }

    const activityId = checkboxes[0].value;
    const activityRow = checkboxes[0].closest('tr');
    const activityName = activityRow.querySelector('td:nth-child(2)').textContent;
    const activityDescription = activityRow.querySelector('td:nth-child(3)').textContent;
    const activityDueDate = activityRow.querySelector('td:nth-child(4)').textContent;

    document.getElementById('modify-activity-id').value = activityId;
    document.getElementById('modify-activity-name').value = activityName;
    document.getElementById('modify-activity-description').value = activityDescription;
    document.getElementById('modify-activity-due-date').value = activityDueDate;

    document.getElementById('modify-activity-popup').style.display = 'block';
});

document.getElementById('modify-activity-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('modify-activity-popup').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('modify-activity-popup')) {
        document.getElementById('modify-activity-popup').style.display = 'none';
    }
});

document.getElementById('modify-activity-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const activityId = document.getElementById('modify-activity-id').value;
    const activityName = document.getElementById('modify-activity-name').value;
    const activityDescription = document.getElementById('modify-activity-description').value;
    const activityDueDate = document.getElementById('modify-activity-due-date').value;

    fetch(`/modifyActivity/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ id: activityId, name: activityName, description: activityDescription, due_date: activityDueDate })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to modify the activity.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('edit-course-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const courseName = document.getElementById('edit-course-name').value;
    const courseDescription = document.getElementById('edit-course-description').value;
    const courseStartDate = document.getElementById('edit-course-start-date').value;
    const courseEndDate = document.getElementById('edit-course-end-date').value;

    fetch(`/modifyCourse/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
            id: course.id,
            name: courseName,
            description: courseDescription,
            start_date: courseStartDate,
            end_date: courseEndDate
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to edit course information.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('delete-course-btn').addEventListener('click', function() {
if (confirm('Are you sure you want to delete this course?')) {
    fetch(`/removeCourse/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ id: course.id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.href = '/courses/';
        } else {
            alert('Failed to delete the course.');
        }
    })
    .catch(error => console.error('Error:', error));
}
});
