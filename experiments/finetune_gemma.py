"""
Fine-tuning script for Gemma-7B using Unsloth.
"""
import os
import torch
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# Configuration
max_seq_length = 2048
dtype = None
load_in_4bit = True

def train():
    print("Loading Gemma-7B model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "unsloth/gemma-7b-bnb-4bit",
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )

    # Add LoRA adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r = 64,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                          "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
    )

    # Load Dataset
    dataset = load_dataset("json", data_files={"train": "data/training_data.jsonl"}, split="train")

    def formatting_prompts_func(examples):
        prompts = examples["prompt"]
        outputs = examples["completion"]
        texts = []
        for p, o in zip(prompts, outputs):
            # Gemma chat template format
            text = f"<start_of_turn>user\n{p}<end_of_turn>\n<start_of_turn>model\n{o}<end_of_turn>"
            texts.append(text)
        return { "text" : texts, }

    dataset = dataset.map(formatting_prompts_func, batched = True)

    print("Starting Training...")
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_proc = 2,
        packing = False,
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 60,
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs_gemma",
        ),
    )

    trainer.train()
    
    print("Saving Fine-Tuned Gemma Model...")
    model.save_pretrained("models/gemma-7b-ft")
    tokenizer.save_pretrained("models/gemma-7b-ft")
    print("Done!")

if __name__ == "__main__":
    train()
