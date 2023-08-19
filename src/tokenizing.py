import grpc
import asyncio

from concurrent import futures
from proto_built_result import tokenizer_definition_pb2_grpc as tokenizer_grpc
from proto_built_result import tokenizer_definition_pb2 as tokenizer

from kiwipiepy import Kiwi

kiwi_instance = Kiwi()


async def tokenize(sentence: tokenizer.TokenizingRequest) -> tokenizer.TokenizingResult:
    loop = asyncio.get_event_loop()

    with futures.ThreadPoolExecutor() as pool:
        parsed_tokens = await loop.run_in_executor(pool, kiwi_instance.tokenize, sentence.title)

    protobuf_result = tokenizer.TokenizingResult()

    for p in parsed_tokens:
        protobuf_result.tokens.append(p.form)

    protobuf_result.words.extend(sentence.title.split())

    return protobuf_result


class TokenizerServicer(tokenizer_grpc.TokenizerServicer):
    async def Tokenize(self, request: tokenizer.TokenizingRequest, unused_context) -> tokenizer.TokenizingResult:
        return await tokenize(request)


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor())
    tokenizer_grpc.add_TokenizerServicer_to_server(
        TokenizerServicer(), server
    )

    port_number = 50051
    server.add_insecure_port(f'[::]:{port_number}')

    await server.start()

    print(f'gRPC server listen on {port_number}!')

    await server.wait_for_termination()

asyncio.get_event_loop().run_until_complete(serve())