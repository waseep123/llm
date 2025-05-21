import re
import json
import pandas as pd

def clean_text(text):
	text = str(text).strip()
	text = re.sub(r"\s+", " ", text)
	return text

def json_parser(path):
	with open(path, 'rb') as f:
		data = json.load(f)

	pairs = {}
	data = data['categories']
	for sub_data in data:
		category = sub_data['category']
		for sub_sub_data in sub_data['questions']:
			q = f"({category}) " + sub_sub_data['question']
			a = sub_sub_data['answer']
			q = clean_text(q)
			a = clean_text(a)
			pairs[q] = a

	docs = []
	for q, a in pairs.items():
		doc = f"Question: {q}\nAnswer: {a}"
		docs.append(doc)

	return docs

def excel_parser(path):
	xls = pd.ExcelFile(path)
	qa_pairs = []

	for sheet_name in xls.sheet_names:
		df = xls.parse(sheet_name=sheet_name, header=None, dtype=str).fillna("")
		lines = df.values.flatten().tolist()
		current_q = None
		current_a = []
		for line in lines:
			line = clean_text(line)
			if line.endswith('?'):
				if current_q and current_a:
					answer = " ".join(current_a).strip()
					qa_pairs.append((current_q, answer))
				current_q = f"({sheet_name}) " + line
				current_a = []
			elif line:
				current_a.append(line)

		if current_q and current_a:
			qa_pairs.append((current_q, " ".join(current_a).strip()))

	docs = []
	for q, a in qa_pairs:
		doc = f"Question: {q}\nAnswer: {a}"
		docs.append(doc)

	return docs

if __name__ == "__main__":
	excel_docs = excel_parser("data/NUST Bank-Product-Knowledge.xlsx")
	json_docs = json_parser("data/funds_transfer_app_features_faq (1).json")

	docs = excel_docs + json_docs

	with open("data/processed.json", 'w') as f:
		json.dump(docs, f)

	print(docs)
