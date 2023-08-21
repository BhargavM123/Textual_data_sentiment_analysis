import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
from collections import Counter

stop_words = set(stopwords.words('english'))

def sent_tokenizer(file):
  file_content = open(file, encoding="utf-8").read()
  tokens = nltk.sent_tokenize(file_content)

  l = [s for s in tokens]
  no_of_sentences = len(l)

  return l, no_of_sentences

def Meta_Stop_Words(sent, h):
  new_words = []

  for message in sent:
    for word in message.lower().split():
      if word not in h:
        new_words.append(word)

  inter_sent = " ".join(new_words)
  new_tokens = nltk.sent_tokenize(inter_sent)
  strict_sent = [s for s in new_tokens]
  ss = str(strict_sent)
  words = ss.split()

  return strict_sent, len(words)


def derived_variables(strict_sent, len_Words,p_stop_words,n_stop_words):
  p_sent = p_stop_words.lower()

  p_word_count = 0
  for message in strict_sent:
    for word in message.lower().split():
      if word in p_sent:
        p_word_count += 1

  n_sent = n_stop_words.lower()

  ng_word_count = 0
  for message in strict_sent:
    for word in message.lower().split():
      if word in n_sent:
        ng_word_count += 1

  polarity_score = (p_word_count - ng_word_count)/((p_word_count + ng_word_count) + 0.000001)

  subjectivity_score = (p_word_count + ng_word_count)/ ((len_Words) + 0.000001)

  return p_word_count, ng_word_count, polarity_score, subjectivity_score



def nltk_stopwords(sent):
  nltk_stop_w = []

  for message in sent:
    for word in message.lower().split():
      if word not in stop_words:
        nltk_stop_w.append(word)

  words_wo_stop = " ".join(nltk_stop_w)

  new_tokens = nltk.sent_tokenize(words_wo_stop)
  nltk_sent = [s for s in new_tokens]
  ns = str(nltk_sent)
  nltk_words = ns.split()

  re_words_wo_stop = re.sub('\d+', '', words_wo_stop) #without digits

  tokenizer = RegexpTokenizer(r'\w+')
  total_words = tokenizer.tokenize(re_words_wo_stop)
  l_tw = len(total_words)

  return nltk_sent, nltk_words, total_words, l_tw


def avg_sent_length(nltk_words,nltk_sent):
  avg_sentence_len = len(nltk_words)/len(nltk_sent)
  return avg_sentence_len


def complex_words_all(nltk_sent,nltk_words,avg_sentence_len):
  #complex words
  cw_count = 0

  for myword in nltk_words:
      d = {}.fromkeys('aeiou',0)
      haslotsvowels = False
      for x in myword.lower():
          if x in d:
              d[x] += 1
      for q in d.values():
          if q > 2:
              haslotsvowels = True
      if haslotsvowels:
          cw_count += 1

  complex_word_perc = (cw_count / len(nltk_words)) * 100

  fog_index = 0.4 * (avg_sentence_len + complex_word_perc)

  return cw_count, complex_word_perc,fog_index


def avg_word_per_sent(total_words_in_nltk_sent,nltk_sent):
  Avg_words_per_sent = total_words_in_nltk_sent/len(nltk_sent)
  return Avg_words_per_sent


def total_words(words_wo_stop):
  re_words_wo_stop = re.sub('\d+', '', words_wo_stop) #without digits

  tokenizer = RegexpTokenizer(r'\w+')
  total_words = tokenizer.tokenize(re_words_wo_stop)
  l_tw = len(total_words)

  return total_words, l_tw



def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("es"):
        count -= 1
    if word.endswith("ed"):
        count -= 1
    if count == 0:
        count += 1
    return count

def syllable(total_words):
  # total_words = str(total_words)
  sc_list = []
  for word in total_words:
    sc = syllable_count(word)
    sc_list.append(sc)

  g = ",".join(str(sc_list))
  avg_syllable = sum(sc_list)/ len(sc_list)
  return avg_syllable


def personal_pronoun(sent):
    pp = re.findall(r'\b(us|I|we|my|ours|and)\b', str(sent))
    count = dict(Counter(pp))
    stri = ''
    for key in count:
        stri += key + '-' + str(count[key]) + ', '

    return stri[:-2]


def text_word_len(sent):
  sentence = str(sent)
  words = sentence.split()
  z = sum(map(len, words))/len(words)
  return z