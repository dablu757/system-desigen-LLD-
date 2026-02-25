from abc import ABC, abstractmethod
from typing import List


# ==========================================
# 1️⃣ Composite Pattern
# ==========================================

class DocumentElement(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class TextElement(DocumentElement):
    def __init__(self, text: str):
        self.text = text

    def render(self) -> str:
        return f"Text: {self.text}"


class ImageElement(DocumentElement):
    def __init__(self, image_path: str):
        self.image_path = image_path

    def render(self) -> str:
        return f"Image: [path={self.image_path}]"


class Document:
    def __init__(self):
        self.elements: List[DocumentElement] = []

    def add_element(self, element: DocumentElement):
        self.elements.append(element)

    def render(self) -> str:
        print("Rendering Document...\n")
        rendered_output = []
        for element in self.elements:
            rendered_output.append(element.render())

        final_output = "\n".join(rendered_output)
        print(final_output)
        return final_output


# ==========================================
# 2️⃣ Strategy Pattern for Persistence
# ==========================================

class Persistence(ABC):
    @abstractmethod
    def save(self, document: Document):
        pass


class SaveToFile(Persistence):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, document: Document):
        content = document.render()
        with open(self.file_path, "w") as f:
            f.write(content)

        print(f"\nDocument saved to file: {self.file_path}")


class SaveToDB(Persistence):
    def save(self, document: Document):
        # Simulated DB Save
        content = document.render()
        print("\nSaving document to database...")
        print(f"Persisted content:\n{content}")
        print("Saved to DB successfully.")


# ==========================================
# 3️⃣ Document Editor (Orchestrator)
# ==========================================

class DocumentEditor:
    def __init__(self, persistence: Persistence):
        self.document = Document()
        self.persistence = persistence

    def add_text(self, text: str):
        self.document.add_element(TextElement(text))

    def add_image(self, image_path: str):
        self.document.add_element(ImageElement(image_path))

    def render_doc(self):
        return self.document.render()

    def save(self):
        self.persistence.save(self.document)


# ==========================================
# 4️⃣ Usage Example
# ==========================================

if __name__ == "__main__":
    # Strategy Injection
    persistence_strategy = SaveToFile("output.txt")
    # persistence_strategy = SaveToDB()

    editor = DocumentEditor(persistence_strategy)

    editor.add_text("Hello World")
    editor.add_image("/images/sample.png")
    editor.add_text("LLD is powerful!")

    editor.render_doc()
    editor.save()