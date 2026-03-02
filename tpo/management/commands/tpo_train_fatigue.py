from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from tpo.ml.trainer import train_from_csv


class Command(BaseCommand):
    help = 'Train fatigue classification model from a CSV file. Optionally evaluate on a test CSV.'

    def add_arguments(self, parser):
        parser.add_argument('--csv', required=True, help='Path to training CSV')
        parser.add_argument('--test', required=False, help='Optional path to test CSV')
        parser.add_argument('--target', default='fatigue_level', help='Target column name')

    def handle(self, *args, **options):
        csv_path = options['csv']
        test_path = options.get('test')
        target = options['target']

        if not Path(csv_path).exists():
            raise CommandError(f'Training CSV not found: {csv_path}')
        if test_path and not Path(test_path).exists():
            raise CommandError(f'Test CSV not found: {test_path}')

        result = train_from_csv(csv_path, test_csv_path=test_path, target_col=target)
        self.stdout.write(self.style.SUCCESS(
            f"Training complete. Accuracy: {result['accuracy']*100:.2f}%\n"
            f"Model: {result['model_path']}\nMeta: {result['meta_path']}"
        ))
