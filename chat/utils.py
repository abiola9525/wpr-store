import random
import json
import torch
from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize

class ChatBot:
    def __init__(self):
        # Load the intents file
        with open('chat/intents.json', 'r') as f:
            self.intents = json.load(f)

        # Load the pre-trained model
        FILE = "chat/data.pth"
        data = torch.load(FILE)

        self.input_size = data["input_size"]
        self.hidden_size = data["hidden_size"]
        self.output_size = data["output_size"]
        self.all_words = data["all_words"]
        self.tags = data["tags"]
        model_state = data["model_state"]

        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size)
        self.model.load_state_dict(model_state)
        self.model.eval()

        self.bot_name = "WPR Bot"

    def get_response(self, sentence):
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in self.intents["intents"]:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])

        return "I do not understand..."
