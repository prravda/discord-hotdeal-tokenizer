from kiwipiepy import Kiwi
from typing import Optional
from pathlib import Path


class TokenizerInstance:
    __tokenizer_instance: Optional[Kiwi] = None
    __custom_dict_path = str(Path("static/user_dictionary.dict"))

    @staticmethod
    def get_instance():
        try:
            if TokenizerInstance.__tokenizer_instance is None:
                TokenizerInstance.__tokenizer_instance = Kiwi()
                TokenizerInstance.__tokenizer_instance.load_user_dictionary(
                    TokenizerInstance.__custom_dict_path
                )

            return TokenizerInstance.__tokenizer_instance
        except Exception as e:
            raise e

    @staticmethod
    def add_word_to_dictionary(word: str):
        try:
            with open(
                TokenizerInstance.__custom_dict_path, "a", encoding="utf-8"
            ) as custom_dict:
                custom_dict.write(f"{word}\tNNP\n")

            if TokenizerInstance.__tokenizer_instance is not None:
                num_of_added_words = (
                    TokenizerInstance.__tokenizer_instance.load_user_dictionary(
                        TokenizerInstance.__custom_dict_path
                    )
                )

                return num_of_added_words
        except Exception as e:
            raise e
