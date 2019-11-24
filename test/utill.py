import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_two.settings")

from iron_parser.models import GooseBase

gooses = GooseBase.objects.all()

for goose in gooses:
    print(goose.name)