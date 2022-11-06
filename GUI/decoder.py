from web_scrapping import get_data, get_countries
import pandas as pd
import json


import os
import subprocess


command = "../nfc-frog/nfc-frog full 2>&- >> emv.out"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
process.wait()

print('Starting...')

df = pd.read_csv('Templates.csv')
parent_tags = set(df['Templates'])
df1 = pd.read_csv('Tags.csv')
all_tags = set(df1['Tag'])

# CardHolder Name, Languaje pref, application level
ascii_tags = ["5F20", "5F2D", "50"]

# Expiration date,
decimal_tags = []

countries = get_countries()
# HEX VALUES

with open('emv.out', 'r') as f:
    output = f.read().replace('\n', '').split(' ')

# hex to int


def hex_to_num(value: str) -> int:
    return int(value, 16)


def hex_to_ascii(value: str) -> str:
    bytes_object = bytes.fromhex(value)
    ascii_string = bytes_object.decode("ASCII")
    return ascii_string


def is_compound_tag(index):
    return output[index] + output[index+1] in all_tags


def recursiva(tag_index, n):  # index starts in the tag position, length is in index+1

    level_dict = dict()

    while tag_index < n:
        if is_compound_tag(tag_index):
            tag_name = output[tag_index]+output[tag_index+1]
            tag_index += 1

        else:
            tag_name = output[tag_index]

        if tag_name in parent_tags:
            child_dict, new_ind = recursiva(
                tag_index+2, tag_index+hex_to_num(output[tag_index+1])+1)
            level_dict[tag_name] = child_dict
            tag_index = new_ind

        elif tag_name in all_tags:
            end = tag_index + hex_to_num(output[tag_index+1]) + 1
            tag_index_shift = 2
            msg = "".join(output[tag_index+tag_index_shift:end+1])
            if tag_name in ascii_tags:
                msg = hex_to_ascii(msg)
            elif tag_name in decimal_tags:
                msg = hex_to_num(msg)
            elif tag_name == "5F28":  # Country
                msg = countries[msg]
            level_dict[tag_name] = str(msg)
            tag_index = end

        tag_index += 1

    return level_dict, n


def main():
    i = 0
    _6F_ = []
    _70_ = []
    counter = 0
    while i < len(output):
        if output[i] in ['6F', '70']:
            counter = 0
            current_dict = {output[i]: None}
            length = hex_to_num(output[i + 1])
            out, _ = recursiva(i + 2, i + length)
            current_dict[output[i]] = out
            if output[i] == '6F':
                _6F_.append(current_dict)
            else:
                _70_.append(current_dict)

            i += length
        else:
            if(output[i] == "00"):
                counter += 1
                if counter == 3:
                    break
            i += 1

    rows = {"6F": _6F_, "70": _70_}
    end_list = {"rows": rows, "value": get_data()}

    return json.dumps(end_list)


json_file = main()

with open('./scripts/json_data.json', 'w') as outfile:
    outfile.write(json_file)
