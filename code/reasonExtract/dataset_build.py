# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import json
import string
import spacy
import zh_core_web_trf
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
from toolkit import CustomSpacy
from toolkit import party_titles

'''
building phrase embedding model dataset
example: 2014/01, use one month text to build data set in paper

dataset format:(dataframe)
id: case_id
reason topic: one of the above reason topics
content: ascertain content
content_vector: doc.vector
topic phrases: noun phrases in content

corpus:(dataframe)
includes all phrases and their vector representation
'''

base_url = "/Users/starice/OwnFiles/cityu/RA/"
output_base_url = "/Users/starice/OwnFiles/cityu/RA/case_study/phrase_embedding/dataset/"
pre_dir = ['type1', 'type2', 'type3', 'type4']
dir_name = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
dir_sname = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
filter_named_entities = ['DATE', 'TIME', 'PERCENT', 'MONEY', 'MONEY_RECOGNIZER',
                         'PARTY_TITLE', 'QUANTITY', 'ORDINAL', 'CARDINAL',
                         'COST_TYPE', 'PARTY_INFO', 'JUDGE_VERB', 'PERSON', 'ORG',
                         'GPE']
filter_pos_tag = ['INTJ', 'AUX', 'CCONJ', 'ADP', 'DET', 'NUM',
                  'PART', 'PRON', 'SCONJ', 'PUNCT', 'SYM', 'X']

def import_text_perfile(file_path):
    '''
    Import case reason text(monthly) from json files
    :param file_path:
    :return: case reason text string
    '''
    pertext = {}
    if not os.path.isdir(file_path):  # 判断是否是文件夹，不是文件夹才打开
        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)
        dict_data = json.loads(data)
        id = dict_data['returnData']['id']
        temppertext = ""
        for i in dict_data['returnData']['segments']:
            if i['type'] == "COURT_HELD":
                temptext = i['text']
                temptext = temptext.replace("“", "")
                temptext = temptext.replace("”", "")
                temptext = temptext.replace("《", "")
                temptext = temptext.replace("》", "")
                temptext = temptext.replace(";", ",")
                temptext = re.sub(r'[一二三四五六七八九十]、', '', temptext)
                temptext = re.sub(r"\([^()<>]*\)", "", temptext)
                temppertext += temptext
        pertext[id] = temppertext
    return pertext



def generate_candidate(nlp, str_text):
    '''
    Split text string into unigram tokens, as well as noun phrases and named entities with Spacy,
    Filter tokens above by criteria settled in paper(II.A)
    :param str_text:
    :return: phrases list
    '''
    candidates = {}
    doc = nlp(str_text)

    # additional filter logic:
    # For each token(has noun chunks) in doc,
    # if the len of token is less than 1, drop it
    # if token is a punctuation, drop it
    for i in doc: # i is token class
        # The begin token of named entity
        if i.tag_ == "NN" and i.pos_ == "NOUN" and \
                "nmod" not in i.dep_: #避免名词短语是在句子里是所有格的作用
            if i.is_digit: continue
            if i.is_stop: continue
            if i.ent_type_ in filter_named_entities: continue
            candidates[i.text] = i.vector.tobytes()
    return candidates, doc.vector.tobytes()

def split_filter_text(nlp, str_text):
    doc = nlp(str_text)
    splitted_text = ""
    for i in doc:
        if i.is_digit: continue
        if i.is_stop: continue
        # if i.ent_type_ in filter_named_entities: continue
        splitted_text += (i.text + " ")
    return splitted_text

def filter_phrase(candidates):
    new_candidates = {}
    for k, v in candidates.items():
        if len(k) <= 1: continue
        if True in [str(char[0]).isdigit() for char in k]: continue
        if True in [str(char[0]) in string.punctuation for char in k]: continue
        if any(pt in k for pt in party_titles): continue #如果名词短语中出现原告title信息，也要被过滤掉
        new_candidates[k] = v
    if len(new_candidates) > 1: return new_candidates
    return None

