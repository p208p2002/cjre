import jieba
import jieba.posseg as pseg
import re
from ckiptagger_interface import ckiptagger
from tqdm import tqdm

class CJRE():
    def __init__(self, extra_dictionary_path=None):
        super().__init__()
        self.keep_flags = []
        self.stopwords = []
    
    def _set_keep_flags(self, keep_flags=[]):
        self.keep_flags = keep_flags
    
    def _set_stopwords(self, stopwords=[]):
        self.stopwords = stopwords
    
    def _remove_repeat_relations(self, results):
        for i,result in enumerate(results):
            result = '-'.join(result)
            results[i] = result
        results = list(set(results))
        results = [result.split("-") for result in results]
        return results
        
    def extract_triple_res(self, text, stopwords=[], relation_flags=['v.*','V.*'], split_by='，'):
        fact_text = text.replace('\n','')
        fact_text_lines = fact_text.split(split_by)

        #
        results = []
        pbar = tqdm(total=len(fact_text_lines))
        for fact_text_line in fact_text_lines:
            fact_text_line = fact_text_line.replace('-','')
            # find relation
            self._set_keep_flags(relation_flags)
            self._set_stopwords(stopwords)
            relations = self.tagger(fact_text_line)
            relations = [relation['words'] for relation in relations]

            # find persion
            self._set_keep_flags(['PER','PERSON'])
            self._set_stopwords(stopwords)
            roles = self.tagger(fact_text_line)
            roles = [role['words'] for role in roles]
            for i,role_a in enumerate(roles):
                for j,role_b in enumerate(roles):
                    if(role_a == role_b):
                        continue
                    #
                    for relation in relations:
                        if(re.match('%(role_a)s.*%(relation)s.*%(role_b)s'%({"role_a":role_a, "role_b":role_b, "relation":relation,}),fact_text_line)):
                            # print('%(role_a)s-%(relation)s-%(role_b)s'%({"role_a":role_a, "role_b":role_b, "relation":relation,}))
                            results.append([role_a,relation,role_b])
            pbar.update(1)
        pbar.close()

        # process repeat relations
        results = self._remove_repeat_relations(results)

        return results

class CJRE_jieba(CJRE):
    def __init__(self, extra_dictionary_path=None):
        super().__init__()
        jieba.enable_paddle()
        if extra_dictionary_path is not None:
            jieba.set_dictionary(extra_dictionary_path)
        jieba.initialize()
    
    def tagger(self, text=''):
        """
        keep_flags: https://github.com/fxsjy/jieba
        """
        words = pseg.cut(text,use_paddle=True) #paddle模式
        outs = []
        keep_flag_pattern = '|'.join(self.keep_flags)
        for word, flag in words:
            # print('%s %s' % (word, flag))
            if(re.match(keep_flag_pattern,flag) and word not in self.stopwords):
                outs.append({"words":word,"flag":flag})
        return outs

class CJRE_ckip(CJRE):
    def __init__(self, **args):
        super().__init__()
        self.ckip = ckiptagger(**args)
    
    @staticmethod
    def download_model(from_gd=False):
        from ckiptagger import data_utils
        if (from_gd):
            data_utils.download_data_gdown("./") # gdrive-ckip
        else:
            data_utils.download_data_url("./") # iis-ckip
    
    def tagger(self, text=''):
        outs = []
        sentences = self.ckip.parse([text])
        keep_flag_pattern = '|'.join(self.keep_flags)
        for sentence in sentences:
            for word in sentence:
                tag,pos,ner = word
                if (re.match(keep_flag_pattern,pos) and tag not in self.stopwords):
                    outs.append({"words":tag,"flag":pos})
                elif (re.match(keep_flag_pattern,ner) and tag not in self.stopwords):
                    outs.append({"words":tag,"flag":ner})
        return outs

class CJRE_hybrid(CJRE_jieba):
    def __init__(self, **args):
        super().__init__()
        self.ckip = ckiptagger(**args)
    
    @staticmethod
    def download_model(from_gd=False):
        from ckiptagger import data_utils
        if (from_gd):
            data_utils.download_data_gdown("./") # gdrive-ckip
        else:
            data_utils.download_data_url("./") # iis-ckip

    def extract_triple_res(self, text, stopwords=[], relation_flags=['v.*','V.*'], split_by='，'):
        fact_text = text.replace('\n','')
        fact_text_lines = fact_text.split(split_by)

        #
        results = []
        pbar = tqdm(total=len(fact_text_lines))
        for fact_text_line in fact_text_lines:
            fact_text_line = fact_text_line.replace('-','')
            # find relation
            self._set_keep_flags(relation_flags)
            self._set_stopwords(stopwords)
            relations = self.tagger(fact_text_line)
            relations = [relation['words'] for relation in relations]

            # find persion
            self._set_keep_flags(['PER','PERSON'])
            self._set_stopwords(stopwords)
            roles = self.tagger(fact_text_line)
            roles = [role['words'] for role in roles]
            for i,role_a in enumerate(roles):
                for j,role_b in enumerate(roles):
                    if(role_a == role_b):
                        continue
                    #
                    for relation in relations:
                        if(re.match('%(role_a)s.*%(relation)s.*%(role_b)s'%({"role_a":role_a, "role_b":role_b, "relation":relation,}),fact_text_line)):                            
                            try:
                                ckip_role_a_name = ''
                                role_a_is_person = False
                                ckip_parse_role_a = self.ckip.parse([role_a])[0]
                                for _role in ckip_parse_role_a:
                                    _tag, _pos, _ner = _role                                    
                                    if(_ner == 'PERSON'):
                                        role_a_is_person = True
                                        ckip_role_a_name = _tag
                                        break
                                
                                ckip_role_b_name = ''
                                role_b_is_person = False
                                ckip_parse_role_b = self.ckip.parse([role_b])[0]
                                for _role in ckip_parse_role_b:
                                    _tag, _pos, _ner = _role                                    
                                    if(_ner == 'PERSON'):
                                        role_b_is_person = True
                                        ckip_role_b_name = _tag
                                        break
                                    
                                relation = relation.replace(" ","")
                                if(role_a_is_person and role_b_is_person and relation != ""):
                                    results.append([ckip_role_a_name,relation,ckip_role_b_name])
                            except Exception as e:
                                print(e)  
            pbar.update(1)
        pbar.close()

        # process repeat relations
        results = self._remove_repeat_relations(results)

        return results
    