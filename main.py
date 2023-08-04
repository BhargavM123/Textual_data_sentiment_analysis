import glob
from pathlib import Path
import os
import pandas as pd
import scrapper
import helper

df = pd.read_excel(r'E:\Machine_learning_projects\Data_extraction_NLP\Utils\input_modified.xlsx')
url = df['URL'].tolist()
url_id = df['URL_ID'].tolist()


df_output = pd.read_excel(r'E:\Machine_learning_projects\Data_extraction_NLP\Utils\output_modified.xlsx')


a = open(r'E:\Machine_learning_projects\Data_extraction_NLP\Utils\universal_stopwords.txt',encoding ='latin-1')
stop_words = a.read()
universal_stopwords = stop_words.lower()


f = open(r'E:\Machine_learning_projects\Data_extraction_NLP\Utils\positive-words.txt',encoding ='latin-1')
p_stop_words = f.read()

fr = open(r'E:/Machine_learning_projects/Data_extraction_NLP/Utils/negative-words.txt',encoding ='latin-1')
n_stop_words = fr.read()

def Transformer(url_id,url):
  print(url, url_id)
  scrapper.scrapper(url_id, url)

for i in range(len(df)):
  Transformer(url_id[i],url[i])


path = r"E:/Machine_learning_projects/Data_extraction_NLP/files_text"

for file in glob.glob(f"{path}/[0-9]*.txt"):
  with open(file, 'r', encoding="utf-8") as f:
     f_name = (Path(file).stem)
     # print(f_name)

     l, num_of_sentences = helper.sent_tokenizer(file)

     strict_sent, total_words_strict_sent = helper.Meta_Stop_Words(l,universal_stopwords)

     p_word_count, ng_word_count, polarity_score, subjectivity_score = helper.derived_variables(strict_sent, total_words_strict_sent,p_stop_words,n_stop_words)


     nltk_sent, nltk_words, total_words, total_words_in_nltk_sent = helper.nltk_stopwords(l)

     avg_sent_len = helper.avg_sent_length(nltk_words,nltk_sent)

     complex_word_count, complex_word_perc, fog_index = helper.complex_words_all(nltk_sent,nltk_words,avg_sent_len)

     avvg_word_per_sent = helper.avg_word_per_sent(total_words_in_nltk_sent,nltk_sent)

     syllables_list = helper.syllable(total_words)

     personal_pnoun = helper.personal_pronoun(l)

     words_in_entire_article = helper.text_word_len(l)

     s = df_output[ (df_output['URL_ID'] == float(f_name))].index
     # print(s)
     # print(df_output.iloc[s])

     df_output.loc[s,['POSITIVE SCORE',	'NEGATIVE SCORE',	'POLARITY SCORE',	'SUBJECTIVITY SCORE',	'AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT',	'SYLLABLE PER WORD','PERSONAL PRONOUNS', 'AVG WORD LENGTH']] = [p_word_count,ng_word_count,polarity_score,subjectivity_score,avg_sent_len,complex_word_perc,fog_index,avvg_word_per_sent,complex_word_count,total_words_in_nltk_sent,syllables_list,personal_pnoun,words_in_entire_article]



df_output.to_excel("Output_excel_bm.xlsx")
