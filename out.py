import cjre
from cjre import CJRE_hybrid
from VerdictCut.find_fact import extract_fact
import json
if __name__ == "__main__":
    cjre = CJRE_hybrid()

    with open('test.txt','r',encoding='utf-8') as f:
        text = f.read().replace('\r\n','\n')
    
    fact_text = extract_fact(text,break_line='\n')
    triple_res = cjre.extract_triple_res(fact_text, stopwords=[])

    out={}
    out['id'] = ''
    out['full_context'] = text
    out['year'] = ''
    out['entities'] = []
    out['relations']=[]

    for triple_re in triple_res:
        print(triple_re)
        role_a, relation, role_b = triple_re
        # entities
        out['entities'].append({
            "id": "",
            "name": role_a,
            "type": "PERSON",
        })
        out['entities'].append({
            "id": "",
            "name": role_b,
            "type": "PERSON",
        })
        # relations
        out['entities'].append({
            "id": "",
            "from": role_a,
            "to": role_b,
            "context": relation,
        })
    with open("out.json","w",encoding='utf-8') as f:
        f.write(json.dumps(out,ensure_ascii=False))