from cjre import CJRE_jieba
from VerdictCut.find_fact import extract_fact
if __name__ == "__main__":
    cjre = CJRE_jieba()
    cjre.set_keep_flags(['v','vd','vn'])
    cjre.set_stopwords(['上列','│'])
    with open('test.txt','r',encoding='utf-8') as f:
        text = f.read()
    fact_text = extract_fact(text)
    print(cjre.tagger(text))