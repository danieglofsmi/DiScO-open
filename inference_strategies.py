import json
import re

def read_jsonl(jsonl_file):
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def read_json(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

template_prompt = """<｜User｜>Try to solve the following question step by step. If the final answer is obtained, use \\boxed{{}} to represent it.
### Question:{question}
<｜Assistant｜><think>\n{response}"""

def make_messages(question,response):
    messages = [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': template_prompt.format(question=question,response=response)}
            ]
    return messages


def repetition_elimination(input_str):
    # Split the string into words by spaces
    input_str = input_str.replace("\\thought", "")

    words = input_str.split()
    # Group every 15 words and add them to the content list
    content_list = []
    for i in range(0, len(words), 15):
        content_list.append(" ".join(words[i:i + 15]))

    # Check for duplicate content
    seen = set()
    for i, content in enumerate(content_list):
        if content in seen:
            # If duplicate found, truncate before the first occurrence of the 15-word group
            return " ".join(words[:(i - 1) * 15])
        seen.add(content)

    # If no duplicates, return the string truncated from 20% of its length
    split_pos = int(len(input_str) * 0.2)

    # Find the end of the next complete sentence
    match = re.search(r'[.!?]\s*', input_str[split_pos:])
    if match:
        boundary = split_pos + match.end()
        return input_str[boundary:].lstrip()
    else:
        return input_str[split_pos:].lstrip()


def truncation(input_str):
    input_str = input_str.replace("\\thought","")

    split_pos = int(len(input_str) * 0.2)

    # Find the end of the next complete sentence
    match = re.search(r'[.!?]\s*', input_str[split_pos:])
    if match:
        boundary = split_pos + match.end()
        return input_str[boundary:].lstrip()
    else:
        return input_str[split_pos:].lstrip()


def process_string(response,label,strategy):
  if strategy == "elimination":
    processed_response = repetition_elimination(response)
  elif strategy == "truncation":
    processed_response = truncation(response)
    
  return processed_response
