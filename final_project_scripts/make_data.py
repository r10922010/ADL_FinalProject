import argparse
import json
from collections import defaultdict

import spacy
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--prediction",
        default="output.jsonl",
        type=str,
        help="file that save the prediction dialogs",
    )

    parser.add_argument(
        "--output",
        default="extract.jsonl",
        type=str,
        help="file to save the extracted dialogs",
    )

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()

    with open("keywords.json") as f:
        keywords = json.load(f)

    with open(args.prediction, "r") as f:
        dialog = [json.loads(line) for line in f]

    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    for key, val in keywords.items():
        # separate words by its length (one, others)
        one_lemma = []
        multi_lemma = []
        for word in val:
            split = [token.lemma_ for token in nlp(word)]
            if len(split) >= 2:
                multi_lemma.append(" ".join(split))
            else:
                one_lemma.append(split[0])
            keywords[key] = [one_lemma, multi_lemma]
    print(keywords)

    source = []
    target = []
    for d in tqdm(dialog):
        flag = 0
        for key, (one, multi) in keywords.items():
            for idx in range(2, len(d["dialog"]), 2):
                dialog = d["dialog"][idx]
                for o in one:
                    if dialog.find(o) != -1:
                        print('one', dialog.find(o))
                        if idx <= 2:
                            for i in range(idx):
                                print(i)
                                source.append(d["dialog"][i])
                        else:
                            for i in range(idx-3,idx):
                                print(i)
                                source.append(d["dialog"][i])

                            
                for m in multi:
                    if dialog.find(m) != -1:
                        print(idx)
                        print('multi', dialog.find(m))
            