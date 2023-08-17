from kiwipiepy import Kiwi
import tokenizer_definition_pb2

kiwi = Kiwi()

result = tokenizer_definition_pb2.TokenizingResult()

hotdeal_title = "[지마켓] 가시제거연구소 노르웨이 순살고등어 오렌지라벨 800g+800g (20,630원) (무료)"
tokenizer_result = kiwi.tokenize(hotdeal_title)

extracted_tokens = []
for t in tokenizer_result:
    extracted_tokens.append(t.form)

result.tokens.extend(extracted_tokens)

print(result)