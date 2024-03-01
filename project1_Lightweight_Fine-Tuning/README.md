# Lightweight Fine-Tuning Project

## Introduction

Lightweight fine-tuning stands as a crucial technique for adapting foundation models, offering the flexibility to modify models without hefty computational resources. This project focuses on applying parameter-efficient fine-tuning through the Hugging Face `peft` library.

## Project Summary

This project encompasses all essential components of a PyTorch + Hugging Face training and inference process. Key activities include:

- Loading a pre-trained model and evaluating its performance
- Performing parameter-efficient fine-tuning using the pre-trained model
- Conducting inference using the fine-tuned model and comparing its performance to the original model

The project consists of following elements:

- **PEFT Technique:**
    - Explore various PEFT techniques, including LoRA, as detailed in the course material. 
    - Consider LoRA as a suitable starting point, given its compatibility with all models.
- **Model:**
    - Choose a model compatible with your selected PEFT technique and a sequence classification task.
    - Opt for smaller models, especially if using the Udacity Workspace.
    - GPT-2 is recommended if uncertainty persists, given its compatibility with sequence classification and LoRA.
- **Evaluation Approach:**
    - Utilize the evaluation method covered in the course or any reasonable approach suitable for sequence classification tasks.
    - Ensure the ability to compare the original foundation model's performance with the fine-tuned model's performance.
- **Dataset:**
    - Utilize datasets from Hugging Face's library, ensuring compatibility with the task and size constraints of the Udacity Workspace.

# Implementation and Results Summary

This project utilized the IMDb dataset alongside the DistilBERT-base-uncased model for sentiment analysis. Through low-rank adaptation (LoRA), we observed a notable improvement in overall accuracy, albeit with a slight increase in training duration.

- **Fine-tuning Dataset**: Utilized the IMDb dataset, offering a lightweight yet effective resource for sentiment analysis tasks.

- **Model**: Employed DistilBERT-base-uncased, a practical transformer-based model known for its efficiency in NLP tasks.

- **Evaluation Approach**: Primarily assessed accuracy, revealing that low-rank adaptation (LoRA) significantly improved overall accuracy. However, training duration slightly extended due to the adaptation process.

- **PEFT Technique**: Low-rank adaptation (LoRA) demonstrated enhanced accuracy while fine-tuning, despite a slight increase in training time.