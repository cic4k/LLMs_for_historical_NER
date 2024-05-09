import os
import pandas as pd
import json
import subprocess
from tqdm import tqdm

IOB_FOLDER = '../iob'
REF_FOLDER = './Ref'
TASK = 'nerc_coarse'
HIPE_EDITION = 'hipe-2022'
EVAL_SCRIPT = "./HIPE_eval/clef_evaluation.py"
HEADERS = ["language_model", "guidelines_type", "role_type", "dataset", "lang",
           "strict_P_micro", "strict_R_micro", "strict_F1_micro",
           "fuzzy_P_micro", "fuzzy_R_micro", "fuzzy_F1_micro"]


def find_pred_tsv_files(path):
    # Create an empty list to store the file paths
    file_list = []

    # Iterate through the directory tree starting from the given path
    for root, dirs, files in os.walk(path):
        # Iterate through the files in the current directory
        for file in files:
            # Check if the file name ends with "_pred.tsv"
            if file.endswith("_pred.tsv"):
                # Construct the full file path
                full_path = os.path.join(root, file)
                # Add the full file path to the list
                file_list.append(full_path)

    # Return the list of file paths
    return file_list

def select_gt_txt_file(dataset, lang):
    gt_txt_files = {
        "ajmc": f"{REF_FOLDER}/AJMC_{lang}/HIPE-2022-v2.1-ajmc-test-{lang}.tsv",
        "hipe": f"{REF_FOLDER}/HIPE_{lang}/HIPE-2022-v2.1-hipe2020-test-{lang}.tsv",
        "newseye_de": f"{REF_FOLDER}/NewsEye_de/NewsEye-GT-NER_EL_StD-v2-test-de.tsv",
        "newseye_fr": f"{REF_FOLDER}/NewsEye_fr/NewsEye-GT-NER_EL_StD-v1-test-fr.tsv"
    }

    if "newseye" in dataset:
        return gt_txt_files[f"{dataset}_{lang}"]
    return gt_txt_files[f"{dataset}"]


def run_hipe_eval(*args):
    # Create a list of arguments
    command = ['python', EVAL_SCRIPT]
    # Add the parameters to the command list
    command.extend(args)

    # Run the Python script using subprocess.run
    result = subprocess.run(command, capture_output=True, text=True)

    # Return the result
    return result

def extract_scores(scores_file_name):

    with open(scores_file_name, 'r') as file:
        # Load the JSON data from the file
        data = json.load(file)

    strict = data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"]["ALL"]["strict"]
    fuzzy = data["NE-COARSE-LIT"]["TIME-ALL"]["LED-ALL"]["ALL"]["ent_type"]
    return strict, fuzzy

def main():

    pred_files = find_pred_tsv_files(IOB_FOLDER)
    evaluations = []

    for pred_file in tqdm(pred_files):
        out_dir = os.path.split(pred_file)[0]
        _ = pred_file.split("/")
        file_name = _[-1]
        dataset, lang = _[-2].split('_')
        role_type = _[-3]
        guidelines_type = _[-4]
        language_model = _[-5]

        args_hipe_eval = f"--skip-check --ref {select_gt_txt_file(dataset.lower(), lang)} --pred {pred_file} --task {TASK} --outdir {out_dir} --hipe_edition {HIPE_EDITION} --log {os.path.join(out_dir, 'log.log')}"
        args_list = args_hipe_eval.split(" ")
        status = run_hipe_eval(*args_list)
        if status.returncode == 0:
            eval_file_name = [_ for _ in os.listdir(out_dir) if _.endswith("json")][0]
            strict, fuzzy = extract_scores(os.path.join(out_dir, eval_file_name))
            evaluations.append([language_model, guidelines_type, role_type, dataset, lang,
                                strict["P_micro"], strict["R_micro"], strict["F1_micro"],
                                fuzzy["P_micro"], fuzzy["R_micro"], fuzzy["F1_micro"]])
        else:
            print(f"Problem with {pred_file}")
    df = pd.DataFrame(evaluations, columns=HEADERS)
    print(df)
    df_sorted = df.sort_values(by=["language_model", "guidelines_type", "role_type", "dataset", "lang"])
    df_sorted.to_csv("all_results.tsv", sep='\t', index=False, float_format='%.4f')
if __name__ == "__main__":
    main()

