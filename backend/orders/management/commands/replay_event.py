from django.core.management.base import BaseCommand
from outbox.replay import replay_dead_letter_event


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("event_id")

    def handle(self, *args, **options):
        event_id = options["event_id"]
        replay_dead_letter_event(event_id)
        self.stdout.write(
            self.style.SUCCESS(
                f"Replayed event {event_id}"
            )
        )