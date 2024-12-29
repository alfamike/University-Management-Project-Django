// Get CSRF token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Get data from the data-container
const jsonData = JSON.parse(document.getElementById('data').textContent);
const student = JSON.parse(jsonData.student.replace(/'/g, '"'));
const courses = JSON.parse(jsonData.courses.replace(/'/g, '"'));
const titles = JSON.parse(jsonData.titles.replace(/'/g, '"'));
const course_grades = JSON.parse(jsonData.course_grades.replace(/'/g, '"'));
const activity_grades = JSON.parse(jsonData.activity_grades.replace(/'/g, '"'));


document.addEventListener('DOMContentLoaded', function() {
    const titleSelect = document.getElementById('course-title');
    const courseSelect = document.getElementById('course-name');
    const courseSelect2 = document.getElementById('course-grade-select');

    // Populate titles dropdown
    titles.forEach(title => {
        const option = document.createElement('option');
        option.value = title.id;
        option.textContent = title.name;
        titleSelect.appendChild(option);
    });

    // Event listener for title selection change
    titleSelect.addEventListener('change', function() {
        const titleId = parseInt(this.value);
        courseSelect.innerHTML = ''; // Clear previous options

        // Filter and populate courses based on selected title
        courses.filter(course => course.title === titleId).forEach(course => {
            const option = document.createElement('option');
            option.value = course.id;
            option.textContent = course.name;
            courseSelect.appendChild(option);
        });
    });

    // Populate course dropdown for managing grades
    courses.forEach(course => {
        const option = document.createElement('option');
        option.value = course.id;
        option.textContent = course.name;
        courseSelect2.appendChild(option);
    });

    // Event listener for "Show Activities" button
    document.getElementById('show-activities-course-btn').addEventListener('click', function() {
        const selectedCheckboxes = document.querySelectorAll('.course-checkbox:checked');
        const activitiesTableBody = document.getElementById('activities-table-body');
        const activitiesSection = document.getElementById('activities-section');

        if (selectedCheckboxes.length === 1) {
            const selectedCourseId = selectedCheckboxes[0].value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch('/get_activities_by_course_of_activity_grades/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    course_id: selectedCourseId,
                    activities_grades: activity_grades
                })
            })
            .then(response => response.json())
            .then(data => {
                activitiesTableBody.innerHTML = ''; // Clear previous activities
                const activityGradeSelect = document.getElementById('activity-grade-select');
                activityGradeSelect.innerHTML = ''; // Clear previous options

                data.activities.forEach(activity => {
                    const row = `
                        <tr>
                            <td>${activity.name}</td>
                            <td>${activity.description}</td>
                            <td>${activity.due_date}</td>
                            <td>${activity.grade}</td>
                        </tr>
                    `;
                    activitiesTableBody.insertAdjacentHTML('beforeend', row);

                    // Populate activities dropdown for managing grades

                    const option = document.createElement('option');
                    option.value = activity.id;
                    option.textContent = activity.name;
                    activityGradeSelect.appendChild(option);

                });

                activitiesSection.style.display = 'block';
            })
            .catch(error => console.error('Error:', error));
        } else {
            activitiesSection.style.display = 'none';
            alert('Please select exactly one course to view activities.');
            return;
        }
    });
});

document.getElementById('add-course-btn').addEventListener('click', function() {
    document.getElementById('add-course-popup').style.display = 'block';
});

document.getElementById('manage-grade-btn').addEventListener('click', function() {
    document.getElementById('manage-grade-popup').style.display = 'block';
});

document.getElementById('manage-activity-btn').addEventListener('click', function() {
    document.getElementById('manage-grade-activity-popup').style.display = 'block';
});

document.getElementById('add-course-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('add-course-popup').style.display = 'none';
});

document.getElementById('manage-grade-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('manage-grade-popup').style.display = 'none';
});

document.getElementById('manage-grade-activity-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('manage-grade-activity-popup').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('add-course-popup')) {
        document.getElementById('add-course-popup').style.display = 'none';
    }

    if (event.target == document.getElementById('manage-grade-popup')) {
        document.getElementById('manage-grade-popup').style.display = 'none';
    }

    if (event.target == document.getElementById('manage-grade-activity-popup')) {
        document.getElementById('manage-grade-activity-popup').style.display = 'none';
    }
});

document.getElementById('delete-course-btn').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('.course-checkbox:checked');
    const selectedCourses = Array.from(checkboxes).map(checkbox => checkbox.value);

    if (selectedCourses.length > 0) {
        if (confirm('Are you sure you want to delete these courses?')) {
            fetch(`/deEnrollCourses/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({ course_ids: selectedCourses, pk: student.id })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove the selected courses from the table
                    selectedCourses.forEach(courseId => {
                        document.querySelector(`.course-checkbox[value="${courseId}"]`).closest('tr').remove();
                    });
                    location.reload();
                } else {
                    alert('Failed to de-enroll courses.');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    } else {
        alert('No courses selected.');
    }

});


document.getElementById('add-course-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const course = document.getElementById('course-name').value;

    fetch(`/enrollCourses/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ course_id: course , pk: student.id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to enroll in course.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('manage-grade-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const courseId = document.getElementById('course-grade-select').value;
    const grade = document.getElementById('grade-input').value;

    fetch(`/manageGradeToCourse/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
            student_id: student.id,
            course_id: courseId,
            grade: grade
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to manage grade.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('manage-grade-activity-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const activityId = document.getElementById('activity-grade-select').value;
    const grade = document.getElementById('activity-grade-input').value;

    fetch(`/manageGradeToActivity/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
            student_id: student.id,
            activity_id: activityId,
            grade: grade
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to manage grade.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('edit-student-btn').addEventListener('click', function() {
    document.getElementById('edit-student-popup').style.display = 'block';
});

document.getElementById('edit-student-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('edit-student-popup').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('edit-student-popup')) {
        document.getElementById('edit-st-student-popup').style.display = 'none';
    }
});

document.getElementById('edit-student-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const firstName = document.getElementById('edit-first-name').value;
    const lastName = document.getElementById('edit-last-name').value;
    const email = document.getElementById('edit-email').value;

    fetch(`/modifyStudent/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
            id: student.id,
            first_name: firstName,
            last_name: lastName,
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to edit student information.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('delete-student-btn').addEventListener('click', function() {
    if (confirm('Are you sure you want to delete this student?')) {
        fetch(`/removeStudent/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: JSON.stringify({ id: student.id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/students/'; // Redirect to the students list page
            } else {
                alert('Failed to remove student.');
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
