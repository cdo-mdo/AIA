"""Create, train, and query the ChatterBot conversational engine."""
from pathlib import Path

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from django.conf import settings

# Each list represents a small sample dialogue used for training.
TRAINING_CONVERSATIONS = [
    ["Hello", "Hello! How can I help you?"],
    ["Hi", "Hi! Nice to meet you."],
    ["Good morning! How are you doing?", "I am doing very well, thank you for asking."],
    ["How are you?", "I am doing well, thank you!"],
    ["What is your name?", "My name is Django ChatBot."],
    ["What can you do?", "I can answer simple questions from my training conversations."],
    ["Thank you", "You are welcome!"],
    ["You're welcome.", "It is nice chatting with you."],
    ["What is Django?", "Django is a web framework written in Python."],
    ["What is Python?", "Python is a general-purpose programming language."],
    ["Goodbye", "Goodbye! Have a wonderful day."],
]


def create_chatbot():
    """Return a chatbot with a persistent database stored in the project root."""
    database_file = Path(settings.BASE_DIR) / "chatterbot.sqlite3"
    return ChatBot(
        "Django ChatBot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=f"sqlite:///{database_file.as_posix()}",
        read_only=True,  # Do not add new statements while users chat.
    )


def train_chatbot(bot):
    """Teach the chatbot the example conversations before chatting."""
    trainer = ListTrainer(bot)
    for conversation in TRAINING_CONVERSATIONS:
        trainer.train(conversation)


def get_bot_reply(bot, user_message):
    """Generate a response for a non-empty user message."""
    if not user_message.strip():
        raise ValueError("A message must not be empty.")
    return str(bot.get_response(user_message))
