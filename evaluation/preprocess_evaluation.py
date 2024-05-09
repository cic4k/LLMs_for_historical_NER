import sys
import os
import re
import pandas as pd
EMPTY_TAG = "O\tO\tO\tO\tO\tO\t_\t_\t_"
EMPTY_TAG_newseye_fr = "O\tO\tO\tnull\tnull\tNoMatch"
def select_gt_txt_file(dataset, lang):
    gt_txt_files = {
        "ajmc": f"./Ref/AJMC_{lang}/HIPE-2022-v2.1-ajmc-test-{lang}.tsv",
        "hipe": f"./Ref/HIPE_{lang}/HIPE-2022-v2.1-hipe2020-test-{lang}.tsv",
        "newseye_de": "./Ref/NewsEye_de/NewsEye-GT-NER_EL_StD-v2-test-de.tsv",
        "newseye_fr": "./Ref/NewsEye_fr/NewsEye-GT-NER_EL_StD-v1-test-fr.tsv"
    }

    if "newseye" in dataset:
        return gt_txt_files[f"{dataset}_{lang}"]
    return gt_txt_files[f"{dataset}"]


def main(argv):

    pred_path = sys.argv[1]



    dataset, lang = os.path.split(pred_path)[-1].lower().split("_")
    gt_file = select_gt_txt_file(dataset, lang)
    for _ in os.listdir(pred_path):
        if _.endswith("_pred.tsv"):
            os.remove(os.path.join(pred_path, _))
    output_file = [_ for _ in os.listdir(pred_path) if _.endswith(".tsv")][-1]

    print(f"Preprocessing {output_file}...")
    pred_file = output_file.replace(".tsv", "_pred.tsv")
    file_tsv_pred = open(os.path.join(pred_path, pred_file), "w")

    with open(gt_file, 'r') as gt:
        content_gt = gt.read() 
    gt.close()
            
    # Load GT sentences
    gt_sentences = []
    gt_sentences = content_gt.split("\n")
    
    with open(os.path.join(pred_path, output_file), 'r') as out:
        content_out = out.read() 
    out.close()
            
    # Load GT sentences
    out_sentences = []
    out_sentences = content_out.split("\n")
    out_sentences = list(filter(len, out_sentences))
    index_sentence = 0

    #print (out_sentences)

    for sentence in gt_sentences:
        #print(sentence)
        #print("\n")
        #if "1942" in sentence:
        #    print("eee")
        if sentence == '' or sentence.startswith('# ') or sentence.startswith('TOKEN'):
            file_tsv_pred.write(sentence+"\n")
        elif sentence.split('\t')[0] == out_sentences[index_sentence].split('\t')[0]:
            #print(sentence.split('\t')[0]+'\t'+out_sentences[index_sentence].split('\t')[0])

            file_tsv_pred.write(out_sentences[index_sentence].split('\t')[0] + '\t' + out_sentences[index_sentence].split('\t')[1] + '\t' +"\t".join(sentence.split('\t')[2:])+'\n')
            #file_tsv_pred.write(out_sentences[index_sentence].split('\t')[0]+'\t'+out_sentences[index_sentence].split('\t')[1]+'\tO\t'+sentence.split('\t')[3]+'\t'+sentence.split('\t')[4]+'\t'+sentence.split('\t')[5]+'\t'+sentence.split('\t')[6]+'\t'+sentence.split('\t')[7]+'\t'+sentence.split('\t')[8]+'\t'+sentence.split('\t')[9]+'\n')
            #file_tsv_pred.write(out_sentences[index_sentence].split('\t')[0]+'\t'+out_sentences[index_sentence].split('\t')[1]+'\tO\t'+sentence.split('\t')[3]+'\t'+sentence.split('\t')[4]+'\t'+sentence.split('\t')[5]+'\n')
            index_sentence+=1
        else:
            print(sentence.split('\t')[0]+" XXX "+out_sentences[index_sentence].split('\t')[0])
            #file_tsv_pred.write(sentence+'\n')
            word = sentence.split('\t')[0]
            if f"{dataset}_{lang}" == "newseye_fr":
                file_tsv_pred.write(f"{word}\t{EMPTY_TAG_newseye_fr}\n")
            else:
                file_tsv_pred.write(f"{word}\t{EMPTY_TAG}\n")
            index_sentence+=1
    file_tsv_pred.close()
    print("------\n")
if __name__ == "__main__":
   main(sys.argv)