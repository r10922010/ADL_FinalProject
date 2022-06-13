pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
wget -O final_best.zip 'https://www.dropbox.com/s/feddnok1154jyjp/final_best.zip?dl=1'
unzip final_best.zip
python simulator.py --split test --model_name_or_path final_best/ --num_chats 980 --disable_output_dialog