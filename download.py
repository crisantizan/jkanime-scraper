import os
import re
import wget
import sys
import helper


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
        lines_formatted = []

        # filter, get only valid urls
        for line in lines:
            # invalid line
            if not re.match(r'^[0-9]+ https://', line):
                continue

            [num, url] = line.strip().split(' ')
            lines_formatted.append({'episode': int(num), 'url': url})

        return lines_formatted


def remove_temp_files(output_folder):
    # get temp files
    tmp_files = [f for f in os.listdir(output_folder) if re.search('.tmp$', f)]
    if tmp_files:
        # remove .tmp files
        for tmp_file in tmp_files:
            os.remove(os.path.join(output_folder, tmp_file))


def custom_bar(current, total, width=80):
    percent = int(current / total * 100)
    current = helper.format_size(current)
    total = helper.format_size(total)
    progress = f'Downloading: {percent}% [{current} of {total}]'

    sys.stdout.write('\r' + progress + ' ')


def download_video(url_data, output_folder, anime_name):
    episode = url_data.get('episode')
    episode = f'0{episode}' if episode < 10 else episode

    url = url_data.get('url')
    extension = os.path.splitext(url)[1]

    complete_path = os.path.join(
        output_folder, f'{episode} {anime_name}{extension}')

    try:
        os.stat(complete_path)
        print(f'Episode {episode} already downloaded')
    except:
        print(f'\nFile: {episode} {anime_name}{extension}')
        wget.download(url=url, out=complete_path, bar=custom_bar)


def first_episode(txt_file_path):
    # if the current anime already locally exists
    try:
        os.stat(txt_file_path)
        # open file and read content
        with open(txt_file_path, mode='r') as f:
            lines = f.readlines()
            for line in lines:
                if re.match(r'^EPISODE [0-9]+$', line):
                    # get episode number
                    return int(line.strip().replace('EPISODE ', ''))

    except:
        print('The .txt anime file doesn\'t exists!')
        sys.exit(1)


def main():
 # params file
    txt_path = sys.argv[1]

    if not txt_path:
        print('Path of params .txt file is required!')
        sys.exit(0)

    params = get_params(txt_path=txt_path)

    anime_file_path = os.path.join('animes', f"{params.get('anime')}.txt")
    # verify anime path
    if not helper.path_exists(anime_file_path):
        print(f"Anime \"{params.get('anime')}\" doesn't exists, try again.")
        sys.exit(0)

    output_folder = params.get('output_folder')
    anime_name = params.get('name')

    # create output folder if not exists
    helper.mkdir(output_folder)
    # videos urls
    urls_data = get_urls(path=anime_file_path)
    # remove temp files
    remove_temp_files(output_folder=output_folder)

    for url_data in urls_data:
        download_video(
            url_data=url_data,
            output_folder=output_folder,
            anime_name=anime_name,
        )


if __name__ == '__main__':
    main()
