import java.util.HashMap;
import java.util.Map;

// Клас, що реалізує патерн проектування Одинак (Singleton).
// Забезпечує існування єдиного екземпляра менеджера сховищ у системі.
public class StorageManager {

    // Статичне поле для зберігання єдиного екземпляра класу.
    private static StorageManager instance;

    // Зберігання налаштувань сховища для кожного користувача (User ID -> Storage Type).
    private Map<String, String> userStoragePreferences;

    // Приватний конструктор запобігає створенню екземплярів класу ззовні.
    private StorageManager() {
        userStoragePreferences = new HashMap<>();
        System.out.println("Система управління файлами ініціалізована.");
    }

    // Публічний статичний метод для отримання доступу до єдиного екземпляра.
    // Реалізує "ліниву" ініціалізацію (lazy initialization).
    public static synchronized StorageManager getInstance() {
        if (instance == null) {
            instance = new StorageManager();
        }
        return instance;
    }

    /**
     * Встановлює тип сховища для конкретного користувача.
     * @param userId Унікальний ідентифікатор користувача.
     * @param storageType Тип сховища (наприклад, "LocalDisk", "AmazonS3").
     */
    public void connectUserToStorage(String userId, String storageType) {
        userStoragePreferences.put(userId, storageType);
        System.out.println("Користувач " + userId + " підключений до сховища: " + storageType);
    }

    /**
     * Метод завантаження файлу у сховище.
     * @param userId Ідентифікатор користувача.
     * @param fileName Назва файлу.
     * @param fileData Масив байтів, що містить дані файлу.
     * @return Результат операції (успіх/невдача).
     */
    public boolean uploadFile(String userId, String fileName, byte[] fileData) {
        String storage = userStoragePreferences.get(userId);
        if (storage == null) {
            System.out.println("Помилка: сховище для користувача " + userId + " не обрано.");
            return false;
        }
        // Логіка завантаження файлу у відповідне сховище
        return true; 
    }

    /**
     * Метод отримання файлу зі сховища.
     * @param userId Ідентифікатор користувача.
     * @param fileName Назва файлу.
     * @return Дані файлу у вигляді масиву байтів.
     */
    public byte[] downloadFile(String userId, String fileName) {
        // Логіка пошуку та завантаження файлу
        return new byte[0];
    }
}

// Клас для демонстрації роботи системи
class Main {
    public static void main(String[] args) {
        // Отримання єдиного екземпляра менеджера
        StorageManager manager = StorageManager.getInstance();

        // Налаштування сховищ для різних користувачів згідно з варіантом
        manager.connectUserToStorage("user1", "LocalDisk");
        manager.connectUserToStorage("user2", "AmazonS3");
    }
}
