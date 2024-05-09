import sys
import os
import re

"""
# AJMC tags
# tags = ['pers','loc', 'scope','work', 'object','date']
# HIPE tags
tags = ['pers', 'loc', 'org', 'prod', 'time']
# NewsEye tags
# tags = ['per','loc', 'org','humanprod']
"""


def select_gt_txt_file(dataset, lang):
    gt_txt_files = {
        "ajmc": f"AJMC/{lang}/HIPE-2022-v2.1-ajmc-test-{lang}.txt",
        "hipe": f"HIPE/{lang}/HIPE-2022-v2.1-hipe2020-test-{lang}.txt",
        "newseye_de": "Newseye/de/HIPE-2022-v2.1-newseye-test-de.txt",
        "newseye_fr": "Newseye/fr/NewsEye-GT-NER_EL_StD-v1-test-fr.txt"
    }

    if "newseye" in dataset:
        return gt_txt_files[f"{dataset}_{lang}"]
    return gt_txt_files[f"{dataset}"]


def select_tagset(dataset):
    tagset = {
        "ajmc": ['pers', 'loc', 'scope', 'work', 'object', 'date'],
        "hipe": ['pers', 'loc', 'org', 'prod', 'time'],
        "newseye": ['per', 'loc', 'org', 'humanprod']
    }
    return tagset[dataset]


def select_normalization_function(dataset):
    def normalise_ajmc(label):
        if re.search("loc", label, re.IGNORECASE):
            return 'loc'
        elif re.search("pers", label, re.IGNORECASE):
            return 'pers'
        elif re.search("scope", label, re.IGNORECASE):
            return 'scope'
        elif re.search("work", label, re.IGNORECASE):
            return 'work'
        elif re.search("obj", label, re.IGNORECASE):
            return 'object'
        elif re.search("date", label, re.IGNORECASE):
            return 'date'
        else:
            return label

    def normalise_newseye(label):
        if re.search("loc", label, re.IGNORECASE):
            return 'loc'
        elif re.search("pers", label, re.IGNORECASE):
            return 'per'
        elif re.search("org", label, re.IGNORECASE):
            return 'org'
        elif re.search("prod", label, re.IGNORECASE):
            return 'humanprod'
        else:
            return label

    def normalise_hipe(label):
        if re.search("loc", label, re.IGNORECASE):
            return 'loc'
        elif re.search("pers", label, re.IGNORECASE):
            return 'pers'
        elif re.search("org", label, re.IGNORECASE):
            return 'org'
        elif re.search("pred", label, re.IGNORECASE):
            return 'prod'
        elif re.search("time", label, re.IGNORECASE):
            return 'time'
        else:
            return label

    normalization_function = {
        "ajmc": normalise_ajmc,
        "hipe": normalise_hipe,
        "newseye": normalise_newseye
    }

    return normalization_function[dataset]


