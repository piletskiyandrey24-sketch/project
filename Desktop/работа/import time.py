import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

Folder_to_watch = r"C:\Users\Admin\OneDrive\Документы\nigger"
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # Спрацоўвае пры стварэнні файла
        if not event.is_directory:
            print(f"Знойдзены новы файл: {event.src_path}")
            time.sleep(0.5) 
            try:
                with open(event.src_path, 'r', encoding='utf-8', errors='ignore') as file:
                    print(f"Змесціва: {file.read(10)}...")
                    print(event)
            except Exception as e:
                print(f"Не ўдалося прачытаць файл: {e}")


if __name__ == "__main__":
    # Праверка, ці існуе папка, перад запускам
    if not os.path.exists(Folder_to_watch):
        print(f"Памылка: Папка па шляху '{Folder_to_watch}' не знойдзена!")
    else:
        event_handler = Handler()
        observer = Observer()
        # recursive=False азначае, што мы сочым толькі за гэтай папкай, без падпапак
        observer.schedule(event_handler, Folder_to_watch, recursive=False)
        
        observer.start()
        print(f"Маніторынг запушчаны ў: {Folder_to_watch}")
        print("Націсніце Ctrl+C, каб спыніць...")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\nМаніторынг спынены.")
        
        observer.join()

