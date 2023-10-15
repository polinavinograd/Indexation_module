import nltk
from nltk.corpus import wordnet
from nltk import WordNetLemmatizer

LEMMATIZER = WordNetLemmatizer()

class NaturalLanguageUtils:
    @staticmethod
    def normalize(tokenized_text: list[str]) -> list:
        part_of_speech_tags = nltk.pos_tag(tokenized_text)
        new_part_of_speech_tags = []
        for tag in part_of_speech_tags:
            wn_part_of_speech = wordnet.ADJ
            if tag[1].startswith('N'):
                wn_part_of_speech = wordnet.NOUN
            elif tag[1].startswith('V'):
                wn_part_of_speech = wordnet.VERB
            elif tag[1].startswith('R'):
                wn_part_of_speech = wordnet.ADV
            new_tag = tuple([LEMMATIZER.lemmatize(tag[0], wn_part_of_speech), tag[1]])
            new_part_of_speech_tags.append(new_tag)
        return new_part_of_speech_tags
    
    @staticmethod
    def normalize_tokens_only(tokenized_text: list[str]) -> list[str]:
        return list(map(lambda tag: tag[0], NaturalLanguageUtils.normalize(tokenized_text)))