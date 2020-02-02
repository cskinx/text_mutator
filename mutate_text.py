from fitbert import FitBert
from nltk.corpus import wordnet
import random
from transformers import BertTokenizer, BertModel, BertForMaskedLM
import torch
import re
import sys



class WordMasker:

	def __init__(self, mask_str):
		self.mask_str = mask_str

	def mask_word_in_sent(self, sent, word_span):
		pre_w = sent[:word_span[0]]
		post_w = sent[word_span[1]:]
		return f"{pre_w}{self.mask_str}{post_w}"

	def unmask_word_in_sent(self, sent, new_word):
		mask_pos = sent.index(self.mask_str)
		mask_end = mask_pos + len(self.mask_str)
		pre_w = sent[:mask_pos]
		post_w = sent[mask_end:]
		return f"{pre_w}{new_word}{post_w}"


class FBReplacer:

	def __init__(self, model_name):
		self.fb = FitBert(model_name=model_name)
		self.mask = "***mask***"

	def find_new_word(self, sent, options):
		""" in a given sentence, replace word at word_span 
		with one of the options"""
		# print(f"masked={masked}, options={options}")
		ranked = self.fb.rank(sent, options=options)

		best_ranked = ranked[0]

		return best_ranked

class MLMReplacer:

	def __init__(self, model_name):
		self.model = BertForMaskedLM.from_pretrained(model_name)
		self.model.eval()
		self.tokenizer = BertTokenizer.from_pretrained(model_name)
		self.mask = "[MASK]"

	def find_new_word(self, sent, options):
		""" in a given sentence, replace word at word_span.
		options are ignored."""
		text = f"[CLS] {sent} [SEP]"
		tokenized_text = self.tokenizer.tokenize(text)
		indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
		segments_ids = [0]*len(indexed_tokens)
		# Convert inputs to PyTorch tensors
		tokens_tensor = torch.tensor([indexed_tokens])
		segments_tensors = torch.tensor([segments_ids])

		masked_index = tokenized_text.index("[MASK]")
		if not masked_index:
			print("Error: [MASK] is missing")
			return

		# Predict all tokens
		with torch.no_grad():
			outputs = self.model(tokens_tensor, token_type_ids=segments_tensors)
			predictions = outputs[0]

		# print(f"predictions: {predictions}")

		predicted_index = torch.argmax(predictions[0, masked_index]).item()
		predicted_token = self.tokenizer.convert_ids_to_tokens([predicted_index])[0]

		return predicted_token


class WordReplacer:

	def __init__(self, replacer, get_syns, excluded=[]):
		self.replacer = replacer
		self.wmasker = WordMasker(mask_str=replacer.mask)
		self.get_syns = get_syns
		self.excluded = excluded

	def replace_word(self, sent, word_span):
		rpl = sent[word_span[0]:word_span[1]]
		rpl_syns = self.get_syns(rpl)
		# print(f"replace {rpl} with {rpl_syns}")

		masked_sent = self.wmasker.mask_word_in_sent(sent, word_span)
		new_word = self.replacer.find_new_word(masked_sent, rpl_syns)
		new_sent = self.wmasker.unmask_word_in_sent(masked_sent, new_word)

		if rpl == new_word or \
			new_word in self.excluded or \
			"#" in new_word:
			return sent
			
		return new_sent




def get_synonyms(word):
	""" get synonyms for word from wordnet and return set """
	syns = []
	ans = []
	for t in wordnet.synsets(word):
		# print(wordnet.synsets(word))
		for lemma in t.lemmas():
			syns.append(lemma.name())
			if lemma.antonyms():
				ans.append(lemma.antonyms()[0].name())

	syans = set(syns + ans + [word])
	syans = [w for w in syans if not "_" in w]
	return set([s.lower() for s in syans])

def get_word_span(sent, word_index):
	""" returns the span of a random word in the sentence. """

	sent_split = sent.split()
	rnd_word_ind = random.randint(0, len(sent_split)-1)
	## sum up lengths of previous words
	words_left_len = sum(len(w) for w in sent_split[:word_index])
	## total sentence length before the word (add blanks)
	w_start = words_left_len + word_index
	w_end = w_start + len(sent_split[word_index])

	return (w_start, w_end)

def mutate_sentence(wreplacers, sent):
	sent_hist = [sent]
	newest_sent = sent

	## roughly touch each word 3 times
	iter_cnt = len(sent.split()) * 3
	for i in range(iter_cnt):
		has_changed = False
		for wreplacer in wreplacers:				
			## create word order for changes
			## strip sentence end punctuations
			sent_stripped = re.sub(r"[!\.\? ]*$", "", newest_sent)
			word_inds = list(range(0, len(sent_stripped.split())))
			## shuffle
			word_inds = random.sample(word_inds, len(word_inds))

			for word_ind in word_inds:
				## pick a random word
				word_span = get_word_span(sent_stripped, word_ind)
				new_sent = wreplacer.replace_word(newest_sent, word_span)
				if new_sent not in sent_hist:
					# print(f"\t{new_sent}")
					newest_sent = new_sent
					sent_hist.append(new_sent)
					has_changed = True
					break

		if not has_changed:
			break

	return sent_hist[-1]

def split_sentences(txt):
	sents = []
	in_punctuation = False
	sent_start_ind = 0
	for char_ind, char in enumerate(f"{txt} "):
		char_is_punct = char in "?!."
		if in_punctuation and not char_is_punct:
			## punctuation ends here
			sents.append(txt[sent_start_ind:char_ind].strip())
			sent_start_ind = char_ind + 1
		in_punctuation = char_is_punct

	return sents

def main(file_name):
	## read input text from file
	with open(file_name, "r", encoding="utf8") as f:
		txt = " ".join([line.strip(" \n") for line in f])

	sents = split_sentences(txt.lower())

	## initialize models
	excluded_chars = ".,!?\"'-"
	fb = FBReplacer(model_name="bert-base-uncased")
	word_replacer_fb = WordReplacer(fb, get_synonyms, excluded=excluded_chars)
	mlm = MLMReplacer(model_name="bert-base-uncased")
	word_replacer_mlm = WordReplacer(mlm, get_synonyms, excluded=excluded_chars)

	sents_mut = []
	for s in sents:
		# print(s)
		mut = mutate_sentence([word_replacer_mlm, word_replacer_fb], s)
		sents_mut.append(mut)

	print(" ".join(sents_mut))

if __name__ == '__main__':
	try:
		file_name = sys.argv[1]
	except:
		print("Error: file name needs to be provided")
	main(file_name)