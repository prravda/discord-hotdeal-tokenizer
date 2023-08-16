from kiwipiepy import Kiwi
kiwi = Kiwi()

hotdeal_title = "[지마켓] 가시제거연구소 노르웨이 순살고등어 오렌지라벨 800g+800g (20,630원) (무료)"
result = kiwi.tokenize(hotdeal_title)

for r in result:
    print(r.form)