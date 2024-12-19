import os

class FileUtils:
    @staticmethod
    def remove_file_if_exists(file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass