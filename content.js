// Create a container for the chat interface
const chatContainer = document.createElement('div');
chatContainer.id = 'auto-container';
chatContainer.style.position = 'fixed';
chatContainer.style.right = '0';
chatContainer.style.top = '0';
chatContainer.style.width = '300px';
chatContainer.style.height = '100%';
chatContainer.style.backgroundColor = 'white';
chatContainer.style.zIndex = '9999';
chatContainer.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.5)';
document.body.appendChild(chatContainer);

// Add chat interface to the container
chatContainer.innerHTML = `
  <div id="auto-header" style="padding: 10px; background-color: #333; color: white;">
    <h2>Auto</h2>
    <button id="close-chat" style="float: right;" class="material-symbols-outlined">clear</button> <!-- Changed close button to use Material Symbols icon -->
  </div>
  <div id="auto-content" style="padding: 10px; overflow-y: auto; height: calc(100% - 50px);">
    <!-- Chat interface goes here -->
  </div>
  <div id="auto-input" style="padding: 10px; position: absolute; bottom: 0; width: 100%;">
    <input type="text" id="chat-input" style="width: 80%; padding: 5px;" placeholder="Type a message...">
    <button id="send-message" style="width: 18%;">Send</button>
  </div>
`;

// Close chat interface
document.getElementById('close-chat').addEventListener('click', () => {
    chatContainer.style.display = 'none';
});

// Send message
document.getElementById('send-message').addEventListener('click', () => {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value;
    if (message.trim() !== '') {
        const chatContent = document.getElementById('auto-content');
        chatContent.innerHTML += `<div style="padding: 10px; border-bottom: 1px solid #ccc;">${message}</div>`;
        chatInput.value = '';

        // TODO: Add logic to send message to Auto and display response
    }
});