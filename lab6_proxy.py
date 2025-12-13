from abc import ABC, abstractmethod
import time


# 1. Інтерфейс Downloader (Загальний інтерфейс)
class Downloader(ABC):
    """
    Спільний інтерфейс для Реального Суб'єкта (SimpleDownloader)
    та Замісника (ProxyDownloader).
    """

    @abstractmethod
    def download(self, filename: str) -> str:
        pass


# 2. Клас SimpleDownloader (Реальний Суб'єкт)
class SimpleDownloader(Downloader):
    """
    Клас, що виконує реальну роботу із завантаження файлів.
    Ми не змінюємо цей клас для додавання кешування.
    """

    def download(self, filename: str) -> str:
        print(f"[SimpleDownloader] Завантаження файлу '{filename}' з мережі...")

        # Імітація повільного завантаження (затримка 1 секунда)
        time.sleep(1.0)

        # Повертаємо імітовані дані файлу
        return f"Вміст файлу {filename}"


# 3. Клас ProxyDownloader (Замісник)
class ProxyDownloader(Downloader):
    """
    Замісник, який додає логіку кешування.
    Він перехоплює виклики до реального об'єкта.
    """

    def __init__(self, real_downloader: SimpleDownloader):
        self._real_downloader = real_downloader
        self._cache = {}

    def download(self, filename: str) -> str:
        # Перевірка, чи є файл вже у кеші
        if filename in self._cache:
            print(f"[Proxy] Файл '{filename}' знайдено в кеші. Повертаємо збережену копію.")
            return self._cache[filename]
        else:
            # Якщо файлу немає в кеші, звертаємось до реального завантажувача
            print(f"[Proxy] Файл '{filename}' відсутній у кеші. Виклик реального завантажувача.")
            data = self._real_downloader.download(filename)

            # Зберігаємо результат у кеш
            self._cache[filename] = data
            return data


# 4. Клієнтський код
def client_code(downloader: Downloader, filename: str):
    """
    Клієнтський код працює з будь-яким об'єктом, що наслідує інтерфейс Downloader.
    Йому не важливо, працює він з Proxy чи з реальним об'єктом.
    """
    start_time = time.time()
    result = downloader.download(filename)
    end_time = time.time()

    print(f"Результат: {result}")
    print(f"Час виконання: {end_time - start_time:.2f} сек.\n")


if __name__ == "__main__":
    # Створення реального об'єкта
    real_subject = SimpleDownloader()

    # Створення замісника, який огортає реальний об'єкт
    proxy = ProxyDownloader(real_subject)

    print("--- Тест 1: Перше завантаження файлу (холодний старт) ---")
    # Файл ще не в кеші, тому завантаження буде повільним
    client_code(proxy, "image_hq.jpg")

    print("--- Тест 2: Повторне завантаження того ж файлу (кеш) ---")
    # Файл вже в кеші, завантаження має бути миттєвим
    client_code(proxy, "image_hq.jpg")

    print("--- Тест 3: Завантаження іншого файлу ---")
    client_code(proxy, "video_clip.mp4")
