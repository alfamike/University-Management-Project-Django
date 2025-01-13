document.getElementById('create-student-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const first_name = document.getElementById('student_first_name').value;
    const last_name = document.getElementById('student_last_name').value;
    const email = document.getElementById('student_email').value;

    try {
        const response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ first_name, last_name, email })
        });

        const result = await response.json();
        if (result.success) {
            window.location.href = '/students/';
        } else {
            alert('Failed to create student. Please try again.');
            console.error('Error submitting the form:', result.error);
        }
    } catch (error) {
        console.error('Error submitting the form:', error);
        alert('An error occurred. Please try again later.');
    }
});
