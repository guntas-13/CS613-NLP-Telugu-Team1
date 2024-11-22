# CS613-NLP Team-1 Telugu Assignment 3

## Team Members

1. **Bhavik Patel (22110047)** : Fine-tuned the model on SST-2 dataset and evaluated the model.
2. **Guntas Singh Saran (22110089)** : Helped in fine-tuning the model on SQuAD dataset and evalueated the model.
3. **Hitesh Kumar (22110098)** : Fine-tuned the model on SQuAD dataset and SST-2 dataset.
4. **Ruchit Jagodara (22110102)** : Evaluated fine tuned model on SQuAD dataset.
5. **Jinil Patel (22110184)** : Evaluated fine tuned model on SST-2 dataset and helped in fine-tuning of SST-2 dataset.

## Task - 1

### Project: Fine-Tuning and Evaluation of the Llama 3.2-1B/Gemma Model

---

#### **1. Model Selection and Parameter Calculation**

- **Selected Model:** [Llama 3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B)
- **Parameter Calculation:**  
  
  - **Calculated Parameters:** `1,235,814,400`
  - **Reported Parameters (in paper):** `1.23 Billion` 
    <div align="center">
        <img src="images/num_param_hf.png" width="600px">
    </div>
  **Comparison:** Since the paper does not explicitly provide the exact number of parameters for the Llama 3.2-1B, we compare the approximate parameter count mentioned in the paper with the parameters calculated through the code. Upon calculation, the parameters are approximately similar, validating the correctness of our implementation and alignment with the model architecture described in the paper.

---

#### **2. Fine-Tuning Process**

- **Datasets:**  
  - **Classification Task:** SST-2 (Sentiment Analysis)  
  - **Question-Answering Task:** SQuAD (Stanford Question Answering Dataset)

- **Train-Test Split:**  
  - Split ratio: 80% train, 20% test  
  - Sampling: Stratified sampling

- **Fine-Tuning Process:**  
  1. Classification Task: SST-2  
     - Loaded pre-trained Llama 3.2-1B using AutoModelForSequenceClassification.

     <div align="center">
        <img src="images/sst2_train.png" width="500px">
     </div>

     <div align="center">
        <img src="images/sst2_training.png" width="500px">
     </div>
     <br>
     
    2. Question-Answering Task: SQuAD  
    - Loaded pre-trained Llama 3.2-1B using AutoModelCausalLM and added custom output layer for the respective task.
     <div align="center">
        <img src="images/qa_trainLoss.png" width="500px">
     </div>
     <div align="center">
        <img src="images/qa_training.png" width="300px">
     </div>

---

#### **3. Evaluation Metrics**

##### **Classification (SST-2)**  
- Metrics:  
  - **Accuracy**: Measures overall correctness.  
  - **Precision**: Measures the ratio of correctly predicted positive observations to the total predicted positives.  
  - **Recall**: Measures the ratio of correctly predicted positive observations to the all positives in the dataset.  
  - **F1 Score**: Harmonic mean of precision and recall.  

  | **Pretrained (Zero-shot)** | **Fine-tuned**       |
  |--------------------|------------------------|
  |![Zero-shot](images/sst2_evalbefore.png) | ![Accuracy Fine-tuned](images/sst2_evalafter.png) |

##### **Question-Answering (SQuAD)**  
- Metrics:  
  - **squad_v2**: Performance on unanswerable questions.  
  - **F1 Score**: Measures overlap between prediction and ground truth.  
  - **METEOR, BLEU, ROUGE**: Evaluate textual similarity.  
  - **Exact Match**: Measures strict correctness.

  | **Pretrained (Zero-shot)** | **Fine-tuned**       |
  |--------------------|------------------------|
  | <img src="images/qa_evalbefore.png" width="200px"> | <img src="images/qa_evalafter.png" width="200px"> |

---

#### **4. Model Parameters After Fine-Tuning**

