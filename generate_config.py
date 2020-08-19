import helper
from sys import exit
from pathlib import Path
import os


def get_input_data(placeholder, is_path=False):
    while True:
        data = input(placeholder)
        if not data:
            print('Please, fill this param')
        else:
            if is_path and not helper.path_exists(path=data):
                print('Path doesn\'t exists')
                continue
            return data


def generate_filename(name):
    return f"{name.lower().replace(' ', '-')}.config.txt"


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
    anime_txt = get_input_data('Anime file name (.txt file): ')
    output_folder = get_input_data('Output folder: ', is_path=True)
    anime_name = get_input_data('Anime name: ')
    write_file(anime_txt, output_folder, anime_name)


if __name__ == '__main__':
    main()
