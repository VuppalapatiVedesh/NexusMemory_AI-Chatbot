/* 
  script.js
  
  Controls client-side UI actions, message rendering, history restoration, 
  and markdown parsing with syntax highlighting.
*/

// SVG markup for beautiful, self-contained avatars
const AI_AVATAR_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bot" style="width: 18px; height: 18px; display: block;"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>`;
const USER_AVATAR_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user" style="width: 18px; height: 18px; display: block;"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;

document.addEventListener("DOMContentLoaded", () => {
    // DOM elements
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const messagesContainer = document.getElementById("messages-container");
    const welcomeCard = document.getElementById("welcome-card");
    const clearChatBtnSidebar = document.getElementById("clear-chat-btn-sidebar");
    const clearChatBtnHeader = document.getElementById("clear-chat-btn-header");
    const errorBanner = document.getElementById("error-banner");
    const errorText = errorBanner.querySelector(".error-text");
    const sendBtn = document.getElementById("send-btn");

    // Configure Marked.js to parse Markdown and use Highlight.js for code highlights
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(code, { language: lang }).value;
                } catch (e) {}
            }
            return hljs.highlightAuto(code).value;
        },
        breaks: true,
        gfm: true
    });

    // Load conversation history from session on page load
    loadChatHistory();

    // Event listener: Send Message Form Submission
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        sendMessage();
    });

    // Event listener: Clear Chat (Sidebar and Header buttons)
    clearChatBtnSidebar.addEventListener("click", confirmAndClearChat);
    clearChatBtnHeader.addEventListener("click", confirmAndClearChat);

    /**
     * Sends the user's message to the server and handles the response.
     */
    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Hide welcome card if visible
        hideWelcomeCard();
        hideError();

        // 1. Render user message locally
        appendMessageBubble("user", text);
        
        // Clear input and reset focus
        userInput.value = "";
        userInput.focus();
        
        // 2. Disable input fields during API call
        setInputDisabledState(true);

        // 3. Show typing indicator
        const typingIndicator = showTypingIndicator();
        scrollToBottom();

        try {
            // 4. Perform POST request to Flask app
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            // Remove typing indicator immediately
            typingIndicator.remove();

            if (response.ok && data.status === "success") {
                // 5. Render assistant's markdown response
                appendMessageBubble("assistant", data.response);
            } else {
                // Render error message in the error banner
                showError(data.message || "An error occurred while generating a response.");
            }
        } catch (err) {
            if (typingIndicator) typingIndicator.remove();
            showError("Could not connect to the server. Please check if the Flask backend is running.");
            console.error("Fetch error:", err);
        } finally {
            // Re-enable inputs
            setInputDisabledState(false);
            userInput.focus();
            scrollToBottom();
        }
    }

    /**
     * Appends a message bubble (user or assistant) to the chat feed container.
     */
    function appendMessageBubble(role, content) {
        const bubble = document.createElement("div");
        bubble.classList.add("message-bubble", role);

        // Create avatar element
        const avatar = document.createElement("div");
        avatar.classList.add("message-avatar");
        avatar.innerHTML = role === "user" ? USER_AVATAR_SVG : AI_AVATAR_SVG;

        // Create content block
        const contentDiv = document.createElement("div");
        contentDiv.classList.add("message-content");

        if (role === "user") {
            // Users are simple text. Prevent XSS by treating as textContent.
            contentDiv.textContent = content;
        } else {
            // Assistants send Markdown. Parse with marked.js.
            contentDiv.innerHTML = marked.parse(content);
            
            // Highlight code blocks inside the parsed markdown
            contentDiv.querySelectorAll("pre code").forEach((block) => {
                hljs.highlightElement(block);
            });
        }

        bubble.appendChild(avatar);
        bubble.appendChild(contentDiv);
        messagesContainer.appendChild(bubble);
        scrollToBottom();
    }

    /**
     * Displays the bouncing dot typing indicator.
     */
    function showTypingIndicator() {
        const indicator = document.createElement("div");
        indicator.classList.add("typing-indicator-container");
        indicator.id = "typing-indicator";

        const avatar = document.createElement("div");
        avatar.classList.add("message-avatar");
        avatar.innerHTML = AI_AVATAR_SVG;

        const dots = document.createElement("div");
        dots.classList.add("typing-indicator-dots");
        dots.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;

        indicator.appendChild(avatar);
        indicator.appendChild(dots);
        messagesContainer.appendChild(indicator);
        return indicator;
    }

    /**
     * Loads the existing chat history from the session storage on the server.
     */
    async function loadChatHistory() {
        try {
            const response = await fetch("/history");
            const data = await response.json();
            
            if (response.ok && data.status === "success" && data.history.length > 0) {
                hideWelcomeCard();
                data.history.forEach((msg) => {
                    appendMessageBubble(msg.role, msg.content);
                });
                scrollToBottom();
            }
        } catch (err) {
            console.error("Failed to load chat history:", err);
        }
    }

    /**
     * Sends a request to clear the server's session memory and resets the UI.
     */
    async function confirmAndClearChat() {
        if (!confirm("Are you sure you want to clear the conversation history? This will reset the chatbot's memory.")) {
            return;
        }

        try {
            const response = await fetch("/clear", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const data = await response.json();

            if (response.ok && data.status === "success") {
                // Clear DOM messages
                // Keep only the welcome card if present, otherwise remove all elements
                messagesContainer.innerHTML = "";
                
                // Show welcome card again
                showWelcomeCard();
                hideError();
            } else {
                showError("Could not clear the conversation history.");
            }
        } catch (err) {
            showError("Error connecting to the server to reset history.");
            console.error("Clear error:", err);
        }
    }

    /**
     * Disables or enables inputs during transmission states.
     */
    function setInputDisabledState(disabled) {
        userInput.disabled = disabled;
        sendBtn.disabled = disabled;
    }

    /**
     * Scrolls the chat container directly to the bottom.
     */
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    /**
     * Hides the initial welcome card from display.
     */
    function hideWelcomeCard() {
        if (welcomeCard) {
            welcomeCard.style.display = "none";
        }
    }

    /**
     * Restores the welcome card.
     */
    function showWelcomeCard() {
        if (welcomeCard) {
            welcomeCard.style.display = "block";
            // Re-append welcome card as it might have been cleared out by innerHTML resets
            messagesContainer.appendChild(welcomeCard);
        }
    }

    /**
     * Shows the error banner.
     */
    function showError(message) {
        errorText.textContent = message;
        errorBanner.classList.remove("hidden");
    }

    /**
     * Hides the error banner.
     */
    function hideError() {
        errorBanner.classList.add("hidden");
        errorText.textContent = "";
    }

    // Expose close error function globally
    window.hideError = hideError;

    // Expose prompt selection function globally
    window.useSuggestedPrompt = function(promptText) {
        userInput.value = promptText;
        sendMessage();
    };
});
