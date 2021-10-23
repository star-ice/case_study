# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import json
import spacy
import zh_core_web_trf
# import zh_core_web_sm
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from spacy.language import Language
from spacy.attrs import ORTH
import re
from spacy.tokens import Doc
from spacy.pipeline import EntityRuler
from spacy import displacy
from spacy.tokenizer import Tokenizer
from spacy.symbols import POS
from spacy.strings import StringStore
from spacy.pipeline import Tagger

# pre-defined variables
party_titles = ['三被告共同委托代理人', '两被申诉人的共同委托代理人', '被上诉人(原审原告、反诉被告)', \
                    '上述两被告的共同委托诉讼代理人', '代表人', '公司代表人', '法定代表人', '特别授权被告', \
                    '上诉人(原审第三人)', '上述两被告委托代理人', '上述两被告共同委 托诉讼代理人', \
                    '再审申请人(原审被告)', '委托代理人(特别授权)', '被申请人(一审被告、二审被上诉人)', \
                    '委托诉讼代理人(特别授权)', '被告委托代理人', '再审申请人', '诉讼委托代理人', '被告一', \
                    '拟稿人', '被上诉人(原审被告)', '上诉人(原审原告)', '被上诉人二(原审被告二)', \
                    '两被告共同委托代理人', '上诉人共同委托代理人', '原审被告', '被告二', '上诉人(原审被告、反诉原告)', \
                    '三上诉人的共同委托代理人', ' 再审申请人(一审原告)', '申诉人(一审原告、二审上诉人)', \
                    '支持起诉人', '两上诉人共同委托的诉讼代理人', '原审第二被告', '被上诉人一(原审被告一)', \
                    '一审被告', '原告', '被上诉人共同委托代理人', '原审第三人 ', '两原审被告共同委托代理人', \
                    '被告', '上述三上诉人共同委托代理人', '被上诉人(一审原告)', '授权代理人', '诉讼代表人', \
                    '被告(反诉原告)', '法人代表', '法人代表人', '法定代表人(负责人)', \
                    '两被上诉人共同的委托代理人', '上述两被告的委托 诉讼代理人', '申诉人(一审原告、二审被上诉人)', \
                    '(一审被告、二审被上诉人)', '一审第三人', '上诉人', '以上原告共同委托代理人', \
                    '以上二被上诉人的共同委托诉讼代理人', '申请再审人(原审被告)', '公益诉讼出庭人', \
                    '以上二被告共同委托代理人', '以上三被告共同委托代理人', '上述两被告的共同委托代理人', \
                    '以上两被告委托代理人', '被申诉人(一审被告、二审上诉人)', '两被上诉人的共同委托代理人', \
                    '二被告之共同委托诉讼代理人', '共同委托诉讼代理人', '两被告的共同委托代理人', '支持起诉机关', \
                    '上列两被上诉人委托代理人 ', '上述两被上诉人的共同委托诉讼代理人', '二被告共同委托诉讼代理人', \
                    '上列两被上诉人的委托代理人', ' 两被告共同的委托代理人', '上述两被告共同委托代理人', \
                    '被上诉人的共同委托诉讼代理人', '以上三被告共同的委托诉讼代理人', '抗诉机关', '被上诉人', \
                    '原审第三被告', '上诉人(一审原告)', '二被告共同委托代理人', '以上两被告共同委委托代理人', \
                    '两被申诉人共同委托诉讼代理人', '特别授权委托诉讼代理人', '两上诉 人共同委托代理人', \
                    '以上两被上诉人共同委托诉讼代理人', '上诉人(原审第一被告)', '申诉人(一审原告、二审上诉人、原再审申请人)', \
                    '第二被告', '被申请人(原审被告)', '上述两上诉人共同委托代理人', \
                    '被申诉人 (一审被告、二审被上诉人、原再审被申请人)', '再审申请人(一审原告、二审上诉人)', \
                    '两上诉人的共同委托代理人', '上列两被告的共同委托代理人', '上列两被告共同委托代理人', \
                    '被申请人(一审被告)', '原告共同委托诉讼代理人', '被申请人(一审被告、二审上诉人)', \
                    '上诉人共同委托诉讼代理人', '被申诉人(一审被告、二审 被上诉人)', '被上诉人(一审被告)', \
                    '上述二上诉人的共同委托诉讼代理人', '被申诉人(原审被告)', '二被上 诉人共同委托诉讼代理人', \
                    '上述两上诉人共同的委托诉讼代理人', '第三被告', '再审申请人(一审原告、二审被 上诉人)', \
                    '两上诉人共同委托诉讼代理人', '被申请人(一审原告、二审被上诉人)', '申诉人(原审原告)', \
                    '两被上诉人共同委托诉讼代理人', '诉讼代理人', '上诉人(一审被告)', '被申请人(原审原告)', \
                    '上诉人(原审被告)', '以上二上诉人共同的委托诉讼代理人', '上述两上诉人的共同委托代理人', \
                    '两上诉人的共同委托诉讼代理人', '上述两被上诉人委托诉讼代理人', '上上诉人(原审被告)', \
                    '第三人', '法定代理人', '被上诉人(原审第三人)', '原告(反诉被告)', '第一被告', \
                    '三被上诉人共同委托诉讼代理人', '委托代理人', '被申诉人(一审被告、二审被上诉人、再审被申请人)', \
                    '委托代理人(特别授权代理)', '两第三人的共同委托代理人', '被上诉人共同委托代理人(特别授权代理)', \
                    '再审申请人(一审被告、二审上诉人)', '以上两被告共同委托 代理人', '以上两被告的委托代理人', \
                    '上述两上诉人共同委托诉讼代理人', '上述被上诉人共同委托诉讼代理人 ', \
                    '二被委托代理人', '被申请人', '两被告共同委托诉讼代理人', '公益诉讼起诉人', \
                    '被上诉人(原审原告)', '上述两被上诉人共同委托代理人', '委托诉讼代理人', '上述被告共同委托诉讼代理人', \
                    '以上二被上诉 人委托代理人', '上列两被上诉人的共同委托代理人', '共同委托代理人', \
                    '再审申请人(原审原告)', '上述上诉人的委托诉讼代理人', '申诉人(一审原告、二审上诉人、再审申请人)', \
                    '二被上诉人的委托代理人', '上述两被上诉人的共同委托代理人', '上列二被告共同委托代理人', \
                    '以上两被告共同委托诉讼代理人', '执行事务合伙人', '投资人', '以上两被告的共同委托代理人',
                    '两被上诉人之共同委托代理人', '再审申请人(一审被告、二审被上诉人)', '被申请人(一审原告、二审上诉人)', \
                    '一审被告、二审被上诉人', '再审申请人:(一审第三人、二审上诉人)', '申请再审人(一审原告、二审上诉人)', \
                    '被申请人(一审被告,二审被上诉人)', '被申诉人(一审被告、二审被上诉人)',
                    '被申诉人(一审被告、二审被上诉人、原再审被申请人)', \
                    '上诉人(原告)', '上诉人(被告)', '原审当事人(原审被告)'
                    ]
