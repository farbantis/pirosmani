# from pathlib import Path
# from random import randint
# from django.core.exceptions import ValidationError
#
#
# def validate_file_size(value):
#     file_size = value.file.size
#     LIMIT_KB = 150
#     if file_size > LIMIT_KB * 1024:
#         raise ValidationError(f'Max size of file is {file_size*1024}Kb, while max {LIMIT_KB*1024}KB allowed')
#
#
# def upload_path_and_rename(instance, filename):
#     extension = filename.split('.')[-1]
#     folder = 'user'
#     sub_folder = 'user/%Y/%m'
#     if instance.pk:
#         filename = f'{str(instance.user.pk)}.{extension}'
#     else:
#         filename = f"{''.join([str(y) for x in range(0, 5) for y in [randint(0, 9)]])}.{extension}"
#     return Path(folder, sub_folder, filename)