def main(argv):
    gt_path = sys.argv[1]
    log_path = sys.argv[2]
    output_path = log_path.replace("log", "iob")  # sys.argv[3]
    if os.path.isdir(output_path):
        print(f"{output_path} already there...")
    else:
        print(f"Creating {output_path}")
        os.makedirs(output_path)

    for filename in os.listdir(log_path):
        log_file = os.path.join(log_path, filename)
        if os.path.isfile(log_file) and filename.endswith('.log'):

            # AJMC && HIPE txt
            # gt_txt_file = os.path.join(gt_path, filename.split('_')[4].split('.tsv')[0])+'.txt'
            # NewsEye txt
            # gt_txt_file = os.path.join(gt_path, filename.split('_')[3].split('.tsv')[0])+'.txt'
            dataset, lang = os.path.split(log_path)[-1].lower().split("_")
            tmp = select_gt_txt_file(dataset, lang)
            gt_txt_file = os.path.join(gt_path, tmp)
            # iob outputs
            output_txt_file = os.path.join(output_path, filename.replace('.log', '.txt'))
            output_tsv_file = os.path.join(output_path, filename.replace('.log', '.tsv'))

            # Parse GT sentences
            with open(gt_txt_file, 'r') as gt_txt:
                content = gt_txt.read()
            gt_txt.close()

            # Load GT sentences
            gt_sentences = []
            gt_sentences = content.split("\n")

            # Read the log file and split by "####" symbol
            with open(log_file, 'r') as file:
                content = file.read()
            file.close()

            # Split content by "####"
            blocks = []
            blocks = content.split("########")

            # Initialize lists to store extracted information
            sentences = []

            # Define regular expression pattern
            pattern = re.compile(r'<SENTENCE>(.*?)</SENTENCE>', re.DOTALL)

            # Iterate over blocks and extract information
            index_sentence = 0
            file_txt_out = open(output_txt_file, "w")
            file_tsv_out = open(output_tsv_file, "w")
            for block in blocks:
                match = pattern.search(block)
                if match:
                    sentence = match.group(1).strip()
                    sentences.append(sentence)
                    file_txt_out.write(sentence + '\n')
                else:
                    if (gt_sentences[index_sentence]):
                        file_txt_out.write(gt_sentences[index_sentence] + '\n')
                        sentences.append(gt_sentences[index_sentence])
                index_sentence += 1
            file_txt_out.close()

            list_tags = []

            tags = select_tagset(dataset)
            normalise = select_normalization_function(dataset)

            index_sentence = 0
            for sent in sentences:
                words = sent.split()
                gt_words = gt_sentences[index_sentence].split()
                inside_tag = 0
                index_word = 0
                for w in gt_words:
                    if index_word >= len(words):
                        index_word -= 1
                    if len(words) == 0:
                        words = ["NOTHING"]
                        index_word = 0
                    # print(w+"\t"+str(index_word)+"\t"+words[0])
                    if re.search("<.*>.*</.*>", words[index_word]):
                        if w == words[index_word].split('>')[1].split('<')[0]:
                            # print('case 1 : '+w+'\t'+words[index_word])
                            tag = words[index_word].split('>')[0].split('<')[1].lower()
                            list_tags.append(tag)
                            tag = normalise(tag)
                            if tag in tags:
                                file_tsv_out.write(w + '\tB-' + tag + '\n')
                            else:
                                file_tsv_out.write(w + '\tO\n')
                            if words[index_word].split('>')[-1] != '':
                                index_word -= 1
                            index_word += 1
                        else:
                            file_tsv_out.write(w + '\tO\n')
                    elif re.search(".*</.*>", words[index_word]):
                        # print('case 3 : '+words[index_word])
                        if w == words[index_word].split('<')[0]:
                            # print('case 3 : '+w+'\t'+words[index_word])
                            tag = words[index_word].split('>')[0].split('</')[1].lower()
                            list_tags.append(tag)
                            tag = normalise(tag)
                            if tag in tags:
                                file_tsv_out.write(w + '\tI-' + tag + '\n')
                            else:
                                file_tsv_out.write(w + '\tO\n')
                            if words[index_word].split('>')[-1] != '':
                                index_word -= 1
                            index_word += 1
                        else:
                            file_tsv_out.write(w + '\tO\n')
                        inside_tag = 0
                    elif re.search("<.*>.*", words[index_word]):
                        if w == words[index_word].split('>')[1]:
                            # print('case 2 : '+w+'\t'+words[index_word])
                            # print('case 2 : '+words[index_word])
                            inside_tag = 1
                            tag = words[index_word].split('>')[0].split('<')[1].lower()
                            list_tags.append(tag)
                            tag = normalise(tag)
                            if tag in tags:
                                # print(w+'\tB-'+tag)
                                file_tsv_out.write(w + '\tB-' + tag + '\n')
                            else:
                                #                                print(tag)
                                file_tsv_out.write(w + '\tO\n')
                            index_word += 1
                        elif w in words[index_word].split('>')[1]:
                            # print('case 2 : '+w+'\t'+words[index_word])
                            tag = words[index_word].split('>')[0].split('<')[1].lower()
                            list_tags.append(tag)
                            tag = normalise(tag)
                            if tag in tags:
                                if inside_tag:
                                    file_tsv_out.write(w + '\tI-' + tag + '\n')
                                    index_word += 1
                                else:
                                    file_tsv_out.write(w + '\tB-' + tag + '\n')
                            else:
                                file_tsv_out.write(w + '\tO\n')
                            inside_tag = 1
                        else:
                            file_tsv_out.write(words[index_word] + '\tO\n')
                            index_word += 1
                    else:
                        # print('case 4 : '+words[index_word])
                        if w == words[index_word]:
                            if inside_tag:
                                if tag in tags:
                                    file_tsv_out.write(w + '\tI-' + tag + '\n')
                                else:
                                    file_tsv_out.write(w + '\tO\n')
                            else:
                                file_tsv_out.write(w + '\tO\n')
                            index_word += 1
                        else:
                            if inside_tag:
                                if tag in tags:
                                    file_tsv_out.write(w + '\tI-' + tag + '\n')
                                else:
                                    file_tsv_out.write(w + '\tO\n')
                                index_word += 1
                            else:
                                file_tsv_out.write(w + '\tO\n')
                file_tsv_out.write('\n')
                index_sentence += 1
            file_tsv_out.close()
    print(set(list_tags))


if __name__ == "__main__":
    main(sys.argv)