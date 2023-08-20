import asyncio
from concurrent import futures
from typing import List

from grpc import aio
from kiwipiepy import Kiwi
from pydantic import BaseModel

from src.proto_built_result.tokenizer_definition_pb2 import (TokenizingRequest,
                                                             TokenizingResult)
from src.proto_built_result.tokenizer_definition_pb2_grpc import (
    TokenizerServicer, add_TokenizerServicer_to_server)

kiwi_instance = Kiwi()


class TokensAndWords(BaseModel):
    words: List[str]
    tokens: List[str]


def tokenize(title: str) -> TokensAndWords:
    parsed_tokens = kiwi_instance.tokenize(title)

    tokens: List[str] = [t.form for t in parsed_tokens]
    words: List[str] = title.split()

    return TokensAndWords(tokens=tokens, words=words)


class TokenizerService(TokenizerServicer):
    def Tokenize(self, request: TokenizingRequest, unused_context) -> TokenizingResult:
        tokenized_result = tokenize(request.title)

        protobuf_result = TokenizingResult()

        protobuf_result.words.extend(tokenized_result.words)
        protobuf_result.tokens.extend(tokenized_result.tokens)

        return protobuf_result


async def serve() -> None:
    server = aio.server(futures.ThreadPoolExecutor())
    add_TokenizerServicer_to_server(TokenizerService(), server)

    port_number = 50051
    server.add_insecure_port(f"[::]:{port_number}")

    await server.start()

    print(f"gRPC server listen on {port_number}!")

    await server.wait_for_termination()


asyncio.get_event_loop().run_until_complete(serve())
