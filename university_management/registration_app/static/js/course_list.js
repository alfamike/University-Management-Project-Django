document.addEventListener('DOMContentLoaded', function () {
    // Add event listener for filter form submission
    document.getElementById('filter-form').addEventListener('submit', function (event) {
        event.preventDefault();

        // Get the selected title filter value
        const titleFilter = document.getElementById('title').value;
        const yearFilter = document.getElementById('year').value;

        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Update the URL to reflect the filter parameters
        const url = new URL(window.location.href);
        url.searchParams.set('title', titleFilter);
        url.searchParams.set('year', yearFilter);

        // Fetch the filtered courses data via AJAX
        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            }
        })
            .then(response => response.json())
            .then(data => {
                // Update the course list table
                const courseList = document.getElementById('course-list');
                courseList.innerHTML = ''; // Clear the current table rows

                // Populate the table with new data
                if (data.courses.length > 0) {
                    data.courses.forEach(course => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${course.name}</td>
                            <td>${course.description}</td>
                            <td>${course.start_date}</td>
                            <td>${course.end_date}</td>
                        `;
                        courseList.appendChild(row);
                    });
                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td colspan="2">No courses found.</td>`;
                    courseList.appendChild(row);
                }

                // Update pagination buttons
                const paginationContainer = document.querySelector('.pagination-container');
                paginationContainer.innerHTML = ''; // Clear current pagination

                // Build pagination buttons dynamically
                const pagination = document.createElement('div');
                pagination.classList.add('pagination');

                // Add 'First' and 'Previous' buttons if applicable
                if (data.has_previous) {
                    const firstButton = document.createElement('a');
                    firstButton.href = `?page=1&title=${titleFilter}`;
                    firstButton.textContent = 'First';
                    firstButton.classList.add('btn-page');
                    pagination.appendChild(firstButton);

                    const prevButton = document.createElement('a');
                    prevButton.href = `?page=${data.previous_page}&title=${titleFilter}`;
                    prevButton.textContent = 'Previous';
                    prevButton.classList.add('btn-page');
                    pagination.appendChild(prevButton);
                }

                // Add current page info
                const currentPage = document.createElement('span');
                currentPage.textContent = `Page ${data.current_page} of ${data.total_pages}`;
                currentPage.classList.add('current-page');
                pagination.appendChild(currentPage);

                // Add 'Next' and 'Last' buttons if applicable
                if (data.has_next) {
                    const nextButton = document.createElement('a');
                    nextButton.href = `?page=${data.next_page}&title=${titleFilter}`;
                    nextButton.textContent = 'Next';
                    nextButton.classList.add('btn-page');
                    pagination.appendChild(nextButton);

                    const lastButton = document.createElement('a');
                    lastButton.href = `?page=${data.total_pages}&title=${titleFilter}`;
                    lastButton.textContent = 'Last';
                    lastButton.classList.add('btn-page');
                    pagination.appendChild(lastButton);
                }

                paginationContainer.appendChild(pagination);
            })
            .catch(error => console.error('Error:', error));
    });

    // Add event listener for pagination buttons
    document.querySelector('.pagination-container').addEventListener('click', function (event) {
        if (event.target.classList.contains('btn-page')) {
            event.preventDefault();

            // Get the URL for the next/previous page
            const url = event.target.href;
            const titleFilter = document.getElementById('title').value;

            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    // Update the course list table
                    const courseList = document.getElementById('course-list');
                    courseList.innerHTML = ''; // Clear the current table rows

                    // Populate the table with new data
                    if (data.courses.length > 0) {
                        data.courses.forEach(course => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${course.name}</td>
                                <td>${course.description}</td>
                                <td>${course.start_date}</td>
                                <td>${course.end_date}</td>
                            `;
                            courseList.appendChild(row);
                        });
                    } else {
                        const row = document.createElement('tr');
                        row.innerHTML = `<td colspan="2">No courses found.</td>`;
                        courseList.appendChild(row);
                    }

                    // Update pagination buttons
                    const paginationContainer = document.querySelector('.pagination-container');
                    paginationContainer.innerHTML = ''; // Clear current pagination

                    // Build pagination buttons dynamically
                    const pagination = document.createElement('div');
                    pagination.classList.add('pagination');

                    // Add 'First' and 'Previous' buttons if applicable
                    if (data.has_previous) {
                        const firstButton = document.createElement('a');
                        firstButton.href = `?page=1&title=${titleFilter}`;
                        firstButton.textContent = 'First';
                        firstButton.classList.add('btn-page');
                        pagination.appendChild(firstButton);

                        const prevButton = document.createElement('a');
                        prevButton.href = `?page=${data.previous_page}&title=${titleFilter}`;
                        prevButton.textContent = 'Previous';
                        prevButton.classList.add('btn-page');
                        pagination.appendChild(prevButton);
                    }

                    // Add current page info
                    const currentPage = document.createElement('span');
                    currentPage.textContent = `Page ${data.current_page} of ${data.total_pages}`;
                    currentPage.classList.add('current-page');
                    pagination.appendChild(currentPage);

                    // Add 'Next' and 'Last' buttons if applicable
                    if (data.has_next) {
                        const nextButton = document.createElement('a');
                        nextButton.href = `?page=${data.next_page}&title=${titleFilter}`;
                        nextButton.textContent = 'Next';
                        nextButton.classList.add('btn-page');
                        pagination.appendChild(nextButton);

                        const lastButton = document.createElement('a');
                        lastButton.href = `?page=${data.total_pages}&title=${titleFilter}`;
                        lastButton.textContent = 'Last';
                        lastButton.classList.add('btn-page');
                        pagination.appendChild(lastButton);
                    }

                    paginationContainer.appendChild(pagination);
                })
                .catch(error => console.error('Error fetching pagination:', error));
        }
    });
});

