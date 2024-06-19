class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            inputField: document.querySelector('.chatbox__footer input'),
            startRecordButton: document.querySelector('#start-record-btn'),
            stopRecordButton: document.querySelector('#stop-record-btn')
        }

        this.state = false;
        this.messages = [];
        this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        this.synth = window.speechSynthesis;
    }

    display() {
        const { openButton, chatBox, sendButton, startRecordButton, stopRecordButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });

        startRecordButton.addEventListener('click', () => this.startRecognition());
        stopRecordButton.addEventListener('click', () => this.stopRecognition());
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value;
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);

        fetch('/get-response/', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            textField.value = '';

            // Speak out the response
            this.speak(r.answer);
        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

    startRecognition() {
        this.recognition.start();
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.args.inputField.value = transcript;
            this.onSendButton(this.args.chatBox);
        };
    }

    stopRecognition() {
        this.recognition.stop();
    }

    speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        this.synth.speak(utterance);
    }
}

const chatbox = new Chatbox();
chatbox.display();

