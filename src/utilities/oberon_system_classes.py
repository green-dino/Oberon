from pydantic import Basemodel  


class Document:
    def __init__(self, element_identifier: str, element_type: str, title: str, text: str, doc_identifier: str):
        self._element_identifier = None
        self._element_type = None
        self._title = None
        self._text = None
        self._doc_identifier = None

        self.element_identifier = element_identifier
        self.element_type = element_type
        self.title = title
        self.text = text
        self.doc_identifier = doc_identifier

    @property
    def element_identifier(self) -> str:
        return self._element_identifier

    @element_identifier.setter
    def element_identifier(self, value: str):
        if not isinstance(value, str):
            raise TypeError("element_identifier must be a string")
        self._element_identifier = value

    @property
    def element_type(self) -> str:
        return self._element_type

    @element_type.setter
    def element_type(self, value: str):
        if not isinstance(value, str):
            raise TypeError("element_type must be a string")
        self._element_type = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str):
            raise TypeError("title must be a string")
        self._title = value

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        self._text = value

    @property
    def doc_identifier(self) -> str:
        return self._doc_identifier

    @doc_identifier.setter
    def doc_identifier(self, value: str):
        if not isinstance(value, str):
            raise TypeError("doc_identifier must be a string")
        self._doc_identifier = value

    def __repr__(self):
        return (f"Document(element_identifier='{self.element_identifier}', element_type='{self.element_type}', "
                f"title='{self.title}', text='{self.text}', doc_identifier='{self.doc_identifier}')")
