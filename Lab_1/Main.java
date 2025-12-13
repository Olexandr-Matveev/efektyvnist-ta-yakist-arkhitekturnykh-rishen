import java.util.HashMap;
import java.util.Map;

// Інтерфейс для сховищ (дозволяє масштабувати систему в майбутньому )
interface Storage {
    void uploadFile(String fileName, byte[] data);
    byte[] downloadFile(String fileName);
}

// Конкретне сховище: Локальний диск [cite: 31]
class LocalDiskStorage implements Storage {
    @Override
    public void uploadFile(String fileName, byte[] data) {
        // Логіка завантаження на диск
    }

    @Override
    public byte[] downloadFile(String fileName) {
        // Логіка скачування з диска
        return new byte[0];
    }
}

// Конкретне сховище: Amazon S3 [cite: 32]
class AmazonS3Storage implements Storage {
    @Override
    public void uploadFile(String fileName, byte[] data) {
        // Логіка завантаження на S3
    }

    @Override
    public byte[] downloadFile(String fileName) {
        // Логіка скачування з S3
        return new byte[0];
    }
}

// КЛАС-ОДИНАК (Singleton) - Система управління файлами [cite: 25, 41]
class FileSystemManager {

    // 1. Статична змінна, що зберігає єдиний екземпляр класу
    private static FileSystemManager instance;

    // Зберігання налаштувань сховища для кожного користувача
    // Key: UserID, Value: Selected Storage
    private Map<String, Storage> userStoragePreferences;

    // 2. Приватний конструктор, щоб заборонити створення об'єктів ззовні
    private FileSystemManager() {
        userStoragePreferences = new HashMap<>();
        System.out.println("Систему управління файлами запущено.");
    }

    // 3. Публічний статичний метод для отримання єдиного екземпляра
    public static synchronized FileSystemManager getInstance() {
        if (instance == null) {
            instance = new FileSystemManager();
        }
        return instance;
    }

    // Метод підключення користувача до певного сховища [cite: 29]
    // Приймає ID користувача та тип сховища ("local" або "s3")
    public void connectUserToStorage(String userId, String storageType) {
        Storage storage;

        switch (storageType.toLowerCase()) {
            case "s3":
                storage = new AmazonS3Storage();
                break;
            case "local":
            default:
                storage = new LocalDiskStorage();
                break;
        }

        // Зберігаємо вибір користувача
        userStoragePreferences.put(userId, storage);
    }

    // Метод для отримання поточного сховища користувача
    public Storage getUserStorage(String userId) {
        return userStoragePreferences.get(userId);
    }
}

// Приклад використання (Main)
public class Main {
    public static void main(String[] args) {
        // Отримуємо єдиний екземпляр менеджера
        FileSystemManager manager = FileSystemManager.getInstance();

        // Налаштовуємо сховища для різних користувачів [cite: 37]
        manager.connectUserToStorage("user1", "local");
        manager.connectUserToStorage("user2", "s3");

        // Перевірка
        System.out.println("User1 storage: " + manager.getUserStorage("user1").getClass().getSimpleName());
        System.out.println("User2 storage: " + manager.getUserStorage("user2").getClass().getSimpleName());
    }
}
