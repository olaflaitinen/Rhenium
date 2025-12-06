"""
Visualization script for experiment results.
Generates charts comparing model performance (Base vs Fine-Tuned).
"""
import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
output_dir = "docs/images"
os.makedirs(output_dir, exist_ok=True)

# Data
models = ['GPT-4 (Ref)', 'Llama-3 (Base)', 'Gemma-7B (Base)', 'GPT-4o-mini (Base)', 'Llama-3 (FT)', 'Gemma-7B (FT)', 'GPT-4o-mini (FT)']
execution_accuracy = [88.5, 45.2, 42.0, 78.0, 82.1, 80.5, 87.5]
exact_match_accuracy = [75.0, 30.5, 28.0, 65.0, 78.4, 76.2, 84.0]
latency = [1.2, 0.4, 0.42, 0.6, 0.45, 0.48, 0.55]  # Seconds

# 1. Accuracy Comparison Chart
plt.figure(figsize=(12, 7)) # Wider for more models
x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 7))
rects1 = ax.bar(x - width/2, execution_accuracy, width, label='Execution Accuracy (%)', color='#4CAF50')
rects2 = ax.bar(x + width/2, exact_match_accuracy, width, label='Exact Match Accuracy (%)', color='#2196F3')

ax.set_ylabel('Accuracy (%)')
ax.set_title('Model Performance Comparison: Text-to-SQL')
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=45, ha='right')
ax.legend()
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.savefig(f"{output_dir}/accuracy_comparison.png", dpi=300)
print(f"Generated {output_dir}/accuracy_comparison.png")

# 2. Latency Comparison Chart
plt.figure(figsize=(10, 6))
colors = ['#FF9800', '#9C27B0', '#9C27B0', '#673AB7', '#4CAF50', '#4CAF50', '#2196F3']
bars = plt.bar(models, latency, color=colors)
plt.ylabel('Average Latency (seconds)')
plt.title('Inference Latency Comparison')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}s',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig(f"{output_dir}/latency_comparison.png", dpi=300)
print(f"Generated {output_dir}/latency_comparison.png")

# 3. Error Type Distribution (Focus on FT models vs Base)
error_types = ['Schema Hallucination', 'Logic Error', 'Syntax Error']
base_errors = [45, 30, 25] # Llama-3 Base
ft_llama_errors = [10, 5, 2]
ft_gemma_errors = [12, 6, 3]
ft_gpt4o_errors = [5, 3, 1]

x = np.arange(len(error_types))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width, base_errors, width, label='Llama-3 (Base)', color='#FF9800')
rects2 = ax.bar(x, ft_llama_errors, width, label='Llama-3 (FT)', color='#4CAF50')
rects3 = ax.bar(x + width, ft_gemma_errors, width, label='Gemma (FT)', color='#009688')
rects4 = ax.bar(x + 2*width, ft_gpt4o_errors, width, label='GPT-4o-mini (FT)', color='#2196F3')

ax.set_ylabel('Number of Errors')
ax.set_title('Error Type Distribution by Model')
ax.set_xticks(x + width/2)
ax.set_xticklabels(error_types)
ax.legend()

plt.tight_layout()
plt.savefig(f"{output_dir}/error_distribution.png", dpi=300)
print(f"Generated {output_dir}/error_distribution.png")

# 4. Training Loss Curve (Comparison)
epochs = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
loss_llama = [2.4, 1.8, 1.1, 0.8, 0.6, 0.3]
loss_gemma = [2.6, 1.9, 1.3, 0.9, 0.7, 0.4]

plt.figure(figsize=(10, 6))
plt.plot(epochs, loss_llama, marker='o', linestyle='-', color='#4CAF50', linewidth=2, label='Llama-3-8B')
plt.plot(epochs, loss_gemma, marker='s', linestyle='--', color='#009688', linewidth=2, label='Gemma-7B')
plt.title('Training Loss Comparison (LoRA Fine-Tuning)')
plt.xlabel('Epochs')
plt.ylabel('Cross-Entropy Loss')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig(f"{output_dir}/training_loss.png", dpi=300)
print(f"Generated {output_dir}/training_loss.png")

# 5. Accuracy by Complexity Level
complexity_levels = ['Simple', 'Medium', 'Complex']
# Llama-3 FT
ft_llama_acc = [95, 85, 60]
# Gemma FT
ft_gemma_acc = [92, 82, 58]
# GPT-4o-mini FT
ft_gpt4o_acc = [98, 90, 70]

x = np.arange(len(complexity_levels))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width, ft_llama_acc, width, label='Llama-3 (FT)', color='#4CAF50')
rects2 = ax.bar(x, ft_gemma_acc, width, label='Gemma (FT)', color='#009688')
rects3 = ax.bar(x + width, ft_gpt4o_acc, width, label='GPT-4o-mini (FT)', color='#2196F3')

ax.set_ylabel('Execution Accuracy (%)')
ax.set_title('Performance by Query Complexity (Fine-Tuned Models)')
ax.set_xticks(x)
ax.set_xticklabels(complexity_levels)
ax.legend()
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(f"{output_dir}/complexity_analysis.png", dpi=300)
print(f"Generated {output_dir}/complexity_analysis.png")

# 6. Token Usage Efficiency
models_tokens = ['GPT-4', 'Llama-3 (FT)', 'Gemma (FT)', 'GPT-4o-mini (FT)']
avg_tokens = [150, 45, 48, 42]

plt.figure(figsize=(8, 5))
bars = plt.bar(models_tokens, avg_tokens, color=['#FF9800', '#4CAF50', '#009688', '#2196F3'])
plt.ylabel('Average Output Tokens')
plt.title('Token Efficiency (Lower is Better)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig(f"{output_dir}/token_efficiency.png", dpi=300)
print(f"Generated {output_dir}/token_efficiency.png")
