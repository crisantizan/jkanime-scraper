import os
import re
import wget
import sys


def validate_file(path):
    try:
        os.stat(path)
        return True
    except:
        return False


def mkdir(path):
    try:
        os.stat(path)
    except:
        os.mkdir(path)


def get_params(txt_path):
    with open(file=txt_path, mode='r') as f:
        lines = f.readlines()

        if not len(lines) == 3:
            print('File bad format, should be three lines')
            sys.exit(0)

        output = os.path.join(lines[1].strip(), lines[2].strip())

        return {
            'anime': lines[0].strip(),
            'output_folder': output,
            'name': lines[2].strip()
        }


def get_urls(path):
    with open(file=path, mode='r') as f:
        lines = f.readlines()
        # filter, get only valid urls
        return [line.strip() for line in lines if re.match(r'^https://', line)]


def remove_temp_files(output_folder):
    # get temp files
    tmp_files = [f for f in os.listdir(output_folder) if re.search('.tmp$', f)]
    if tmp_files:
        # remove .tmp files
        for tmp_file in tmp_files:
            os.remove(os.path.join(output_folder, tmp_file))


def download_video(url, output_folder, anime_name, episode):
    episode = f'0{episode}' if episode < 10 else episode
    extension = os.path.splitext(url)[1]
    complete_path = os.path.join(
        output_folder, f'{episode} {anime_name}{extension}')

    try:
        os.stat(complete_path)
        print(f'\nEpisode {episode} already downloaded')
    except:
        print(f'\nDownloading episode: {episode}')
        wget.download(url, complete_path)


def main():
 # params file
    txt_path = sys.argv[1]

    if not txt_path:
        print('Path of params .txt file is required!')
        sys.exit(0)

    params = get_params(txt_path=txt_path)

    anime_file_path = os.path.join('animes', f"{params.get('anime')}.txt")
    # verify anime path
    if not validate_file(anime_file_path):
        print(f"Anime \"{params.get('anime')}\" doesn't exists, try again.")
        sys.exit(0)

    output_folder = params.get('output_folder')
    anime_name = params.get('name')

    # create output folder if not exists
    mkdir(output_folder)
    # videos urls
    urls = get_urls(path=anime_file_path)
    # remove temp files
    remove_temp_files(output_folder=output_folder)

    for index, url in enumerate(urls, start=1):
        download_video(url=url, output_folder=output_folder,
                       anime_name=anime_name, episode=index)


if __name__ == '__main__':
    main()
