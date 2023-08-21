from pydantic import BaseModel
from typing import List
from src.tokenizer.TokenizerInstance import TokenizerInstance


class TokenizingResult(BaseModel):
    words: List[str]
    tokens: List[str]


class TokenizerService:
    def tokenize(self, title: str) -> TokenizingResult:
        try:
            tokenizer_instance = TokenizerInstance.get_instance()
            tokens_from_tokenizer = tokenizer_instance.tokenize(title)

            return TokenizingResult(
                words=title.split(), tokens=[t.form for t in tokens_from_tokenizer]
            )

        except Exception as e:
            raise e

    def add_word_to_dict(self, word: str):
        try:
            TokenizerInstance.add_word_to_dictionary(word)

        except Exception as e:
            raise e
