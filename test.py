from cjre import CJRE_jieba
from VerdictCut.find_fact import extract_fact
if __name__ == "__main__":
    cjre = CJRE_jieba()
    with open('test.txt','r',encoding='utf-8') as f:
        text = f.read()
    fact_text = extract_fact(text)
    print(cjre.tagger(text, keep_flags=['v','vd','vn'], stopwords=['上列','│']))