plaintiff_titles = ['上诉人', '上诉人(一审原告)', '上诉人(一审第三人)', '上诉人(原告)', '上诉人(原审原告)', '上诉人(原审原告、反诉被告)',
                    '上诉人(原审原告人)', '上诉人(原审第三人)', '公益诉讼起诉人', '再审申请人', '再审申请人(一审原告)',
                    '再审申请人(一审原告、二审上诉人)',
                    '再审申请人(一审原告、二审被上诉人)', '再审申请人(原审原告)',
                    '再审申请人(原审原告、二审上诉人)', '再审申请人:(一审第三人、二审上诉人)', '原告',
                    '原告(反诉被告)', '抗诉机关', '支持起诉人',
                    '支持起诉机关', '申诉人(一审原告、二审上诉人)',
                    '申诉人(一审原告、二审上诉人、再审申请人)',
                    '申诉人(一审原告、二审上诉人、原再审申请人)',
                    '申诉人(一审原告、二审被上诉人)',
                    '申诉人(原审原告)',
                    '申请再审人(一审原告、二审上诉人)', '被上诉人(一审原告)', '被上诉人(原审原告)',
                    '被上诉人(原审原告、反诉被告)', '被上诉人(原甲原告)',
                    '被上诉人一(原审原告)',
                    '被上诉人一(原审被告一)',
                    '被上诉人二(原审被告二)', '被申请人(一审原告、二审上诉人)',
                    '被申请人(一审原告、二审被上诉人)', '被申请人(原审原告)']
