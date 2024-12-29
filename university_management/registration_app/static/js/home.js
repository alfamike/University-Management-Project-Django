// Get DOM elements
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');

// Function to send the user message to the server
function sendMessage() {
    const message = userInput.value;
    if (!message) return; // Don't send empty messages

    // Append user message to chat container
    chatContainer.innerHTML += `<div class="user-message">${message}</div>`;
    scrollToBottom();

    userInput.value = ''; // Clear input box

    // Get CSRF token from the document
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send message to the Django server using AJAX (fetch API)
    fetch('/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        // Append server response to chat container
        chatContainer.innerHTML += `<div class="bot-message">${data.response}</div>`;
        scrollToBottom();
    })
    .catch(error => {
        console.error('Error:', error);
        chatContainer.innerHTML += `<div class="bot-message">Sorry, there was an issue processing your message. Please try again later.</div>`;
        scrollToBottom();
    });
}

// Handle Enter key press to send message
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Scroll to the bottom of the chat container
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
