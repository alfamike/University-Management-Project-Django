document.getElementById('create-title-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const name = document.getElementById('title_name').value;
    const description = document.getElementById('title_description').value;

    try {
        const response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ name, description })
        });

        const result = await response.json();
        if (result.success) {
            window.location.href = '/titles/';
        } else {
            alert('Failed to create title. Please try again.');
            console.error('Error submitting the form:', result.error);
        }
    } catch (error) {
        console.error('Error submitting the form:', error);
        alert('An error occurred. Please try again later.');
    }
});
