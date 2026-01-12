import gensim
from gensim.models import Word2Vec
import warnings
import pandas as pd
import json
import os
from tqdm import tqdm
import numpy as np

# ==============================================================================
# 0. CONFIGURATION
# ==============================================================================
DATASET_PATH = "../Dataset/All_Data.csv"
OUTPUT_FILE = "w2v_matrix_final01.json"
W2V_DIMENSION = 100 
W2V_WINDOW = 5      
W2V_MIN_COUNT = 1

# ==============================================================================
# 1. PREPARE DATA
# ==============================================================================
df = pd.read_csv(DATASET_PATH)
api_sequences = []
for index, row in tqdm(df.iterrows(), total=len(df), desc="Extracting API Sequences"):
    sequence = row.iloc[1:].dropna().astype(str).tolist()
    if len(sequence) > 0:
        api_sequences.append(sequence)

print(f"--- Đã trích xuất {len(api_sequences)} chuỗi API ---")

# ==============================================================================
# 2. TRAINING
# ==============================================================================

print("--- Bắt đầu huấn luyện Word2Vec (Skip-gram) ---")
# Khởi tạo mô hình
w2v_model = Word2Vec(
    sentences=api_sequences,
    vector_size=W2V_DIMENSION, 
    window=W2V_WINDOW, 
    min_count=W2V_MIN_COUNT,
    sg=1, 
    workers=4, 
    epochs=20 
)

unique_apis_learned = list(w2v_model.wv.index_to_key)
print(f"--- Đã học được {len(unique_apis_learned)} API duy nhất ---")

# ==============================================================================
# 3. SAVE A DICTIONARY TO JSON
# ==============================================================================
W2V_EMBEDDING = {}
for api_name in unique_apis_learned:
    vector = w2v_model.wv[api_name]
    W2V_EMBEDDING[api_name] = vector.tolist()

with open(OUTPUT_FILE, 'w') as f:
    json.dump(W2V_EMBEDDING, f, indent=4)

print(f"--- Đã lưu W2V_EMBEDDING vào {OUTPUT_FILE} ---")