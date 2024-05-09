import json
import requests
import os
import sys
import re
import copy
import logging
import pickle
from time import sleep, strftime, localtime
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer


from utils import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def parse_arguments():

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    #dataset params
    parser.add_argument("-i", "--input_file",
                        dest="input_file",
                        type=str,
                        help="""tsv input file""")

    parser.add_argument("-p", "--system_prompt",
                        dest="system_prompt",
                        type=str,
                        choices=SYSTEM_PROMPTS.keys(),
                        help="""System prompt to use""")

    #models
    parser.add_argument("-m", "--model",
                        dest="model",
                        default="Llama-2-70b-chat-hf",
                        type=str,
                        choices=API_MODELS.keys(),
                        help="""Model to call""")

    parser.add_argument("-s", "--save_freq",
                        dest="save_freq",
                        type=int,
                        default=10,
                        help="""Save each # phrases.""")

    return parser.parse_args()

def load_and_format_file(input_file):

    with open(input_file, "r") as ap:
        lines = ap.readlines()

    phrase = list()
    ref_index = 0
    phrases = list()
    for line in lines:
        line = line.split("\t")
        if len(line) == 2 and len(line[0]) != 0:
            word = line[0]
            tag = line[1].replace("\n", "")
            end_index = ref_index + len(word)
            phrase.append({
                "word": word,
                "tag": tag,
                "start_index": ref_index,
                "end_index": end_index
            })
            ref_index = end_index + 1
        elif len(phrase) != 0:
            phrases.append({"phrase": phrase})
            ref_index = 0
            phrase = list()

    if len(phrase) != 0:
        phrases.append({"phrase": phrase})

    return phrases


def get_text(phrase):

    words = list()
    for word in phrase:
        words.append(word["word"])

    return " ".join(words)

def construct_conversation(tokenizer, format_model, system_prompt, payload):

    conversation = []

    if system_prompt["examples"][0][0] != "": #with role
        examples = copy.deepcopy(system_prompt["examples"])

        if format_model[0] == "system":
            conversation.append({"role": format_model[0], "content": system_prompt["prompt"]})
        else:
            examples[0][0] = f"{system_prompt['prompt']}\n{system_prompt['examples'][0][0]}"
        for interaction in examples:
            conversation.append({"role": format_model[-2], "content": interaction[0]})
            conversation.append({"role": format_model[-1], "content": interaction[1]})

        conversation.append({"role": format_model[-2], "content": payload})
    else: #without role
        if format_model[0] == "system":
            conversation.append({"role": format_model[0], "content": system_prompt["prompt"]})
            conversation.append({"role": format_model[-2], "content": payload})
        else:
            content = f"{system_prompt['prompt']}\n{payload}"
            conversation.append({"role": format_model[-2], "content": content})

    #logger.info(f"TOKENS: {len(tokenizer.apply_chat_template(conversation, tokenize=True))}")
    return tokenizer.apply_chat_template(conversation, tokenize=False)


def query(api_url, format_model, system_prompt, tokenizer, payload="Say hi.", estimated_length=1024):

    conversation = construct_conversation(tokenizer=tokenizer, format_model=format_model, system_prompt=system_prompt, payload=payload)
    json_body = {
        #"inputs": f"<s>[INST] <<SYS>>\n{system_prompt}<</SYS>>\n\n{payload} [/INST]",
        #"inputs": f"<s>[INST] <<SYS>>\n{system_prompt['prompt']}<</SYS>>\n\n{system_prompt['examples'][0][0]} [/INST] {system_prompt['examples'][0][1]} </s><s>[INST] {system_prompt['examples'][1][0]} [/INST] {system_prompt['examples'][1][1]} </s><s>[INST] {payload} [/INST]",
        "inputs": conversation,
        "parameters": {"max_new_tokens": estimated_length,#"512, #1024
                       #"top_p": 0.9,
                       "temperature": 0.001, #0.1
                       #"top_k": 10,
                       "num_return_sequences": 1, #3
                       "return_full_text": True,
                       "do_sample":False}
    }
    data = json.dumps(json_body)
    while True:
        try:
            response = requests.request("POST", api_url, headers=HEADERS, data=data)
            #print(response.content.decode("utf-8"))
            if response.status_code == 200:
                try:
                    return json.loads(response.content.decode("utf-8"))
                except:
                    return response
            #logger.info("> Model overloaded, retrying 1s.")

            elif (response.status_code == 500) and ("Internal Server Error" in response.content.decode("utf-8")) or (response.status_code == 503) and ("Service Unavailable" in response.content.decode("utf-8")):
                logger.info(response.content.decode("utf-8"))
                return [{'generated_text':"[/INST]"}]

            elif (response.status_code == 422) and ("Input validation error" in response.content.decode("utf-8")):
                json_body["parameters"]["max_new_tokens"] = json_body["parameters"]["max_new_tokens"] - 100
                data = json.dumps(json_body)
                # scape for Mixtral where input
                if json_body["parameters"]["max_new_tokens"] <= 0 or "`inputs` must have less than" in response.content.decode("utf-8"):
                    logger.info(response.content.decode("utf-8"))
                    return [{'generated_text': "[/INST]"}]

            logger.info(response.content.decode("utf-8"))
            sleep(0.25)
        except:
            logger.info("> Problem fetching model, retrying 1s.")
            sleep(1)

