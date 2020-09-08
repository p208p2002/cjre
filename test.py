from cjre import CJRE_jieba
from VerdictCut.find_fact import extract_fact
from VerdictCut import find_roles
import re

if __name__ == "__main__":
    cjre = CJRE_jieba()
    cjre.set_keep_flags(['v','vd','vn'])
    cjre.set_stopwords(['上列','│'])

    with open('test.txt','r',encoding='utf-8') as f:
        text = f.read().replace('\r\n','\n')

    fact_text = text.replace('\n','')
    fact_text_lines = fact_text.split('，')

    #
    for fact_text_line in fact_text_lines:
        # find relation
        cjre.set_keep_flags(['v','vd','vn'])
        cjre.set_stopwords(['上列','│'])
        relations = cjre.tagger(fact_text_line)
        relations = [relation['words'] for relation in relations]

        # find persion
        cjre.set_keep_flags(['PER'])
        cjre.set_stopwords([])
        roles = cjre.tagger(fact_text_line)
        roles = [role['words'] for role in roles]
        for i,role_a in enumerate(roles):
            for j,role_b in enumerate(roles):
                if(role_a == role_b):
                    continue
                #
                for relation in relations:
                    if(re.match('%(role_a)s.*%(relation)s.*%(role_b)s'%({"role_a":role_a, "role_b":role_b, "relation":relation,}),fact_text_line)):
                        print('%(role_a)s-%(relation)s-%(role_b)s'%({"role_a":role_a, "role_b":role_b, "relation":relation,}))