# ADL 2022 Final Project Scripts
## Submission

Our `run.sh` will generate `output.jsonl`,
which is the output of `simulator.py` on the test set.

Before executing python simulator.py, we first set up the environment which followed TA's sample README.md. Then, downloading our model from dropbox.

Below is the content of our `run.sh`:

```
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
wget -O final_best.zip 'https://www.dropbox.com/s/feddnok1154jyjp/final_best.zip?dl=1'
unzip final_best.zip
python simulator.py --split test --model_name_or_path final_best/ --num_chats 980 --disable_output_dialog
```

`output.jsonl` contains 980 dialogues of (at most) 5 turns.


## Usage
### Install requirements
```
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
```

## Dataset

Our data collect from the training set output of the default simulator.py and Otters+Anlg dataset, which is used in warm-up.
Otters : https://github.com/karinseve/OTTers
Anlg : https://drive.google.com/file/d/15ckbKsyq5sMU-RJh0n-mB9NgyW1WhTsF/view
We consider the sentence before the keyword sentence as our target, and the 3 sentences before the target sentence as our training source. Then, using the dataset to finetune the default "facebook/blenderbot-400M-distill" model.

Our model can acheive 0.762 hit rate.


### Calculate metric (hit rate)
**WARNING: PLEASE DO NOT MODIFY `hit.py` AND `keywords.json`.**
This script will calculate keyword hit rate for you by:
```
python hit.py --prediction [/path/to/your/output/prediction/from/simulator]
```
