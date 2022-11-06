import pandas as pd
from typing import List, Dict 
from time import sleep
import json
import os
import subprocess


##
#command = "./nfc-frog/nfc-frog full 2>&- >> emv.out"
#process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
#process.wait()
##
#print('empezamos')



df = pd.read_csv('Templates.csv')
parent_tags = set(df['Templates'])
df1 = pd.read_csv('Tags.csv')
all_tags = set(df1['Tag'])
# HEX VALUES 
with open('emv.out', 'r') as f:
    output = f.read().split(' ')

# hex to int 
def hex_to_num(value: str) -> int:
  return int(value, 16)

def is_compound_tag(index):
  return output[index] + output[index+1] in all_tags 
 
def parse_information(tag_name, index):
  n = index + hex_to_num(output[index+1]) + 1
  tag_index_shift = 2
  print(f"tag name {tag_name}:", output[index+tag_index_shift:n+1])
  return n

def recursiva(tag_index, n): # index starts in the tag position, length is in index+1
  
  level_dict = dict()
  
  while tag_index < n:
    if is_compound_tag(tag_index):
      tag_name = output[tag_index]+output[tag_index+1]
      tag_index += 1 
        
    else:
      tag_name = output[tag_index]
  
    if tag_name in parent_tags:
      child_dict, new_ind = recursiva(tag_index+2, tag_index+hex_to_num(output[tag_index+1])+1)
      level_dict[tag_name] = child_dict
      tag_index = new_ind
    
    elif tag_name in all_tags:
      end = tag_index + hex_to_num(output[tag_index+1]) + 1
      tag_index_shift = 2
      level_dict[tag_name] = output[tag_index+tag_index_shift:end+1]
      tag_index = end
      
    tag_index += 1

  return level_dict, n
  
def main():
  if output[0] in ['6F' ,'70']:
    end_dict = {output[0]: None}
    out, _ = recursiva(2, hex_to_num(output[1]))
    end_dict[output[0]] = out
    print(end_dict)
  else:
    raise ValueError('not recognized init tag')

main()
     


