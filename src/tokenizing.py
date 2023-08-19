import grpc

from concurrent import futures
from proto_built_result import tokenizer_definition_pb2_grpc as tokenizer_grpc
from proto_built_result import tokenizer_definition_pb2 as tokenizer

from kiwipiepy import Kiwi

kiwi_instance = Kiwi()


def tokenize(sentence: tokenizer.TokenizingRequest) -> tokenizer.TokenizingResult:
    parsed_tokens = kiwi_instance.tokenize(sentence.title)

    protobuf_result = tokenizer.TokenizingResult()

    for p in parsed_tokens:
        protobuf_result.tokens.append(p.form)

    protobuf_result.words.extend(sentence.title.split())

    return protobuf_result


class TokenizerServicer(tokenizer_grpc.TokenizerServicer):
    def Tokenize(self, request: tokenizer.TokenizingRequest, unused_context) -> tokenizer.TokenizingResult:
        return tokenize(request)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tokenizer_grpc.add_TokenizerServicer_to_server(TokenizerServicer(), server)

    port_number = 50051
    server.add_insecure_port(f'[::]:{port_number}')

    server.start()

    print(f'gRPC server listen on {port_number}!')

    server.wait_for_termination()

serve()