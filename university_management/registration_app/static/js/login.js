document.getElementById('certificate-login-btn').addEventListener('click', async () => {
    const response = await fetch('login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    });

    const result = await response.json();
    if (result.success) {
        window.location.href = 'home/';
    } else {
        alert(`Login failed: ${result.error}`);
    }
});