> **Note:** In fine-tuning we are adding a task specific head to the output of the pre-trained `Llama 3.2-1B model`(base model). While importing 

  1. Classification Task: SST-2 
  
  - Pre-trained model parameters: `1,235,814,400`  
  - Fine-tuned model parameters: `1,235,818,496`  
  <div align="center">
    <img src="images/sst2_params.png">
  </div>
  
  2. Question-Answering Task: SQuAD  
  
  - Pre-trained model parameters: `1,235,814,400`  
  - Fine-tuned model parameters: `1,235,818,498`  
  <div align="center">
    <img src="images/qa_params.png">
  </div>

  - **Conclusion:** The total number of parameters in the pre-trained model and fine-tuned model are different due to the addition of task-specific layer. The base model parameters remain the same, and the additional parameters are due to the task-specific head added during fine-tuning and are only trained on the task-specific dataset.

---

#### **5. Model Upload to Hugging Face**

Fine-tuned models are uploaded to the 🤗 Hub: 
  - [Llama 3.2-1B Fine-Tuned on SST-2](https://huggingface.co/bp03/Classification_SST2_Llama_3.2_1B_Model/tree/main)
  - [Llama 3.2-1B Fine-Tuned on SQuAD](https://huggingface.co/bp03/QuestionAnswering_SQUADV2_Llamma_3.2_1B/tree/main)

---

#### **6. Analysis of Results**

1. Classification Task: SST-2
    - **Higher Scores in Fine-Tuned Models:**  
      - The fine-tuned models exhibit higher scores compared to the pre-trained models on the zero-shot evaluation. This is because the fine-tuned models are more task-specific and have learned the patterns specific to the SST-2 dataset.
      - The fine-tuned models have a task-specific head that is trained on the SST-2 dataset, which helps in capturing the sentiment patterns effectively.
      - The fine-tuned models are more specialized for the SST-2 task, leading to better performance compared to the zero-shot evaluation.

    - **Understanding Parameter Behavior:**  
      - The number of parameters in the fine-tuned model increases due to the addition of task-specific layers which has a total of 4096 parameters.
      - The base model parameters remain the same, and the additional parameters are only trained on the task-specific dataset.
      - The base model parameters are freezed and only the task-specific head is trained on the task-specific dataset.

        <p align='center'><img src="images/sst2_params.png" width="500px"> </p>

    - **Zero-Shot vs. Fine-Tuned Performance:**
      - Zero-shot models generalize poorly on specialized tasks like sentiment analysis or question answering whereas fine-tuned models are more task-specific and exhibit better performance on the respective tasks.

        | **Pretrained (Zero-shot)** | **Fine-tuned**      |
        |--------------------|------------------------|
        |![Zero-shot](images/sst2_evalbefore.png) | ![Accuracy Fine-tuned](images/sst2_evalafter.png) |

2. Question-Answering Task: SQuAD
    - **Lower Scores in Fine-Tuned Models:**  
      - The fine-tuned models exhibit lower scores compared to the pre-trained models on the zero-shot evaluation. Following could be the possible reasons for that:
        - **Overfitting:** The fine-tuned models might overfit on the training data, leading to lower generalization on the test set.
        - **Task-Specific Head:** The task-specific head added during fine-tuning might not be able to capture the underlying patterns effectively.
        - **Data Mismatch:** The fine-tuned models might not have been exposed to a diverse range of examples during training, leading to lower performance.
        - **Model Complexity:** The pre-trained model might be too complex for the task, leading to difficulties in fine-tuning.
      - We were not able to fine-tune the model for a sufficient number of epochs due to computational constraints, as it was taking a lot of time to train the model on the entire dataset and also the kaggle notebook was crashing due to memory issues.


    - **Understanding Parameter Behavior:**  
      - The number of parameters in the fine-tuned model increases due to the addition of task-specific layers.  
      - The base model parameters remain the same, and the additional parameters are only trained on the task-specific dataset.
      - The base model parameters are freezed and only the task-specific head is trained on the task-specific dataset.

        <p align='center'><img src="images/qa_params.png" width="500px"> </p>

    - **Zero-Shot vs. Fine-Tuned Performance:**  
      - Zero-shot models generalize poorly on specialized tasks like sentiment analysis or question answering whereas fine-tuned models are more task-specific and exhibit better performance on the respective tasks. But, due to the problems faced during training, we were not able to get the desired results.
        
          | **Pretrained (Zero-shot)** | **Fine-tuned**      |
          |--------------------|------------------------|
          |<img src="images/qa_evalbefore.png" width="300px"> | <img src="images/qa_evalafter.png" width="300px"> |

---