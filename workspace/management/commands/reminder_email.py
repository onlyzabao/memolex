from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workspace.models import Package
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Sends a reminder email.'

    def handle(self, *args, **options):
        # Get today's date
        today = timezone.now().date()

        # Get all users
        users = User.objects.all()

        for user in users:
            # Get the user's profile
            packages = Package.objects.filter(user=user).order_by("date")

            for package in packages:
                if package.date == today:
                    html = render_to_string('reminder_email.html', {
                        'user': user,
                        'package': package
                    })

                    email = EmailMessage(
                        'Reminder: Time to study',
                        html,
                        'your@email.com',
                        [user.email],
                    )

                    email.send()

        self.stdout.write(self.style.SUCCESS('Successfully sent reminder email.'))
