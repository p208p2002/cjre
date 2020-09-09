# CJRE
## Install
```bash
$ pip install -U git+https://github.com/p208p2002/cjre.git
```
## Basic Usage
``` python
import cjre
from cjre import CJRE_jieba, CJRE_ckip

if __name__ == "__main__":
    print(cjre)
    
    # use jieba
    cjre = CJRE_jieba()

    # use ckip
    # CJRE_ckip.download_model() # download model first
    # cjre = CJRE_ckip()

    with open('test.txt','r',encoding='utf-8') as f:
        text = f.read().replace('\r\n','\n')
    
    # flags: https://github.com/fxsjy/jieba
    triple_res = cjre.extract_triple_res(text, stopwords=[])
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

## API
### cjre.CJRE_jieba
```python
def __init__(self, extra_dictionary_path=None):
```
```python
def tagger(self, text=''):
```
```python
def extract_triple_res(self, text, stopwords=[], relation_flags=['v.*','V.*'], split_by='，'):
```
### cjre.CJRE_ckip
```python
def __init__(self, ckip_data_path = './data', custom_dict_path=None, disable_cuda=True, cuda_memory_limit=2048)
```
```python
@staticmethod 
def download_model(from_gd=False)
```
```python
def tagger(self, text='')
```
```python
def extract_triple_res(self, text, stopwords=[], relation_flags=['v.*','V.*'], split_by='，'):
```