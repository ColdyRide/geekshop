from django.core.management.base import BaseCommand
from geekshop.settings import BASE_DIR
import os
import chardet


def encoding_dump(file_name):
    with open(os.path.join(BASE_DIR, f"{file_name}.json"), "rb") as raw_file:
        raw_file_str = raw_file.read()
        raw_file_data = chardet.detect(raw_file_str)
        if raw_file_data['confidence'] >= 0.5:
            coding = raw_file_data['encoding']
            final_data = raw_file_str.decode(coding).encode('utf-8')
            with open(os.path.join(BASE_DIR, f'{file_name}_encoded.json'), 'wb') as final_file:
                final_file.write(final_data)
        else:
            return print(f'Confidence {raw_file_data["confidence"]}'
                         f' is not enough to unambiguously define encoding of the dump file')


class Command(BaseCommand):
    def handle(self, *args, **options):
        encoding_dump('dump')
