"""Run the chatbot in a Django-powered terminal session."""
from django.core.management.base import BaseCommand, CommandError
from chat.bot_service import create_chatbot, get_bot_reply, train_chatbot


class Command(BaseCommand):
    help = "Train and chat with ChatterBot in the terminal"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-training",
            action="store_true",
            help="Reuse existing chatbot training data",
        )

    def handle(self, *args, **options):
        try:
            bot = create_chatbot()
            if not options["skip_training"]:
                self.stdout.write("Training the chatbot (may take a moment)...")
                train_chatbot(bot)
        except Exception as exc:
            raise CommandError(f"Unable to initialize chatbot: {exc}") from exc

        self.stdout.write("ChatBot is ready. Type 'exit' or 'quit' to end.")
        while True:
            try:
                message = input("user: ").strip()
            except (EOFError, KeyboardInterrupt):
                self.stdout.write("\nbot: Goodbye!")
                break

            if message.lower() in {"exit", "quit"}:
                self.stdout.write("bot: Goodbye!")
                break
            if not message:
                self.stdout.write("bot: Please enter a message.")
                continue

            try:
                self.stdout.write(f"bot: {get_bot_reply(bot, message)}")
            except Exception as exc:
                self.stderr.write(f"Could not generate a response: {exc}")
