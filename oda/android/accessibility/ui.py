from dataclasses import dataclass, field


@dataclass
class UIElement:
    text: str | None = None
    content_description: str | None = None
    resource_id: str | None = None
    class_name: str | None = None

    clickable: bool = False
    enabled: bool = True

    x: int | None = None
    y: int | None = None

    children: list["UIElement"] = field(default_factory=list)


class UISnapshot:
    def __init__(self, elements: list[UIElement] | None = None):
        self.elements = elements or []

    def add(self, element: UIElement) -> None:
        self.elements.append(element)

    def find_by_text(self, text: str) -> UIElement | None:
        target = text.strip().lower()

        for element in self.elements:
            if element.text and element.text.strip().lower() == target:
                return element

        return None

    def find_by_description(self, description: str) -> UIElement | None:
        target = description.strip().lower()

        for element in self.elements:
            if (
                element.content_description
                and element.content_description.strip().lower() == target
            ):
                return element

        return None

    def clickable_elements(self) -> list[UIElement]:
        return [
            element
            for element in self.elements
            if element.clickable and element.enabled
        ]
