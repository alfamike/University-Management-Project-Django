document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.pagination-container').addEventListener('click', function (event) {
        if (event.target.classList.contains('btn-page')) {
            event.preventDefault();

            // Get the URL for the next/previous page
            const url = event.target.href;
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
                    const titleList = document.getElementById('title-list');
                    titleList.innerHTML = ''; // Clear the current table rows

                    // Populate the table with new data
                    data.titles.forEach(title => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${title.name}</td>
                            <td>${title.description}</td>
                        `;
                        titleList.appendChild(row);
                    });

                    // Update pagination buttons
                    const paginationContainer = document.querySelector('.pagination-container');
                    paginationContainer.innerHTML = ''; // Clear current pagination

                    // Build pagination buttons dynamically
                    const pagination = document.createElement('div');
                    pagination.classList.add('pagination');

                    // Add 'First' and 'Previous' buttons if applicable
                    if (data.has_previous) {
                        const firstButton = document.createElement('a');
                        firstButton.href = '?page=1';
                        firstButton.textContent = 'First';
                        firstButton.classList.add('btn-page');
                        pagination.appendChild(firstButton);

                        const prevButton = document.createElement('a');
                        prevButton.href = `?page=${data.previous_page}`;
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
                        nextButton.href = `?page=${data.next_page}`;
                        nextButton.textContent = 'Next';
                        nextButton.classList.add('btn-page');
                        pagination.appendChild(nextButton);

                        const lastButton = document.createElement('a');
                        lastButton.href = `?page=${data.total_pages}`;
                        lastButton.textContent = 'Last';
                        lastButton.classList.add('btn-page');
                        pagination.appendChild(lastButton);
                    }

                    paginationContainer.appendChild(pagination);
                })
                .catch(error => {
                    console.error('Error fetching pagination:', error);
                });
        }
    });
});