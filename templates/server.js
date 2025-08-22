const loadingIndicator = document.createElement('div');
loadingIndicator.classList.add('loading');
loadingIndicator.innerText = 'Loading...';

document.getElementById('sendButton').onclick = function() {
    const userInput = document.getElementById('userInput').value.trim();
    if (!userInput) return;

    document.getElementById('userInput').value = '';
    const messagesDiv = document.getElementById('messages');

    messagesDiv.innerHTML += `<div class="message user-message"><strong>You:</strong> ${userInput}</div>`;
    messagesDiv.appendChild(loadingIndicator);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to bottom

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        messagesDiv.innerHTML += `<div class="message bot-message"><strong>Bot:</strong> ${data.response}</div>`;
        messagesDiv.removeChild(loadingIndicator); // Remove loading indicator
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        messagesDiv.innerHTML += `<div class="message bot-message"><strong>Bot:</strong> Sorry, something went wrong!</div>`;
        messagesDiv.removeChild(loadingIndicator); // Remove loading indicator
    });
};