def build_dataset(pre_dir, dir_name, dir_sname):
    '''
    Build corpus for phrase embeddings dataset
    :param pre_dir:
    :param dir_name:
    :param dir_sname:
    :return:
    '''
    dataset = pd.DataFrame(columns=['id', 'reason_topic',
                                    'content', 'content_vector',
                                    'topic_phrases', 'phrase_vectors'])
    vocab = pd.DataFrame(columns=[''])
    cs = CustomSpacy()
    cs.global_entity_ruler()
    cs.attribute_ruler()
    cs.add_money_recognizer()
    cs.add_merge_entities()
    nlp = cs.nlp

    for i in pre_dir:
        for j in dir_name:
            document = ""
            for k in dir_sname:
                url = base_url + i + "/" + j + "/" + k + "/json"
                if not os.path.exists(url):
                    print("路径不存在！", url)
                    return
                print("----------------------------executing path: ", url)

                # 处理哪部分case文件就引入哪部分的party patterns
                party_entityruler_pattern_path = "/Users/starice/Desktop/" + "party_entityruler_files/" + "entityruler_patterns_" + str(
                    i) + "_" + str(j) + "_" + str(k) + ".jsonl"
                if not os.path.exists(party_entityruler_pattern_path):
                    print("Entityruler patterns file 路径不存在！使用默认的entity ruler可能会影响金额承担者的提取！",
                          party_entityruler_pattern_path)
                else:
                    name = "party_entityruler_" + str(i) + "_" + str(j) + "_" + str(k)
                    if name not in list(nlp.pipe_names):
                        config = {"overwrite_ents": True}
                        party_entityruler = nlp.add_pipe("entity_ruler", name=name, after="ner", config=config)
                        party_entityruler.from_disk(party_entityruler_pattern_path)
                        print("entityruler has been added!!!! ", name)

                files = os.listdir(url)  # 得到文件夹下的所有文件名称
                for file in files:  # 遍历文件夹
                    if os.path.splitext(file)[-1][1:] != "json": continue
                    pertext = import_text_perfile(url + "/" + file)
                    if len(pertext) > 0:
                        for k, v in pertext.items():
                            id = k
                            content = v
                            reason_topic = "unknown"
                            phrases, doc_vector = generate_candidate(nlp, content)
                            new_content = split_filter_text(nlp, content)
                            phrases = filter_phrase(phrases)
                            content_vector = doc_vector
                            if phrases != None:
                                topic_phrases = list(phrases.keys())
                                phrase_vectors = list(phrases.values())
                            else:
                                topic_phrases = None
                                phrase_vectors = None
                            dataset = dataset.append({
                                "id": id,
                                "content": new_content,
                                "content_vector": content_vector,
                                "reason_topic": reason_topic,
                                "topic_phrases": topic_phrases,
                                "phrase_vectors": phrase_vectors},
                                ignore_index=True)

    return dataset


def build_phrases(pre_dir, dir_name, dir_sname):
    '''
    Build dataset for training phrase embeddings
    :param pre_dir: type1
    :param dir_name: 2014
    :param dir_sname: 1
    :return:
    '''
    phrase_list = []
    cs = CustomSpacy()
    cs.global_entity_ruler()
    cs.attribute_ruler()
    cs.add_money_recognizer()
    cs.add_merge_entities()
    nlp = cs.nlp

    for i in pre_dir:
        for j in dir_name:
            document = ""
            for k in dir_sname:
                url = base_url + i + "/" + j + "/" + k + "/json"
                if not os.path.exists(url):
                    print("路径不存在！", url)
                    return
                print("----------------------------executing path: ", url)
                # 处理哪部分case文件就引入哪部分的party patterns
                party_entityruler_pattern_path = "/Users/starice/Desktop/" + "party_entityruler_files/" + "entityruler_patterns_" + str(
                    i) + "_" + str(j) + "_" + str(k) + ".jsonl"
                if not os.path.exists(party_entityruler_pattern_path):
                    print("Entityruler patterns file 路径不存在！使用默认的entity ruler可能会影响金额承担者的提取！",
                          party_entityruler_pattern_path)
                else:
                    name = "party_entityruler_" + str(i) + "_" + str(j) + "_" + str(k)
                    if name not in list(nlp.pipe_names):
                        config = {"overwrite_ents": True}
                        party_entityruler = nlp.add_pipe("entity_ruler", name=name, after="ner", config=config)
                        party_entityruler.from_disk(party_entityruler_pattern_path)
                        print("entityruler has been added!!!! ", name)

                files = os.listdir(url)  # 得到文件夹下的所有文件名称
                for file in files:  # 遍历文件夹
                    if os.path.splitext(file)[-1][1:] != "json": continue
                    pertext = import_text_perfile(url + "/" + file)
                    if pertext != "":
                        document += pertext
            phrases = split_filter_text(nlp, document)
            phrase_list += phrases

    # phrase_list = list(set(phrase_list))
    phrase_list = filter(filter_phrase, phrase_list)
    return list(phrase_list)

if __name__ == "__main__":
    phrases = build_dataset(pre_dir[:1], dir_name[3:4], dir_sname[:])
    i = "-".join(pre_dir[:1])
    j = "-".join(dir_name[3:4])
    k = "-".join(dir_sname[:])
    # with open("/Users/starice/Desktop/noun_phrases/" + str(i) + "_" + str(j) + "_" + str(
    #         k) + "_" + "nps.txt", "w+", encoding="utf-8") as f:
    #     f.write(str(len(phrases)) + " " + str(phrases[0][1].shape) + "\n")
    #     for phrase in phrases:
    #         f.write(str((phrase[0], phrase[1].tostring())) + "\n")
    if phrases is not None:
        phrases.to_csv("/Users/starice/Desktop/noun_phrases/" + str(i) + "_" + str(j) + "_" + str(
                k) + "_" + "nps.csv")