defendant_titles = ['(一审被告、二审被上诉人)', '一审被告', '一审被告(二审上诉人)', '一审被告、二审被上诉人', '一审被告二审上诉人)',
                        '上上诉人(原审被告)', '上诉人(一审被告)', '上诉人(原审第一被告)', '上诉人(原审被告)',
                        '上诉人(原审被告、反诉原告)',
                        '上诉人(原审被告一)', '上诉人(被告)', '公益诉讼出庭人', '再审申请人(一审被告)',
                        '再审申请人(一审被告、二审上诉人)',
                        '再审申请人(一审被告、二审被上诉人)', '再审申请人(再审被告)', '再审申请人(原审被告)', '原审当事人(原审被告)',
                        '原审第三被告',
                        '原审第二被告',
                        '原审被告',
                        '原审被告(反诉原告)', '特别授权被告', '申请再审人(原审被告)',
                        '第一被告', '第三被告',
                        '第二被告',
                        '被上诉人',
                        '被上诉人(一审被告)', '被上诉人(原审第三人)',
                        '被上诉人(原审被告)',
                        '被上诉人(原审被告、反诉原告)',
                        '被上诉人(原审被告人)', '被告',
                        '被告(反诉原告)',
                        '被告一',
                        '被告二', '被申诉人(一审被告,二审被上诉人)',
                        '被申诉人(一审被告、二审上诉人)',
                        '被申诉人(一审被告、二审被上诉人)',
                        '被申诉人(一审被告、二审被上诉人、再审被申请人)',
                        '被申诉人(一审被告、二审被上诉人、原再审被申请人)',
                        '被申诉人(原审被告)',
                        '被申请人', '被申请人(一审被告)',
                        '被申请人(一审被告,二审被上诉人)',
                        '被申请人(一审被告、二审上诉人)',
                        '被申请人(一审被告、二审被上诉人)', '被申请人(原审被告)', '被申请人(原审被告、二审被上诉人)']
party_infos = ['身份证地址', '联系地址', '通信地址', '现住', '住', '营业场所', '信用代码', '籍贯', \
               '住址', '住址地', '所在地', '户籍所在地', '住所', '营业地', '身份证住址', \
               '港澳证件号码', '原名称', '注册号', '组织机构代码', '非公司私营企业住所', \
               '户籍地址', '身份证号码', '组织机构代码证', '公⺠身份号码', '营业执照', \
               '身份号码', '营业执照注册号', '住所地', '执照注册号', '经营场所', '身份证住址', \
               ' 个体工商户营业执照注册', '机构代码', '户籍住所', '统一信用代码', '原名称', \
               '身份证地址', '经营地址', '身份证登记住址', '组织机构代码证号', '执业证号', \
               '曾用名', '统一社会信用代码', '工商注册号', '身份证号', '注册号', '营业场所', \
               '居⺠身份证', '地址', '现住址', '经常居住地', '代理权限', '户籍地', \
               '营业执照号码', '公⺠身份证号', '中文名称 ', '所在地', '户籍地址', \
               '组织机构代码证', '公⺠身份号码', '代码', '经营业主', '经营场所', \
               '身份证登记住址', '统一社会信用代码', '地址', '注册号', '营业场所', '居⺠身份证号码', \
               '户籍地', '身份证住址', '公民身份号码', '公民身份证号码']
party_occupations = ['律师', '经理', '总经理', '董事长', '法务', '无职业', '业主', '员工', '店长', \
                     '主管', '经营者', '董事', '职员', '部长', '负责人']
cost_type = ['货款', '价款', '受理费', '赔偿金', '公证费', '诉讼费', '购物款', '上诉费', '公告费', '运费',
             '交通费', '误工费', '打印费', '鉴定费', '邮寄费', '赔偿款', '医疗费', '购酒款', '购药款',
             '住宿费', '产品质量监督检验费', '其他费用', '餐饮费', '购货款', '减半', '合计', '共计',
             '管辖权异议费', '十倍价款', '十倍货款', '价款的十倍', '货款的十倍', '十倍购物款', '餐费',
             '检测费', '三倍货款']
judge_titles = ['审判长', '审判员', '人民审判员', '助理审判员', '代理审判员', '人民陪审员']
party_titles = list(set(party_titles + plaintiff_titles + defendant_titles))

