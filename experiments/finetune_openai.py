"""
Fine-tuning script for GPT-4o-mini using OpenAI API.
"""
import os
import time
import json
from openai import OpenAI

# Ensure OPENAI_API_KEY is set in .env
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def train():
    print("Preparing data for OpenAI Fine-Tuning...")
    
    # Convert our JSONL to OpenAI Chat format if needed
    # For this script, we assume data/training_data_openai.jsonl exists
    # Format: {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
    
    training_file_path = "data/training_data_openai.jsonl"
    
    if not os.path.exists(training_file_path):
        print(f"Error: {training_file_path} not found.")
        return

    print("Uploading training file...")
    training_file = client.files.create(
        file=open(training_file_path, "rb"),
        purpose="fine-tune"
    )
    print(f"File uploaded. ID: {training_file.id}")

    print("Starting Fine-Tuning Job for gpt-4o-mini...")
    job = client.fine_tuning.jobs.create(
        training_file=training_file.id,
        model="gpt-4o-mini-2024-07-18"
    )
    
    print(f"Job created. ID: {job.id}")
    print("Monitoring status...")
    
    while True:
        job_status = client.fine_tuning.jobs.retrieve(job.id)
        print(f"Status: {job_status.status}")
        
        if job_status.status in ["succeeded", "failed", "cancelled"]:
            break
            
        time.sleep(60)
        
    if job_status.status == "succeeded":
        print(f"Fine-tuning complete! Model ID: {job_status.fine_tuned_model}")
        # Save this model ID to config
        with open("experiments/openai_ft_model_id.txt", "w") as f:
            f.write(job_status.fine_tuned_model)
    else:
        print("Fine-tuning failed.")

if __name__ == "__main__":
    train()
