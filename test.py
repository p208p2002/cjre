import cjre
from cjre import CJRE_jieba, CJRE_ckip

if __name__ == "__main__":
    print(cjre)
    
    # use jieba
    cjre = CJRE_jieba()

    # use ckip
    # CJRE_ckip.download_model() # download the model on first time
    # cjre = CJRE_ckip(disable_cuda=False)

    with open('test.txt','r',encoding='utf-8') as f:
        text = f.read().replace('\r\n','\n')
    
    # flags: https://github.com/fxsjy/jieba
    triple_res = cjre.extract_triple_res(text, stopwords=[])
    for triple_re in triple_res:
        print('-'.join(triple_re))

    