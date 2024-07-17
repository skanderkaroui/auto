// Function to create and toggle chat interface
function toggleChatInterface() {
    const chatContainer = document.getElementById('auto-container');
    if (!chatContainer) {
        // Create container if it doesn't exist
        createChatInterface();
    } else {
        // Toggle display
        const isVisible = chatContainer.style.display === 'block';
        chatContainer.style.display = isVisible ? 'none' : 'block';
    }
}

// Function to create chat interface
function createChatInterface() {
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
    chatContainer.style.display = 'none'; // Initially hidden

    chatContainer.innerHTML = `
        <div id="auto-header" style="padding: 10px; background-color: #333; color: white;">
            <h2>Auto</h2>
            <button id="close-chat" style="float: right;" class="material-symbols-outlined">clear</button>
        </div>
        <div id="auto-content" style="padding: 10px; overflow-y: auto; height: calc(100% - 50px);">
            <!-- Chat interface goes here -->
        </div>
        <div id="auto-input" style="padding: 10px; position: absolute; bottom: 0; width: 100%;">
            <input type="text" id="chat-input" style="width: 80%; padding: 5px;" placeholder="Type a message...">
            <button id="send-message" style="width: 18%;">Send</button>
        </div>
    `;

    document.body.appendChild(chatContainer);

    // Close chat interface
    document.getElementById('close-chat').addEventListener('click', () => {
        chatContainer.style.display = 'none';
    });

    // Send message (sample logic)
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
}

// Listen for clicks on elements with class 'jsNRx'
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('jsNRx')) {
        toggleChatInterface();
    }
});

function addAutoChatButton() {
    // Find the first element with class 'tMdQNe'
    const firstElement = document.querySelector('.tMdQNe');

    if (firstElement) {
        // Create a new div
        const newDiv = document.createElement('div');
        newDiv.setAttribute('jscontroller', 'rYZP8b');
        newDiv.setAttribute('jsaction', 'JIbuQc:Dikcde;AJZkAd:uKBWVb;ntQuZe:uKBWVb');
        newDiv.classList.add('r6xAKc');

        // Add the button structure inside the new div
        newDiv.innerHTML = `
            <span data-is-tooltip-wrapper="true">
                <button class="VfPpkd-Bz112c-LgbsSe yHy1rc eT1oJ JsuyRc boDUxc"
                        jscontroller="soHxf"
                        jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;"
                        jsname="A5il2e"
                        data-disable-idom="true"
                        aria-label="Auto Chat"
                        data-tooltip-enabled="true"
                        data-tooltip-id="tt-auto-chat"
                        aria-pressed="false"
                        data-panel-id="2">
                    <div jsname="s3Eaab" class="VfPpkd-Bz112c-Jh9lGc"></div>
                    <div class="VfPpkd-Bz112c-J1Ukfc-LhBDec"></div>
                    <i aria-hidden="true" class="google-symbols ebW6mc NtU4hc">auto</i>
                    <i aria-hidden="true" class="google-symbols hi38gd Mwv9k">auto</i>
                </button>
                <div class="EY8ABd-OWXEXe-TAWMXe" role="tooltip" aria-hidden="true" id="tt-auto-chat">Auto Chat</div>
            </span>
            <div class="IxCbn spYiI" jscontroller="fIa6jf" jsaction="rcuQ6b:dWFD5d;qIX6cf:dWFD5d" style="display: none;"></div>
        `;

        // Append the new div inside the first 'tMdQNe' element
        firstElement.appendChild(newDiv);
    }
}

// Call the function to add the auto chat button
addAutoChatButton();
