document.addEventListener('DOMContentLoaded', function() {
    setupScrollToBottomButton();
    setupSidebarToggle();
    setupNewChatCreation();
    initializeChatList();
    setupPromptInputBehavior();
    setupSearchBar();
    setupPromptSubmission();
});

function setupScrollToBottomButton() {
    const chatContent = document.getElementById('chat-content');
    const scrollToBottomButton = document.getElementById('scroll-to-bottom');

    chatContent.addEventListener('scroll', function() {
        if (chatContent.scrollTop + chatContent.clientHeight < chatContent.scrollHeight - 10) {
            scrollToBottomButton.classList.add('show');
        } else {
            scrollToBottomButton.classList.remove('show');
        }
    });

    scrollToBottomButton.addEventListener('click', function() {
        chatContent.scrollTop = chatContent.scrollHeight;
    });
}

function setupSidebarToggle() {
    document.getElementById('toggle-sidebar').addEventListener('click', function() {
        var sidebar = document.getElementById('sidebar');
        var main = document.querySelector('main');
        var h2 = sidebar.querySelector('h2');
        if (sidebar.style.width === '50px') {
            expandSidebar(sidebar, h2, this);
        } else {
            collapseSidebar(sidebar, main, h2, this);
        }
    });
}

function expandSidebar(sidebar, h2, toggleButton) {
    sidebar.style.width = '180px';
    h2.innerHTML = 'AutoComment';
    h2.style.fontSize = '1.5em';
    toggleButton.textContent = '⟪';
}

function collapseSidebar(sidebar, main, h2, toggleButton) {
    sidebar.style.width = '50px';
    main.style.marginLeft = '30px';
    main.style.marginRight = '-30px';
    h2.innerHTML = 'Auto<br>Comment';
    h2.style.textAlign = 'center';
    h2.style.fontSize = '1em';
    toggleButton.textContent = '⟫';
}

function setupNewChatCreation() {
    document.getElementById('new-chat').addEventListener('click', function() {
        const chatId = prompt('Enter new chat name:');
        if (chatId) {
            createNewChat(chatId);
        }
    });
}

function createNewChat(chatId) {
    fetch('/api/new_chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            addChatToList(chatId);
        }
    });
}

function addChatToList(chatId) {
    const chatList = document.getElementById('chat-list');
    const newChat = document.createElement('li');
    const newChatLink = document.createElement('a');
    newChatLink.href = '#';
    newChatLink.textContent = chatId;
    newChatLink.classList.add('chat-link');
    newChatLink.addEventListener('click', function(event) {
        event.preventDefault();
        switchChat(chatId);
    });
    newChat.appendChild(newChatLink);
    chatList.appendChild(newChat);
}

function switchChat(chatId) {
    // Save current chat history if any
    const currentChatId = getCurrentChatId();
    if (currentChatId) {
        saveChatHistory();
    }

    // Load the new chat history
    loadChatHistory(chatId);

    // Highlight the selected chat and unhighlight the others
    const chatLinks = document.querySelectorAll('#chat-list .chat-link');
    chatLinks.forEach(link => {
        link.classList.remove('active');
    });

    const selectedLink = Array.from(chatLinks).find(link => link.textContent === chatId);
    if (selectedLink) {
        selectedLink.classList.add('active');
    }
}

function getCurrentChatId() {
    return window.currentChatId || null;
}

function getChatHistory() {
    const chatContentElement = document.getElementById('chat-content');
    return chatContentElement.innerHTML;
}

function saveChatHistory() {
    const currentChatId = getCurrentChatId();
    if (currentChatId) {
        const chatHistory = getChatHistory();
        fetch('/api/save_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ chat_id: currentChatId, history: chatHistory })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                console.log(data.message);
            }
        })
        .catch(error => {
            console.error('Error saving chat history:', error);
            alert('Failed to save chat history: ' + error.message);
        });
    }
}

function loadChatHistory(chatId) {
    fetch(`/chats_history/${chatId}.json`)
        .then(response => response.json())
        .then(data => {
            // Display the chat history in the main area
            const chatContentElement = document.getElementById('chat-content');
            chatContentElement.innerHTML = data.history.join('<br>');
            // Update the current chat ID
            window.currentChatId = chatId;
        })
        .catch(error => {
            console.error('Error loading chat history:', error);
        });
}