#还有各种之姐， 之夫， 之父， 之母， 之妻， 之子， 之女， 之， 的， 系， 是， 原告提供， 需要补充
partytitle_token_pattern = [{"TEXT": {"IN": list(party_titles), "NOT_IN": ["系原告", "与原告", "是原告",
                                                                           "和原告", "为原告", "系被告",
                                                                           "与被告", "是被告", "和被告",
                                                                           "为被告", "原告之", "被告之",
                                                                           "原告的", "被告的"]}}]
partyinfo_token_pattern = [{"TEXT": {"IN": list(party_infos)}}]
partyoccup_token_pattern = [{"TEXT": {"IN": list(party_occupations)}}]

# reasons大致分类参考Reason Keywords表格
# ct_pattern_1_1 = [{"ORTH": {"IN": ["不安全", "不合格", "假冒"]}}, {"OP": "*"}, {"ORTH": {"IN": ["食品", "产品"]}}]
# ct_pattern_1_2 = [{"ORTH": {"IN": ["产品", "食品"]}}, {"OP": "*"}, {"ORTH": {"IN": ["不合格", "不符合"]}}]
# ct_pattern_2 = [{"ORTH": {"IN": ['国家安全标准食品添加剂使用标准', '饮料通则', '预包装饮料酒标签通则']}}]
# ct_pattern_3 = [{"ORTH": {"IN": ["不符合", "违反", "无"]}}, {"OP": "*"}, {"ORTH": {"IN": ["食品安全", "安全食用标准", "安全标准", "质量安全"]}}]
# # ct_pattern_3 = [{"ORTH": {"REGEX": "违反"}}, {"OP": "*"}, {"ORTH": {"REGEX": "食品安全"}}]
# ct_pattern_4_1 = [{"ORTH": {"IN": ['产品标准代号', '产品说明', '标签', '标识', '预包装饮料酒标签通则']}}]
# ct_pattern_4_2 = [{"ORTH": {"IN": ["未标注", "没有标注"]}}, {"OP": "*"}, {"ORTH": "成分"}]
# ct_pattern_5 = [{"ORTH": {"IN": ['保质期', '生产日期', '过期']}}]
# ct_pattern_6 = [{"ORTH": {"IN": ['原始配料', '原料', '原材料', '非药食同源物质', '添加剂', '非食用物质', '食品原料']}}]
# ct_pattern_7 = [{"ORTH": "欺诈"}]
# ct_pattern_8 = [{"ORTH": {"IN": ['商标专用权', '商标违法']}}]
# ct_pattern_9 = [{"ORTH": "出入境检验"}]
# ct_pattern_10 = [{"ORTH": {"IN": ['生产许可证编号', '生产许可编号', '生产许可证']}}]




# 定义一个合并字典值的工具类

judgeresult_verbs = ["赔偿", "退还", "负担", "返还", "支付",
                     "赔付", "承担", "收取", "迳付", "给付",
                     "交纳", "缴纳", "担负", "退款"]
specific_words = ["本判决", "发生法律效力之日起", "发生法律效力后",
                  "本判决生效之日起", "本判决生效后", "于", "内",
                  "向", "计", "本判决书生效后", "系原告", "与原告",
                  "是原告", "和原告", "为原告", "系被告", "与被告",
                  "是被告", "和被告", "为被告", "原告之", "被告之",
                  "内容", "其中", "从轻处罚", "从重处罚", "诉讼事实",
                  "牌", "不予支持", "予以支持", "淘宝网", "天猫商城"]
illegal_reasons = ["不安全", "不合格", "不符合",
                  "国家安全标准食品添加剂使用标准", "饮料通则",
                  "预包装饮料酒标签通则", "没有标注",
                  "未标注", "产品标准代号", "产品说明", "原始配料",
                  "非药食同源物质", "非食用物质", "食品原料",
                  "商标专用权", "商标违法", "出入境检验", "生产许可证编号",
                  "生产许可编号", "生产许可证", "食品安全",
                  "安全食用标准", "安全标准", "质量安全", "标签",
                   "原材料", "营养成分表", "外包装", "配料表", "预包装"]
food_words = ['伏特加', "果蔬", "脆爽果蔬脆", "脆爽鲜枣脆"]

