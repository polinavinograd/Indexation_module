class Document:
    def __init__(self, name, text, creation_datetime):
        self.name = name
        self.text = text
        self.creation_datetime = creation_datetime

    def get_lemm_inverse_frequency(self, lemm: str) -> float:
        pass

    def get_lemm_weight(self, lemm: str) -> float:
        pass

    def get_lemm_weights(self, lemm_list: list[str]) -> list[float]:
        pass

    def get_normalized_text() -> list[str]:
        pass