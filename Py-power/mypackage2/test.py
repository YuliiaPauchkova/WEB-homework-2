import shutil
from pathlib import Path
import re
import sys


class FileSorter:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

    MAP = {}

    for cirilic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        MAP[ord(cirilic)] = latin
        MAP[ord(cirilic.upper())] = latin.upper()
        
    def __init__(self, source_folder):
        self.source_folder = source_folder

        self.JPEG_IMAGES = []
        self.JPG_IMAGES = []
        self.PNG_IMAGES = []
        self.SVG_IMAGES = []
        self.MP3_AUDIO = []
        self.OGG_AUDIO = []
        self.WAV_AUDIO = []
        self.AMR_AUDIO = []
        self.AVI_VIDEO = []
        self.MP4_VIDEO = []
        self.MOV_VIDEO = []
        self.MKV_VIDEO = []
        self.DOC_DOCUMENTS = []
        self.DOCX_DOCUMENTS = []
        self.TXT_DOCUMENTS = []
        self.PDF_DOCUMENTS = []
        self.XLSX_DOCUMENTS = []
        self.PPTX_DOCUMENTS = []
        self.OTHERS = []
        self.ZIP_ARCHIVES = []
        self.GZ_ARCHIVES = []
        self.TAR_ARCHIVES = []
        self.FOLDERS = []
        self.EXTENSIONS = set()
        self.UNKNOWN = set()

        self.REGISTER_EXTENSION = {
            'JPEG': self.JPEG_IMAGES,
            'JPG': self.JPG_IMAGES,
            'PNG': self.PNG_IMAGES,
            'SVG': self.SVG_IMAGES,
            'MP3': self.MP3_AUDIO,
            'OGG': self.OGG_AUDIO,
            'WAV': self.WAV_AUDIO,
            'AMR': self.AMR_AUDIO,
            'AVI': self.AVI_VIDEO,
            'MP4': self.MP4_VIDEO,
            'MOV': self.MOV_VIDEO,
            'MKV': self.MKV_VIDEO,
            'DOC': self.DOC_DOCUMENTS,
            'DOCX': self.DOCX_DOCUMENTS,
            'TXT': self.TXT_DOCUMENTS,
            'PDF': self.PDF_DOCUMENTS,
            'XLSX': self.XLSX_DOCUMENTS,
            'PPTX': self.PPTX_DOCUMENTS,
            'ZIP': self.ZIP_ARCHIVES,
            'GZ': self.GZ_ARCHIVES,
            'TAR': self.TAR_ARCHIVES
        }

    def get_extension(self, name):
        return Path(name).suffix[1:].upper()

    def scan(self, folder):
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHERS'):
                    self.FOLDERS.append(item)
                    self.scan(item)
                continue

            ext = self.get_extension(item.name)  
            full_name = folder / item.name 
            if not ext:
                self.OTHERS.append(full_name)
            else:
                try:
                    ext_register = self.REGISTER_EXTENSION[ext]
                    ext_register.append(full_name)
                    self.EXTENSIONS.add(ext)
                except KeyError:
                    self.UNKNOWN.add(ext) 
                    self.OTHERS.append(full_name)

    def normalize(self, name):
        string = name.translate(self.MAP)
        translated_name = re.sub(r'[^a-zA-Z.0-9_]', '_', string)
        return translated_name

    def handle_image(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_audio(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_video(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_documents(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_archive(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.normalize(file_name.name.replace(file_name.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
        except shutil.ReadError:
            folder_for_file.rmdir()
            return
        file_name.unlink()

    def core(self):
        self.scan(self.source_folder)

        for file in self.JPEG_IMAGES:
            self.handle_image(file, self.source_folder / 'images')
        for file in self.JPG_IMAGES:
            self.handle_image(file, self.source_folder / 'images')
        for file in self.PNG_IMAGES:
            self.handle_image(file, self.source_folder / 'images')
        for file in self.SVG_IMAGES:
            self.handle_image(file, self.source_folder / 'images')

        for file in self.MP3_AUDIO:
            self.handle_audio(file, self.source_folder / 'audio')
        for file in self.OGG_AUDIO:
            self.handle_audio(file, self.source_folder / 'audio')
        for file in self.WAV_AUDIO:
            self.handle_audio(file, self.source_folder / 'audio')
        for file in self.AMR_AUDIO:
            self.handle_audio(file, self.source_folder / 'audio')

        for file in self.AVI_VIDEO:
            self.handle_video(file, self.source_folder / 'video')
        for file in self.MP4_VIDEO:
            self.handle_video(file, self.source_folder / 'video')
        for file in self.MOV_VIDEO:
            self.handle_video(file, self.source_folder / 'video')
        for file in self.MKV_VIDEO:
            self.handle_video(file, self.source_folder / 'video')

        for file in self.DOC_DOCUMENTS:
            self.handle_documents(file, self.source_folder / 'documents')
        for file in self.DOCX_DOCUMENTS:
            self.handle_documents(file, self.source_folder / 'documents')
        for file in self.TXT_DOCUMENTS:
            self.handle_documents(file, self.source_folder / 'documents')
        for file in self.PDF_DOCUMENTS:
            self.handle_documents(file, self.source_folder / 'documents')
        for file in self.XLSX_DOCUMENTS:
            self.handle_documents(file, self.source_folder / 'documents')
        for file in self.PPTX_DOCUMENTS:
            self.handle_documents(file, self.source_folder / 'documents')

        for file in self.OTHERS:
            self.handle_image(file, self.source_folder / 'others')

        for file in self.ZIP_ARCHIVES:
            self.handle_archive(file, self.source_folder / 'archives')
        for file in self.GZ_ARCHIVES:
            self.handle_archive(file, self.source_folder / 'archives')
        for file in self.TAR_ARCHIVES:
            self.handle_archive(file, self.source_folder / 'archives')

        for folder in self.FOLDERS[::-1]:
            try:
                folder.rmdir()
            except OSError:
                print(f'Error during remove folder {folder}')

def start():
    if len(sys.argv) > 1:
        folder_process = Path(sys.argv[1])
        file_sorter = FileSorter(folder_process)
        file_sorter.core()

if __name__ == "__main__":
    start()