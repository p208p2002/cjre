import jieba
import jieba.posseg as pseg

class CJRE_jieba():
    def __init__(self, extra_dictionary_path=None):
        super().__init__()
        jieba.enable_paddle()
        if extra_dictionary_path is not None:
            jieba.set_dictionary(extra_dictionary_path)
        jieba.initialize()
        #
        self.keep_flags = []
        self.stopwords = []
    
    def set_keep_flags(self, keep_flags=[]):
        self.keep_flags = keep_flags
    
    def set_stopwords(self, stopwords=[]):
        self.stopwords = stopwords

    def tagger(self, text=''):
        """
        text: cj text
        keep_flags: https://github.com/fxsjy/jieba
                    标签	含义	标签	含义	标签	含义	标签	含义
                    n	普通名词	f	方位名词	s	处所名词	t	时间
                    nr	人名	ns	地名	nt	机构名	nw	作品名
                    nz	其他专名	v	普通动词	vd	动副词	vn	名动词
                    a	形容词	ad	副形词	an	名形词	d	副词
                    m	数量词	q	量词	r	代词	p	介词
                    c	连词	u	助词	xc	其他虚词	w	标点符号
                    PER	人名	LOC	地名	ORG	机构名	TIME	时间
        """
        words = pseg.cut(text,use_paddle=True) #paddle模式
        outs = []
        for word, flag in words:
            # print('%s %s' % (word, flag))
            if(flag in self.keep_flags and word not in self.stopwords):
                outs.append({"words":word,"flag":flag})
        return outs
    
    def extract_triple_re():
        pass

        