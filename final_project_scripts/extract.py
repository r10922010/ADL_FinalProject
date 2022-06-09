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

    cnt = 0
    for d in tqdm(dialog):
        flag = 0
        for index in range(2, len(d["dialog"]), 2):
            lemma_utterance = [token.lemma_ for token in nlp(d["dialog"][index])]
            service_hits = defaultdict(int)
            for key, (one, multi) in keywords.items():
                intersection = set(one) & set(lemma_utterance)
                # check whether the word, the length is bigger than 2, is in the utterance
                for m in multi:
                    unsplit_utterance = " ".join(lemma_utterance)
                    if m in unsplit_utterance:
                        intersection.add(m)
                service_hits[key] += len(intersection)
            isService = sum(service_hits.values()) != 0
            if isService:
                with open(args.output, "a") as f:
                    f.write(json.dumps(d) + "\n")
                break