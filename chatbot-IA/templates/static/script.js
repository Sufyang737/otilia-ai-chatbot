document.addEventListener("DOMContentLoaded", function() {
    var chatContainer = document.getElementById("chat-container");
    var chatForm = document.getElementById("chat-form");
    var userInput = document.getElementById("user-input");
    var userMessages = document.getElementById("user-messages");
    var chatbotMessages = document.getElementById("chatbot-messages");
    var loader = document.getElementById("loader");

    chatForm.addEventListener("submit", function(event) {
        event.preventDefault();
        var userMessage = userInput.value;
        userInput.value = "";

        var userMessageElement = document.createElement("div");
        userMessageElement.textContent = "You: " + userMessage;
        userMessageElement.classList.add("user-message");
        userMessages.appendChild(userMessageElement);

        loader.style.display = "block";

        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "user_input=" + encodeURIComponent(userMessage)
        })
        .then(function(response) {
            return response.text();
        })
        .then(function(response) {
            var chatbotResponseElement = document.createElement("div");
            chatbotResponseElement.textContent = "Chatbot: " + response;
            chatbotResponseElement.classList.add("chatbot-message");
            chatbotMessages.appendChild(chatbotResponseElement);
            loader.style.display = "none";
        });
    });
});