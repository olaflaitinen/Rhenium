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
models = ['GPT-4 (Baseline)', 'Llama-3-8B (Base)', 'Llama-3-8B (Fine-Tuned)']
execution_accuracy = [88.5, 45.2, 82.1]
exact_match_accuracy = [75.0, 30.5, 78.4]
latency = [1.2, 0.4, 0.45]  # Seconds

# 1. Accuracy Comparison Chart
plt.figure(figsize=(10, 6))
x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, execution_accuracy, width, label='Execution Accuracy (%)', color='#4CAF50')
rects2 = ax.bar(x + width/2, exact_match_accuracy, width, label='Exact Match Accuracy (%)', color='#2196F3')

ax.set_ylabel('Accuracy (%)')
ax.set_title('Model Performance Comparison: Text-to-SQL')
ax.set_xticks(x)
ax.set_xticklabels(models)
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
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.savefig(f"{output_dir}/accuracy_comparison.png", dpi=300)
print(f"Generated {output_dir}/accuracy_comparison.png")

# 2. Latency Comparison Chart
plt.figure(figsize=(8, 5))
bars = plt.bar(models, latency, color=['#FF9800', '#9C27B0', '#673AB7'])
plt.ylabel('Average Latency (seconds)')
plt.title('Inference Latency Comparison')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}s',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig(f"{output_dir}/latency_comparison.png", dpi=300)
print(f"Generated {output_dir}/latency_comparison.png")