money_re = r"(?P<money_amount>([零一二三四五六七八九十百千万亿角元\d+\.,]*)(?=[角|元])[角|元])"
@Language.component("money_recognizer")
def money_recognizer(doc):
    for match in re.finditer(money_re, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end, label="MONEY_RECOGNIZER")
        if span is not None:
            doc.ents = list(doc.ents) + [span]
    return doc

@Language.component("merge_zh_noun_chunks")
def merge_zh_noun_chunks(doc):
    nc_end = 0
    tspan = []
    with doc.retokenize() as retokenizer:
        for token in doc:
            if token.text in party_titles: continue
            temp = token.i
            if token.tag_ in ["NN", "JJ"] \
                    and token.pos_ in ["NOUN", "ADJ"]: \
                    # and "nmod" not in token.dep_:
                tspan.append(token.i)
                nc_end = token.i
            if (temp > nc_end and nc_end != 0) or (temp==len(doc)-1):
                if len(tspan) > 1:
                    for j in tspan:
                        if doc[tspan[-1]].tag_ != "NN" and doc[tspan[-1]].pos_ != "NOUN":
                            tspan = tspan[:-1]
                if len(tspan) > 1:
                    # print(tspan, doc[tspan[0]:tspan[-1]+1])
                    retokenizer.merge(doc[tspan[0]:tspan[-1]+1])
                nc_end = token.i
                tspan = []
    return doc

def merge_dict(x,y):
    for k,v in x.items():
                if k in y.keys():
                    y[k] += v
                else:
                    y[k] = v
    return y

class CustomSpacy:
    '''
    This class is for specific settings for spacy
    :return: nlp class
    '''
    def __init__(self):
        # 使用指定的string list作为matcher词库去匹配
        # self.nlp = spacy.load("zh_core_web_trf")
        self.nlp = spacy.load("zh_core_web_lg")
        self.patterns_ptitles = list(self.nlp.pipe(party_titles))
        self.patterns_pinfos = list(self.nlp.pipe(party_infos))
        self.patterns_poccups = list(self.nlp.pipe(party_occupations))
        self.patterns_jtitles = [self.nlp.make_doc(text) for text in judge_titles]
        self.nlp.tokenizer.pkuseg_update_user_dict(cost_type)
        self.nlp.tokenizer.pkuseg_update_user_dict(party_titles)
        self.nlp.tokenizer.pkuseg_update_user_dict(party_infos)
        self.nlp.tokenizer.pkuseg_update_user_dict(judge_titles)
        # 细微分词调节
        self.nlp.tokenizer.pkuseg_update_user_dict(judgeresult_verbs)
        self.nlp.tokenizer.pkuseg_update_user_dict(specific_words)
        self.nlp.tokenizer.pkuseg_update_user_dict(illegal_reasons)
        self.nlp.tokenizer.pkuseg_update_user_dict(food_words)

    def global_entity_ruler(self):
        # 使用entityruler帮助nlp识别特定的实体(费用类型、当事人等等)
        # Entity Ruler V3 (The use of add_pipe was changed because of the version update of spacy)
        # Add necessary patterns to global entityruler(including party_titles, party_infos, cost_types, judge_verbs from lists)
        # global_entityruler = EntityRuler(nlp, overwrite_ents=True)
        if "global_entityruler" in list(self.nlp.pipe_names):
            self.nlp.remove_pipe("global_entityruler")
        global_entityruler = self.nlp.add_pipe("entity_ruler", name="global_entityruler", after="ner")
        patterns_cost_type = [{"label": "COST_TYPE", "pattern": str(i)} for i in cost_type]
        patterns_party_title = [{"label": "PARTY_TITLE", "pattern": str(i)} for i in party_titles]
        patterns_party_info = [{"label": "PARTY_INFO", "pattern": str(i)} for i in party_infos]
        patterns_judgere_verbs = [{"label": "JUDGE_VERB", "pattern": str(i)} for i in judgeresult_verbs]
        global_entityruler.add_patterns(patterns_cost_type)
        global_entityruler.add_patterns(patterns_party_title)
        global_entityruler.add_patterns(patterns_party_info)
        global_entityruler.add_patterns(patterns_judgere_verbs)

    def attribute_ruler(self):
        # 使用自定义的pos mapping table来对一些词汇指定词性
        attribute_ruler = self.nlp.get_pipe("attribute_ruler")
        tagger_pattern = [{"TEXT": {"IN": list(judgeresult_verbs)}}]
        tagger_attrs1 = {"POS": "VERB"}
        attribute_ruler.add(patterns=[tagger_pattern], attrs=tagger_attrs1)

    def add_money_recognizer(self):
        self.nlp.vocab.strings.add('money_recognizer')
        self.nlp.add_pipe("money_recognizer", name="money_recognizer", before="tagger")

    def add_merge_entities(self):
        self.nlp.add_pipe("merge_entities", after="ner")  # merge一般都在ner之后~
        self.nlp.add_pipe("merge_zh_noun_chunks", last=True)
        self.nlp.add_pipe("sentencizer")

    def most_similar(self, word, topn=5):
        word = self.nlp.vocab[str(word)]
        queries = [
            w for w in word.vocab
            if w.is_lower == word.is_lower and w.prob >= -15 and np.count_nonzero(w.vector)
        ]

        by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
        return [(w.lower_, w.similarity(word)) for w in by_similarity[:topn + 1] if w.lower_ != word.lower_]


