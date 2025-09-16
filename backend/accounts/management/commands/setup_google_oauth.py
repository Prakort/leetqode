from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider


class Command(BaseCommand):
    help = 'Set up Google OAuth2 app for authentication'

    def add_arguments(self, parser):
        parser.add_argument(
            '--client-id',
            type=str,
            help='Google OAuth2 Client ID',
        )
        parser.add_argument(
            '--client-secret',
            type=str,
            help='Google OAuth2 Client Secret',
        )

    def handle(self, *args, **options):
        client_id = options.get('client_id')
        client_secret = options.get('client_secret')
        
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.WARNING(
                    'Please provide both --client-id and --client-secret arguments.\n'
                    'Example: python manage.py setup_google_oauth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET'
                )
            )
            return

        # Get or create the default site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'LeetQode Development'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created site: {site.domain}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Using existing site: {site.domain}')
            )

        # Create or update Google OAuth2 app
        app, created = SocialApp.objects.get_or_create(
            provider=GoogleProvider.id,
            defaults={
                'name': 'Google OAuth2',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            app.client_id = client_id
            app.secret = client_secret
            app.save()
            self.stdout.write(
                self.style.SUCCESS('Updated existing Google OAuth2 app')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Created new Google OAuth2 app')
            )

        # Add the site to the app
        app.sites.add(site)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Google OAuth2 setup complete!\n'
                f'Client ID: {client_id}\n'
                f'App ID: {app.id}\n'
                f'Site: {site.domain}'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nNext steps:\n'
                '1. Make sure your Google OAuth2 redirect URI is set to:\n'
                f'   http://{site.domain}/auth/google/login/callback/\n'
                '2. Test the login at: http://localhost:3000/'
            )
        )
