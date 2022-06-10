import argparse
import json
from collections import defaultdict

import spacy
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--prediction",
        default="extract.jsonl",
        type=str,
        help="file that save the prediction dialogs",
    )

    parser.add_argument(
        "--output",
        default="dataset.jsonl",
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

    data={'source':[],'target':[]}
    for d in tqdm(dialog):
        flag = 0
        for key, (one, multi) in keywords.items():
            for idx in range(2, len(d["dialog"]), 2):
                dialog = d["dialog"][idx]
                flag = 0
                for o in one:
                    if dialog.find(o) != -1:
                        print('one', dialog.find(o))
                        if idx <= 2:
                            data['source'].append(d["dialog"][0])
                            data['target'].append(d["dialog"][1])
                            flag = 1
                            break
                        else:
                            temp = ''
                            for i in range(idx-4,idx-1):
                                print(i)
                                temp = temp + d["dialog"][i] + '\n'
                            data['source'].append(temp)
                            data['target'].append(d["dialog"][idx-1])    
                            flag = 1
                            break     
                if flag == 0:                  
                    for m in multi:
                        if dialog.find(m) != -1:
                            print(idx)
                            print('multi', dialog.find(m))
                            if idx <= 2:
                                data['source'].append(d["dialog"][0])
                                data['target'].append(d["dialog"][1])
                                break
                            else:
                                temp = ''
                                for i in range(idx-4,idx-1):
                                    print(i)
                                    temp = temp + d["dialog"][i] + '\n'
                                data['source'].append(temp)
                                data['target'].append(d["dialog"][idx-1])
                                break
    with open(args.output, "w") as f:
        for source, target in zip(data['source'],data['target']):
            f.write(json.dumps({'source':source,'target':target}) + "\n")
            