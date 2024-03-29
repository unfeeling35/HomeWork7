import os
import shutil
import zipfile


def normalize(file_name):
    translit_table = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '',
        'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ю': 'iu', 'я': 'ia'
    }

    result = ''
    base_name, extension = os.path.splitext(file_name)
    
    for char in base_name:
        if char.isspace():
            result += '_'
        else:
            result += translit_table.get(char, char)
    
    return result + extension


def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for directory in dirs:
            current_folder = os.path.join(root, directory)
            try:
                os.rmdir(current_folder)
                print(f"Empty folder removed: {current_folder}")
            except OSError as e:
                print(f"Error: {e}")


def organize_files(folder_path):
    folders_to_ignore = ['archives', 'video', 'audio', 'documents', 'images', 'other']

    for folder in folders_to_ignore:
        if not os.path.exists(os.path.join(folder_path, folder)):
            os.makedirs(os.path.join(folder_path, folder))  # створення папок, якщо їх немає

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if any(folder in file_path.split(os.path.sep) for folder in folders_to_ignore): # Ігнорувати файли, які знаходяться в папках для ігнорування
                continue

            if file_name.startswith('.') or os.path.isdir(file_path) or file_name in folders_to_ignore:
                continue

            normalized_name = normalize(file_name)

            file_extension = os.path.splitext(file_name)[1][1:].lower()

            if file_extension in ['jpeg', 'png', 'jpg', 'svg']:
                shutil.move(file_path, os.path.join(folder_path, 'images', normalized_name))
            elif file_extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
                shutil.move(file_path, os.path.join(folder_path, 'documents', normalized_name))
            elif file_extension in ['mp3', 'ogg', 'wav', 'amr']:
                shutil.move(file_path, os.path.join(folder_path, 'audio', normalized_name))
            elif file_extension in ['avi', 'mp4', 'mov', 'mkv']:
                shutil.move(file_path, os.path.join(folder_path, 'video', normalized_name))
            elif file_extension in ['zip', 'gz', 'tar']:
                try:
                    if os.path.exists(file_path):
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(os.path.join(folder_path, 'archives', normalized_name))
                        os.remove(file_path)  # видалення архіву після розпакування
                        continue  # пропускаємо подальше сортування для розархівованих файлів
                    else:
                        print(f"File not found: {file_path}")
                except zipfile.BadZipFile:
                    os.remove(file_path)
            else:
                shutil.move(file_path, os.path.join(folder_path, 'other', normalized_name))

    remove_empty_folders(folder_path)


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        sys.exit(1)

    organize_files(folder_path)
    print("Folder sorting completed successfully.")

if __name__ == "__main__":
    main()

