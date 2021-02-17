import json
import os
from pathlib import Path


def clean_dataset():
    for i in range(1, 10000):
        number = str(i)
        number = number.zfill(7)
        path_in = Path(__file__).resolve().parent.parent / 'Dataset'
        path_out = Path(__file__).resolve().parent.parent / 'Cleaned Dataset'

        if not os.path.exists(path_in):
            exit(1)
        if not os.path.exists(path_out):
            os.makedirs(path_out)

        path_in = path_in / 'news_{index}.json'.format(index=number)
        path_out = path_out / 'doc{index}.txt'.format(index=number)

        with open(path_in, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Print the data onto new file with some clean names
        with open(path_out, 'w+', encoding='utf-8') as file:
            text = data['title'] + data['text']
            file.write(text)


clean_dataset()