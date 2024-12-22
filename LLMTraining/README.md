# CS613-NLP Team-1 Telugu

## Team Members

1. **Bhavik Patel (22110047)** : Trained the LLama model, tokenized the dataset, defined the hyperparameters of the trainer like login and evaluation steps.
2. **Guntas Singh Saran (22110089)** : Trained the LLama model, tokenized the dataset, defined the hyperparameters of the trainer like login and evaluation steps.
3. **Hitesh Kumar (22110098)** : Trained the tokenizer on different sets of datasets.
4. **Ruchit Jagodara (22110102)** : Trained the tokenizer on different sets of datasets.
5. **Jinil Patel (22110184)** : Helped in tokenizing and generation of prompts and helped in training the LLama model.

## Task - 1

> **_NOTE:_** Here, text length means MBs of data.

<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/Tokenizers.png" style="width: 100%">
</div>

Code for training the tokenizers can be found in `CS613-NLP-Telugu-Team1/LLMTraining/Train_Tokenizers.ipynb`.

## Task - 2

### Pre-Trained Model on Telugu Dataset
[Model Files](https://iitgnacin-my.sharepoint.com/:f:/g/personal/22110089_iitgn_ac_in/EsPZ6u3kv-FKmkg7_eyV_pAB6TTc7vfVZv1HPKt6Abx-pA?e=kcfVjl)


### Tokenizing our dataset with SentencePieceBPEToekenizer.

<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/first_image.png" style="width: 60%">
</div>

### Model Architecture with 46M parameters

<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/second_image.png" style="width: 60%">
</div>


### Model Perplexity with Epochs
<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/perplexity_vs_epoch.png" style="width: 100%">
</div>

The logs can be found in the [WANDB Session](https://wandb.ai/guntas-13-indian-institute-of-technology-gandhinagar/huggingface/reports/Telugu-LLM-Training--VmlldzoxMDE5NTczNA?accessToken=4se1t0m6yinn37cpeduyz08vbiwi96f6hpjc7du9jqq7vfknnl7mozwymbjoojss&panelId=s7xrjynnm).

### Head and Tail of the Perplexity Matrix

<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/third_image.png" style="width: 40%; float: left;">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/fourth_image.png" style="width: 40%">
</div>

### 10 Prompts and their Response

<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/seventh_image.png" style="width: 100%">
</div>

<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/fifth_image.png" style="width: 100%">
</div>

<div align = "center">
    <img src = "https://github.com/guntas-13/CS613-NLP/blob/main/LLMTraining/sixth_image.png" style="width: 100%">
</div>





