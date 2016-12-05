import os
import time
from subprocess import call

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from django.conf import settings
from django.core.management.base import BaseCommand


class AnyChangeHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        print(event)
        call(['python', 'manage.py', 'collectstatic', '--no-input'])


class Command(BaseCommand):
    help = 'Less watcher'

    def handle(self, *args, **options):
        path = os.path.join(settings.PROJECT_DIR, 'static', 'less')
        event_handler = AnyChangeHandler()

        self.stdout.write('Starting less watcher on directory: %s' % path)

        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()