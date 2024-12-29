// Get CSRF token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const title_id = JSON.parse(document.getElementById('data').textContent);

document.getElementById('edit-title-btn').addEventListener('click', function() {
    document.getElementById('edit-title-popup').style.display = 'block';
});

document.getElementById('edit-title-popup').querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('edit-title-popup').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('edit-title-popup')) {
        document.getElementById('edit-title-popup').style.display = 'none';
    }
});

document.getElementById('edit-title-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const titleName = document.getElementById('edit-title-name').value;
    const titleDescription = document.getElementById('edit-title-description').value;
    const titlePublicationDate = document.getElementById('edit-title-publication-date').value;

    fetch(`/modifyTitle/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
            id: title_id,
            name: titleName,
            description: titleDescription,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to edit title information.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('delete-title-btn').addEventListener('click', function() {
    if (confirm('Are you sure you want to delete this title?')) {
        fetch(`/removeTitle/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: JSON.stringify({ id: title_id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/titles/';
            } else {
                alert('Failed to delete the title.');
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
