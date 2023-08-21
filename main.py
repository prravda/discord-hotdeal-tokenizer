from src.tokenizer.TokenizerService import TokenizerService
from fastapi import FastAPI
from pydantic import BaseModel


class WordToAdd(BaseModel):
    word: str


class TitleToTokenize(BaseModel):
    title: str


app = FastAPI()

service = TokenizerService()


@app.post("/tokenize")
async def tokenize(title_to_tokenize: TitleToTokenize):
    return service.tokenize(title_to_tokenize.title)


@app.post("/words")
async def add_word_to_dict(word_to_add: WordToAdd):
    return service.add_word_to_dict(word_to_add.word)
