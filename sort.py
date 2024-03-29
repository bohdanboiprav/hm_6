from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
import os


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    # if len(os.listdir(folder_for_file)) == 0:
    try:
        try:
            shutil.unpack_archive(filename, folder_for_file)
        except shutil.ReadError:
            folder_for_file.rmdir()
    except OSError:
        print(f"{OSError}: ваші архіви видалено!")
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")


def main(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video')

    for file in parser.MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


# if __name__ == "__main__":
#     folder_for_scan = Path('folder_for_test/')
#     print(f'Start in folder: {folder_for_scan.resolve()}')
#     main(folder_for_scan.resolve())


if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder: {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