def extract_response_text(data): #Llama3 format
    # Regex to match text between "< | eot_id | > assistant\n\n" and "assistant\n\n"
    pattern = re.compile(r"<\|eot_id\|>assistant\n\n(.*?)assistant\n\n", re.DOTALL)

    # Search for the pattern in the provided data
    match = pattern.search(data)
    if match:
        return match.group(1)  # Return the captured group which is the text between the markers
    else:
        return None

def main():
    args = parse_arguments()

    if not os.path.exists('./log'):
        os.makedirs('./log', mode=0o777)
    log_file = '{}-{}-{}-{}.log'.format(args.model, args.input_file.replace("/", "_").replace(" ", "_"), args.system_prompt, strftime("%Y-%m-%d_%H:%M:%S", localtime()))
    logger.addHandler(logging.FileHandler("%s/%s" % ('./log', log_file)))

    phrases = load_and_format_file(args.input_file)
    tokenizer = AutoTokenizer.from_pretrained(API_MODELS[args.model].split("/models/")[-1], token=API_TOKEN)

    out_file = log_file.replace(".log", ".out")
    counter = 1
    #a=1
    for phrase in tqdm(phrases):
        text = "INPUT: <SENTENCE>"+get_text(phrase["phrase"])+"</SENTENCE>"
        factor = 6
        valid_output = False
        pivot_text = ""
        while not valid_output:
            estimated_length = len(text.split(" ")) * factor
            logger.info(f"Estimated length: {estimated_length}")
            #if a == 10:
            #    print("")
            #logger.info(f"-- > {a}")
            response = query(API_MODELS[args.model], FORMAT_MODELS[args.model] ,SYSTEM_PROMPTS[args.system_prompt], tokenizer=tokenizer, payload=text, estimated_length=estimated_length)
            #print(response)
            #response_text = response[0]['generated_text'].split('[/INST]')[1]
            if args.model == "Meta-Llama-3-70B-Instruct":
                response_text = extract_response_text(response[0]['generated_text'])
                if not response_text:
                    response_text = response[0]['generated_text'].split("<|eot_id|>assistant\n\n")[-1]
                if "..." not in text and "..." in response_text:
                    response_text = response_text.replace("...", " . . .")
            else:
                response[0]['generated_text'] = response[0]['generated_text'].replace("<|assistant|>", "[/INST]")
                response_text = response[0]['generated_text'].split('[/INST]')[-1]
            #input()
            if len(response_text.split("</SENTENCE>")) > 1 or pivot_text == response_text or len(response_text.split()) >= len(get_text(phrase['phrase']).split())*2:
                valid_output = True
            elif " " not in get_text(phrase['phrase']) and len(response_text) >= len(get_text(phrase['phrase']))*5: #when only one word in phrase and stays in loop
                valid_output = True
            elif get_text(phrase['phrase']) == "GENÈVE .":
                valid_output = True
            else:
                factor += 1
                pivot_text = response_text
        #a=a+1
        phrase["response_text"] = response_text
        if counter % args.save_freq == 0:
            with open("%s/%s" % ('./log', out_file), "wb") as ap:
                pickle.dump(phrases, ap)
        counter += 1
        logger.info(response_text)
        logger.info(f"FINAL Estimated length: {estimated_length}")
        logger.info("########")
        sleep(0.1)

    with open("%s/%s" % ('./log', out_file), "wb") as ap:
        pickle.dump(phrases, ap)

    logger.info(f"I've process {len(phrases)} phrases!")


if __name__ == '__main__':
    """
    Starts the whole app from the command line
    """

    main()



