# Leveraging Open Large Language Models for Historical Named Entity Recognition
---
This repository contains the code and data of the article *Leveraging Open Large Language Models for Historical Named Entity Recognition*.


## Predictions

All predictions are stored in `log/`. `.log` files are text files containing all the predictions generated by the Instruct models. The `.out` files contain the same predictions but in a structured dictionary, which helps during the post-processing and alignment step.

## Evaluation


The ```evaluation``` folder contains all the scripts needed to re-run evaluations. 


---

## Running the workflow and Evaluating


### Extract Entities

To run the workflow, install the libraries specified in `requirements.txt`.

A HUGGINGFACE User Access Token is needed to query HuggingFace's API; you can create it here: https://huggingface.co/settings/tokens. Depending on the model, it may be necessary to subscribe to the Plus program.

The User Access Token has to be placed in `utils.py` `API_TOKEN = "[HUGGINGFACE User Access Token]"` 

Run the `extract_entities.sh` script wrapper to obtain the named entities of all the corpora using all the modes. Attention, this takes a while.

All the predictions are stored in  `log/` .


### Evaluating

The evaluation is a 3 step process. Be sure to be under `evaluation/`, then run:

1. `parse_logs.sh`
2. `preprocess_evaluation.sh`
3. `wrapper_HIPE_eval.py`

This generates the intermediate files aligned to the gold standards and the `.json` files containing the scores of each file `.log` file. In addition, the `all_results.tsv` file is created to facilitate results analysis.  