if __name__=="__main__":
    cs = CustomSpacy()
    cs.global_entity_ruler()
    cs.attribute_ruler()
    cs.add_money_recognizer()
    cs.add_merge_entities()
    nlp = cs.nlp
    test_text1 = "一是加贴了两张伏特加酒标签; 二是保质期格式不符合规定。本院认为:沃尔玛马鞍山雨山东路分店、保乐力" \
                 "加公司作为食品、酒类的经营者,所销售的商品应当符合国" \
                "家相关规定。沃尔玛马鞍山雨山东路分店销售给刘建红的绝对伏特加酒,该酒瓶上另加贴贮存条件、经销商" \
                "及地址,不符合《预包装饮料酒标签通则》(中华人民共和国国家标准GB10344-2005)第4.11条“所有标" \
                "示内容均不应另外加贴、补印或篡改”的规定,故刘建红要求被告退还货款208元的诉讼请求,本院予以支持。"
    test_text2 = "经审理查明,2012年8月原告在被告处购买了千家素果牌脆爽果蔬脆、脆爽鲜枣脆" \
                 "食品,共计付款人民币2,826元。" \
                 "其中脆爽果蔬脆产品声称低脂肪,产品标签营养成分表" \
                 "内容标示:每100克含有脂肪17.1g。其中脆爽鲜枣脆产品声称低热量,产品标签营养成分表" \
                 "内容标示:每100克含有能量1,289.3千卡。国家法律法规规定,低能量的定义为固体食品" \
                 "170KJ/100g,液体食品80KJ/100g。2013年3月上海市工商行政管理局浦东新区分局对" \
                 "被告作出行政处罚决定书,载明:……当事人销售的这款千家素果牌脆爽果蔬脆食品为一款" \
                 "固体食品,……营养成分表中的脂肪含量标明有每100g和脂肪17.1g等字样,……其外包装食品" \
                 "标签又标示有本产品具有低脂肪、高纤维的特点。……等字样。……按照该规定的附件3食品营养" \
                 "声称和营养成分功能声称准则……,声称为低脂肪的固体食品必须符合每100克食品中脂肪含量" \
                 "小于等于3克的要求,……因此,这款食品外包装食品标签含有虚假的内容。……我们认为,当事人" \
                 "销售的食品的标签含有虚假的内容,违反了中华人民共和国食品安全法第四十八条第一款食品" \
                 "和食品添加剂的标签、说明书,不得含有虚假、夸大的内容,……之规定。……作出从轻处罚如下" \
                 ":1、没收违法所得贰仟壹佰玖拾陆圆柒角陆分,2、罚款贰万玖仟捌佰贰拾圆整。2013年11月," \
                 "原告提起本案诉讼。以上事实,由原告提供的行政处罚决定书、照片、购物发票及清单等证据及" \
                 "当事人的当庭陈述等在案佐证。"
    doc = nlp(test_text2)
    # print(nlp.pipeline)
    # for i in doc:
    #     print(i, i.tag_, i.pos_, i.dep_, i.vector[:5], i.is_oov, i.has_vector)
    # w1 = nlp.vocab['标签']
    # w2 = nlp.vocab['食品外包装食品标签']
    # w1_w2 = w1.similarity(w2)
    ms = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings['标签']]]), n=10)
    print([nlp.vocab.strings[w] for w in ms[0][0]])


