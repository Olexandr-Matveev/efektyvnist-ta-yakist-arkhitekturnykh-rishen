from abc import ABC, abstractmethod
from typing import List

# 1. Абстракція для Відвідувача (Visitor)
class Visitor(ABC):
    """
    Інтерфейс Відвідувача оголошує методи відвідування для кожного класу елемента.
    """
    @abstractmethod
    def visit_employee(self, employee) -> None:
        pass

    @abstractmethod
    def visit_department(self, department) -> None:
        pass

    @abstractmethod
    def visit_company(self, company) -> None:
        pass


# 2. Абстракція для Елемента (Element)
class Element(ABC):
    """
    Інтерфейс Елемента оголошує метод accept, який приймає базовий інтерфейс відвідувача.
    """
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


# 3. Конкретні елементи (Співробітник, Департамент, Компанія)

class Employee(Element):
    """
    Співробітник при створенні приймає позицію та зарплату[cite: 21].
    """
    def __init__(self, position: str, salary: float):
        self.position = position
        self.salary = salary

    def accept(self, visitor: Visitor) -> None:
        # Співробітник дозволяє відвідувачу "відвідати" себе
        visitor.visit_employee(self)


class Department(Element):
    """
    Департамент при створенні приймає список співробітників[cite: 20].
    """
    def __init__(self, name: str, employees: List[Employee]):
        self.name = name
        self.employees = employees

    def accept(self, visitor: Visitor) -> None:
        # Департамент дозволяє відвідувачу "відвідати" себе
        visitor.visit_department(self)


class Company(Element):
    """
    Компанія при створенні приймає список департаментів[cite: 18].
    """
    def __init__(self, departments: List[Department]):
        self.departments = departments

    def accept(self, visitor: Visitor) -> None:
        # Компанія дозволяє відвідувачу "відвідати" себе
        visitor.visit_company(self)


# 4. Конкретний Відвідувач (Реалізація звіту)

class SalaryReportVisitor(Visitor):
    """
    Конкретний відвідувач, що реалізує логіку генерації зарплатної відомості.
    """
    def visit_employee(self, employee: Employee) -> None:
        # Логіка для співробітника: виведення інформації про зарплату
        print(f"   - Позиція: {employee.position}, Зарплата: {employee.salary}$")

    def visit_department(self, department: Department) -> None:
        # Логіка для департаменту: спочатку виводимо назву, потім проходимо по всіх співробітниках
        print(f"\n[Звіт по департаменту: {department.name}]")
        for employee in department.employees:
            employee.accept(self)

    def visit_company(self, company: Company) -> None:
        # Логіка для компанії: проходимо по всіх департаментах
        print("=== ЗАГАЛЬНА ЗАРПЛАТНА ВІДОМІСТЬ КОМПАНІЇ ===")
        for department in company.departments:
            department.accept(self)
        print("===============================================")


# 5. Клієнтський код [cite: 26]
if __name__ == "__main__":
    # Створення співробітників
    emp1 = Employee("Junior Developer", 1000)
    emp2 = Employee("Senior Developer", 4000)
    emp3 = Employee("HR Manager", 1500)
    emp4 = Employee("Recruiter", 1200)

    # Створення департаментів (приймають масив співробітників)
    it_dept = Department("IT Department", [emp1, emp2])
    hr_dept = Department("HR Department", [emp3, emp4])

    # Створення компанії (приймає масив департаментів)
    my_company = Company([it_dept, hr_dept])

    # Створення відвідувача (генератора звіту)
    report_visitor = SalaryReportVisitor()

    # --- Сценарій 1: Отримання звіту для всієї компанії ---
    print(">>> Формування звіту для всієї компанії:")
    my_company.accept(report_visitor)

    # --- Сценарій 2: Отримання звіту для конкретного департаменту ---
    print("\n>>> Формування звіту тільки для IT відділу:")
    it_dept.accept(report_visitor)
