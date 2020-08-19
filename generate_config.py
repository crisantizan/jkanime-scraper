import helper
from sys import exit
from pathlib import Path
import os


def get_input_data(placeholder, cb=None):
    while True:
        data = input(placeholder)
        if not data:
            print('Please, fill this param')
        else:
            if type(cb).__name__ == 'function' and not cb(data):
                continue

            return data


def generate_filename(name):
    return f"{name.lower().replace(' ', '-')}.config.txt"


def validate_output_folder(path):
    if not helper.path_exists(path):
        print('Path doesn\'t exists')
        return False
    else:
        return True


def validate_anime_txt(name):
    path = os.path.join('animes', f'{name}.txt')
    if not helper.path_exists(path):
        print(f'Anime "{name}" has not been scraped')
        return False
    else:
        return True


def write_file(anime_txt, output_folder, anime_name):
    home = str(Path.home())
    filename = os.path.join(home, generate_filename(anime_name))
    with open(file=filename, mode='w') as f:
        f.write(f'{anime_txt}\n')
        f.write(f'{output_folder}\n')
        f.write(f'{anime_name}')

    print('\nParams file created successfully!')
    print(f'Find it in: {filename}\n')


def main():
    anime_txt = get_input_data('.txt filename: ', validate_anime_txt)
    output_folder = get_input_data('Output folder: ', validate_output_folder)
    anime_name = get_input_data('Anime name: ')
    write_file(anime_txt, output_folder, anime_name)


if __name__ == '__main__':
    main()