function initializeChatList() {
    fetch('/chats_history/')
        .then(response => response.json())
        .then(data => {
            const chatList = document.getElementById('chat-list');
            chatList.innerHTML = '';
            data.forEach(chatId => {
                addChatToList(chatId);
            });
        });
}

function setupPromptInputBehavior() {
    const promptInput = document.getElementById('prompt-input');
    const sendPromptButton = document.getElementById('send-prompt');

    toggleSendButton(promptInput, sendPromptButton);
    promptInput.addEventListener('input', function() {
        toggleSendButton(promptInput, sendPromptButton);
        adjustPromptInputHeight(promptInput);
    });
    promptInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            submitPrompt(promptInput, sendPromptButton);
        }
    });
}

function toggleSendButton(promptInput, sendPromptButton) {
    sendPromptButton.disabled = !promptInput.value.trim();
}

function adjustPromptInputHeight(promptInput) {
    promptInput.style.height = 'auto';
    const scrollHeight = Math.min(promptInput.scrollHeight, 100);
    promptInput.style.height = `${scrollHeight}px`;
}

function setupSearchBar() {
    const searchBar = document.getElementById('search-bar');
    const chatContent = document.getElementById('chat-content');

    searchBar.addEventListener('input', function() {
        highlightSearchResults(this.value.toLowerCase(), chatContent);
    });
}

function highlightSearchResults(term, chatContent) {
    const messages = chatContent.querySelectorAll('.message');
    messages.forEach(message => {
        const originalText = message.textContent;
        if (originalText.toLowerCase().includes(term) && term !== '') {
            const regex = new RegExp(`(${term})`, 'gi');
            message.innerHTML = originalText.replace(regex, '<mark>$1</mark>');
        } else {
            message.innerHTML = originalText;
        }
    });
}

function setupPromptSubmission() {
    const promptInput = document.getElementById('prompt-input');
    const sendPromptButton = document.getElementById('send-prompt');

    sendPromptButton.addEventListener('click', function() {
        submitPrompt(promptInput, sendPromptButton);
    });
}

function submitPrompt(promptInput, sendPromptButton) {
    // Check if a chat ID is selected
    const currentChatId = getCurrentChatId();
    if (!currentChatId) {
        alert('Please select a chat before sending a prompt🥲.');
        return;
    }
    const userMessage = promptInput.value.trim();
    if (userMessage) {
        addMessage(userMessage, 'user-message');
        promptInput.value = '';
        sendPromptButton.disabled = true;
        promptInput.style.height = '45px'; // Reset to initial height

        // Add loading message
        addLoadingMessage();

        // Simulate model response
        fetch('/api/send_prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt_content: userMessage })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.error || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            // Remove loading message
            removeLoadingMessage();
            addMessage(data.comment, 'model-message'); // Display the model's response

            // Save the chat after receiving the response
            saveChatHistory();
        })
        .catch(error => {
            // Remove loading message
            removeLoadingMessage();
            console.error('Error:', error);
            alert('Failed to get response from the API: ' + error.message);
        })
        .finally(() => {
            // Re-enable send button
            sendPromptButton.disabled = !promptInput.value;
        });
    }
}

function resetPromptInputHeight(promptInput) {
    promptInput.style.height = '45px';
}

function disableSendButton(sendPromptButton) {
    sendPromptButton.disabled = true;
}

function addLoadingMessage() {
    const loadingMessage = document.createElement('div');
    loadingMessage.id = 'loadingMessage';
    loadingMessage.className = 'loading-message';
    loadingMessage.innerHTML = 'Generating response...';
    const chatContent = document.getElementById('chat-content');
    chatContent.appendChild(loadingMessage);
    chatContent.scrollTop = chatContent.scrollHeight;
}

function removeLoadingMessage() {
    const loadingMessage = document.getElementById('loadingMessage');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

function addMessage(content, className) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.innerHTML = content;

    const timestampElement = document.createElement('span');
    const timestamp = new Date().toLocaleString(); // Changed to include date and time
    timestampElement.className = 'message-timestamp';
    timestampElement.textContent = timestamp;

    const chatContent = document.getElementById('chat-content');
    messageElement.appendChild(timestampElement);
    chatContent.appendChild(messageElement);
    chatContent.scrollTop = chatContent.scrollHeight;
}

