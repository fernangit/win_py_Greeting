---
base_model: text-classification_ja
tags:
- generated_from_trainer
metrics:
- accuracy
model-index:
- name: text-classification_ja
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# text-classification_ja

This model is a fine-tuned version of [text-classification_ja](https://huggingface.co/text-classification_ja) on an unknown dataset.
It achieves the following results on the evaluation set:
- Loss: 0.1454
- Accuracy: 0.9783

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 32
- eval_batch_size: 8
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 50.0

### Training results



### Framework versions

- Transformers 4.39.0.dev0
- Pytorch 2.2.1+cpu
- Datasets 2.18.0
- Tokenizers 0.15.2
