from abc import ABC, abstractmethod


# ==============================================================================
# 1. Допоміжні класи даних
# ==============================================================================

class Product:
    """
    Клас, що представляє товар.
    Містить назву, опис, посилання на зображення та ID.
    Відповідає вимогам до ProductPage.
    """

    def __init__(self, product_id: int, title: str, description: str, image_url: str):
        self.id = product_id
        self.title = title
        self.description = description
        self.image_url = image_url


# ==============================================================================
# 2. Ієрархія Реалізації (Implementation) - Renderer
# ==============================================================================

class Renderer(ABC):
    """
    Інтерфейс реалізації (Implementation).
    Оголошує загальні операції для рендерингу частин сторінки.
    Всі конкретні рендерери повинні реалізувати ці методи.
    """

    @abstractmethod
    def render_title(self, title: str) -> str:
        pass

    @abstractmethod
    def render_text_block(self, text: str) -> str:
        pass

    @abstractmethod
    def render_image(self, url: str) -> str:
        pass

    @abstractmethod
    def render_label(self, label: str, value: str) -> str:
        pass


class HTMLRenderer(Renderer):
    """
    Конкретна реалізація рендерера для HTML формату.
    """

    def render_title(self, title: str) -> str:
        return f"<h1>{title}</h1>"

    def render_text_block(self, text: str) -> str:
        return f"<p>{text}</p>"

    def render_image(self, url: str) -> str:
        return f"<img src='{url}' alt='image' />"

    def render_label(self, label: str, value: str) -> str:
        return f"<span><b>{label}:</b> {value}</span>"


class JsonRenderer(Renderer):
    """
    Конкретна реалізація рендерера для JSON формату.
    Повертає форматовані рядки, схожі на структуру JSON.
    """

    def render_title(self, title: str) -> str:
        return f'"title": "{title}"'

    def render_text_block(self, text: str) -> str:
        return f'"content": "{text}"'

    def render_image(self, url: str) -> str:
        return f'"img": "{url}"'

    def render_label(self, label: str, value: str) -> str:
        return f'"{label}": "{value}"'


class XmlRenderer(Renderer):
    """
    Конкретна реалізація рендерера для XML формату.
    """

    def render_title(self, title: str) -> str:
        return f"<title>{title}</title>"

    def render_text_block(self, text: str) -> str:
        return f"<text>{text}</text>"

    def render_image(self, url: str) -> str:
        return f"<image src='{url}' />"

    def render_label(self, label: str, value: str) -> str:
        return f"<{label}>{value}</{label}>"


# ==============================================================================
# 3. Ієрархія Абстракції (Abstraction) - Page
# ==============================================================================

class Page(ABC):
    """
    Абстракція.
    Містить посилання на об'єкт типу Renderer і делегує йому роботу.
    """

    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    def change_renderer(self, renderer: Renderer):
        """Дозволяє динамічно змінювати формат відображення."""
        self.renderer = renderer

    @abstractmethod
    def view(self) -> str:
        """Метод відображення сторінки, який використовує рендерер."""
        pass


class SimplePage(Page):
    """
    Проста сторінка.
    Складається із заголовку та контенту.
    """

    def __init__(self, renderer: Renderer, title: str, content: str):
        super().__init__(renderer)
        self.title = title
        self.content = content

    def view(self) -> str:
        # Збираємо сторінку з частин, використовуючи поточний рендерер
        result = []
        result.append(self.renderer.render_title(self.title))
        result.append(self.renderer.render_text_block(self.content))

        # Для красивого виводу об'єднуємо через перенос рядка
        return "\n".join(result)


class ProductPage(Page):
    """
    Сторінка товару.
    Містить назву, опис, зображення та ID товару (об'єкт Product).
    """

    def __init__(self, renderer: Renderer, product: Product):
        super().__init__(renderer)
        self.product = product

    def view(self) -> str:
        # Делегування відображення деталей товару рендереру
        result = []
        result.append(self.renderer.render_title(self.product.title))
        result.append(self.renderer.render_text_block(self.product.description))
        result.append(self.renderer.render_image(self.product.image_url))
        result.append(self.renderer.render_label("id", str(self.product.id)))

        return "\n".join(result)


# ==============================================================================
# 4. Клієнтський код
# ==============================================================================

if __name__ == "__main__":
    # 1. Створення контенту (об'єкт Product)
    my_product = Product(
        product_id=101,
        title="Ноутбук Gaming X",
        description="Потужний ігровий ноутбук.",
        image_url="/img/laptop.png"
    )

    # 2. Демонстрація SimplePage з HTML рендером
    print("--- SimplePage (HTML) ---")
    html_renderer = HTMLRenderer()
    simple_page = SimplePage(html_renderer, "Головна", "Ласкаво просимо на наш сайт!")
    print(simple_page.view())
    print("\n")

    # 3. Демонстрація зміни рендера на JSON для тієї ж сторінки
    print("--- SimplePage (JSON) ---")
    simple_page.change_renderer(JsonRenderer())
    print("{\n" + simple_page.view() + "\n}")
    print("\n")

    # 4. Демонстрація ProductPage з XML рендером
    print("--- ProductPage (XML) ---")
    xml_renderer = XmlRenderer()
    product_page = ProductPage(xml_renderer, my_product)
    print("<product>")
    print(product_page.view())
    print("</product>")
    print("\n")

    # 5. Демонстрація ProductPage з HTML рендером
    print("--- ProductPage (HTML) ---")
    product_page.change_renderer(html_renderer)
    print(product_page.view())
