/**
 * Лабораторна робота №2
 * Тема: Патерн проектування "Фабричний метод" (Factory Method)
 * * Файл: main.cpp
 * Середовище: Visual Studio Code
 * Мова: C++
 */

#include <iostream>
#include <string>
#include <memory>

using namespace std;

// =========================================================
// 1. Інтерфейс Продукту (Product Interface)
// Описує загальний інтерфейс для всіх соціальних мереж.
// =========================================================
class SocialNetworkConnector {
public:
    virtual ~SocialNetworkConnector() {}
    
    // Метод публікації повідомлення
    virtual void publish(const string& content) const = 0;
    
    // Метод входу в систему (імітація)
    virtual void logIn() const = 0;
};

// =========================================================
// 2. Конкретні Продукти (Concrete Products)
// Реалізація підключення до конкретних мереж.
// =========================================================

// Клас для роботи з Facebook
// Використовує login та password 
class FacebookConnector : public SocialNetworkConnector {
private:
    string _login;
    string _password;

public:
    FacebookConnector(string login, string password) : _login(login), _password(password) {}

    void logIn() const override {
        // Тут мала б бути логіка авторизації Facebook API
        cout << "Login to Facebook using Login: " << _login << endl;
    }

    void publish(const string& content) const override {
        // Імітація публікації у Facebook
        cout << "[Facebook] Публікація нового посту: " << content << endl;
    }
};

// Клас для роботи з LinkedIn
// Використовує email та password 
class LinkedInConnector : public SocialNetworkConnector {
private:
    string _email;
    string _password;

public:
    LinkedInConnector(string email, string password) : _email(email), _password(password) {}

    void logIn() const override {
        // Тут мала б бути логіка авторизації LinkedIn API
        cout << "Login to LinkedIn using Email: " << _email << endl;
    }

    void publish(const string& content) const override {
        // Імітація публікації у LinkedIn
        cout << "[LinkedIn] Публікація нового посту: " << content << endl;
    }
};

// =========================================================
// 3. Абстрактний Творець (Creator)
// Оголошує фабричний метод, який має повертати об'єкт Product.
// =========================================================
class SocialNetworkPoster {
public:
    virtual ~SocialNetworkPoster() {}

    // ФАБРИЧНИЙ МЕТОД (Factory Method)
    // Має бути реалізований у підкласах для створення конкретних конекторів
    virtual unique_ptr<SocialNetworkConnector> getSocialNetwork() const = 0;

    // Основна бізнес-логіка: використовує конектор, створений фабричним методом,
    // не знаючи конкретного класу мережі.
    void postMessage(const string& content) const {
        // Створюємо конектор через фабричний метод
        unique_ptr<SocialNetworkConnector> network = this->getSocialNetwork();
        
        // Виконуємо дії (логін та публікація)
        network->logIn();
        network->publish(content);
    }
};

// =========================================================
// 4. Конкретні Творці (Concrete Creators)
// Перевизначають фабричний метод для повернення конкретного продукту.
// =========================================================

// Творець для Facebook
class FacebookPoster : public SocialNetworkPoster {
private:
    string _login, _password;

public:
    FacebookPoster(string login, string password) : _login(login), _password(password) {}

    // Реалізація фабричного методу
    unique_ptr<SocialNetworkConnector> getSocialNetwork() const override {
        return make_unique<FacebookConnector>(_login, _password);
    }
};

// Творець для LinkedIn
class LinkedInPoster : public SocialNetworkPoster {
private:
    string _email, _password;

public:
    LinkedInPoster(string email, string password) : _email(email), _password(password) {}

    // Реалізація фабричного методу
    unique_ptr<SocialNetworkConnector> getSocialNetwork() const override {
        return make_unique<LinkedInConnector>(_email, _password);
    }
};

// =========================================================
// 5. Клієнтський код (Client Code)
// Демонстрація роботи 
// =========================================================

// Функція, яка працює з абстрактним творцем
void clientCode(const SocialNetworkPoster& creator) {
    creator.postMessage("Це тестове повідомлення для лабораторної роботи №2.");
}

int main() {
    // Налаштування для коректного відображення кирилиці в консолі Windows
    setlocale(LC_ALL, "uk_UA.UTF-8"); 

    cout << "=== Запуск системи публікації повідомлень ===" << endl << endl;

    // 1. Публікація у Facebook
    cout << "Сценарій 1: Публікація у Facebook." << endl;
    // Створюємо творця, передаючи логін та пароль 
    unique_ptr<SocialNetworkPoster> fbPoster = make_unique<FacebookPoster>("my_fb_login", "fb_secure_pass");
    clientCode(*fbPoster);

    cout << endl << "---------------------------------------------" << endl << endl;

    // 2. Публікація у LinkedIn
    cout << "Сценарій 2: Публікація у LinkedIn." << endl;
    // Створюємо творця, передаючи email та пароль 
    unique_ptr<SocialNetworkPoster> liPoster = make_unique<LinkedInPoster>("user@work.email", "li_secure_pass");
    clientCode(*liPoster);

    return 0;
}