from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta

from tasks.models import Task


class Command(BaseCommand):
    help = 'Send reminder emails for tasks due within the next N hours (default 24)'

    def add_arguments(self, parser):
        parser.add_argument('--hours', type=int, default=24, help='Look ahead window in hours')
        parser.add_argument('--dry-run', action='store_true', help='Print reminders instead of sending emails')

    def handle(self, *args, **options):
        hours = options['hours']
        dry = options['dry_run']
        now = timezone.now()
        window = now + timedelta(hours=hours)

        qs = Task.objects.filter(
            completed=False,
            due_date__isnull=False,
            due_date__lte=window,
            due_date__gte=now,
        ).select_related('owner')

        count = 0
        for task in qs:
            owner = task.owner
            if not owner or not owner.email:
                continue

            # avoid sending repeated reminders if recently sent
            if task.last_reminder_sent and (now - task.last_reminder_sent).total_seconds() < (hours * 3600):
                continue

            subject = f"Reminder: '{task.title}' is due soon"
            message = f"Hi {owner.username},\n\nThis is a reminder that your task '{task.title}' is due on {task.due_date}.\n\nOpen your tasks: {settings.SITE_URL if hasattr(settings, 'SITE_URL') else ''}\n\n— ToDo"
            recipient = [owner.email]

            if dry:
                self.stdout.write(f"Would send to {owner.email}: {subject}")
            else:
                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)
                    task.last_reminder_sent = now
                    task.save(update_fields=['last_reminder_sent'])
                    self.stdout.write(f"Sent reminder to {owner.email} for task {task.pk}\n")
                except Exception as e:
                    self.stderr.write(f"Failed to send to {owner.email}: {e}\n")
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Processed {count} due tasks (lookahead {hours}h)."))
