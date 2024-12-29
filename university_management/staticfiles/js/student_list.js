// Handle filter form submission with AJAX
document.getElementById('filter-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const titleFilter = document.getElementById('title').value;
    const courseFilter = document.getElementById('course').value;

    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Update the URL to reflect filter parameters
    const url = new URL(window.location.href);
    url.searchParams.set('title', titleFilter);
    url.searchParams.set('course', courseFilter);

    // Fetch the filtered students data via AJAX
    fetch(url, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => response.json())
    .then(data => {
        const studentList = document.getElementById('student-list');
        studentList.innerHTML = '';

        data.students.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student.first_name} ${student.last_name}</td>
                <td>${student.email}</td>
            `;
            studentList.appendChild(row);
        });

        // Handle pagination logic
        const pagination = document.querySelector('.pagination');
        pagination.innerHTML = '';  // Clear the existing pagination

        if (data.has_next || data.previous_page) {
            const nextPageLink = document.createElement('a');
            nextPageLink.href = `?page=${data.next_page}&title=${titleFilter}&course=${courseFilter}`;
            nextPageLink.textContent = 'Next';
            nextPageLink.classList.add('btn-page');
            pagination.appendChild(nextPageLink);
        }

        if (data.previous_page) {
            const prevPageLink = document.createElement('a');
            prevPageLink.href = `?page=${data.previous_page}&title=${titleFilter}&course=${courseFilter}`;
            prevPageLink.textContent = 'Previous';
            prevPageLink.classList.add('btn-page');
            pagination.appendChild(prevPageLink);
        }
    })
    .catch(error => console.error('Error:', error));
});
