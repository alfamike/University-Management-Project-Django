const jsonData = JSON.parse(document.getElementById('data').textContent);
const titles = JSON.parse(jsonData.titles.replace(/'/g, '"'));

document.getElementById('create-course-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const title = document.getElementById('title').value;
    const name = document.getElementById('course_name').value;
    const description = document.getElementById('course_description').value;
    const startdate = document.getElementById('course_start_date').value;
    const enddate = document.getElementById('course_end_date').value;

    try {
        const response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ title, name, description, startdate, enddate })
        });

        const result = await response.json();
        if (result.success) {
            window.location.href = '/courses/';
        } else {
            alert('Failed to create course. Please try again.');
            console.error('Error submitting the form:', result.error);
        }
    } catch (error) {
        console.error('Error submitting the form:', error);
        alert('An error occurred. Please try again later.');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const titlesDropdown = document.getElementById('titles-dropdown');

    titles.forEach(title => {
        const option = document.createElement('option');
        option.value = title.id;
        option.textContent = title.name;
        titlesDropdown.appendChild(option);
    });
});