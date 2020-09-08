# CJRE
## Install
```bash
$ pip install -U git+https://github.com/p208p2002/cjre.git
```
## Usage
### cjre.extract_triple_res
``` python
from cjre import CJRE_jieba

if __name__ == "__main__":
    cjre = CJRE_jieba()

    with open('test.txt','r',encoding='utf-8') as f:
        text = f.read()
    
    # flags: https://github.com/fxsjy/jieba
    triple_res = cjre.extract_triple_res(text, stopwords=[], relation_flags=['v','vd','vn'])
    for triple_re in triple_res:
        print('-'.join(triple_re))
```
```
context: 
中華民國108年，王曉明造成王小美發生意外，王小美告王曉明

results:
王曉明-造成-王小美
王小美-告-王曉明
```