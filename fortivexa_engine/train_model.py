import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("⏳ [FORTIVEXA ENGINE] Processing Dataset...")
df = pd.read_csv("fortivexa_synthetic_dataset.csv")

# 1. Multi-Layer Directed Mule Network Construction
print("🕸️ Building Directed Graph Network...")
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['Layer1_Mule'], row['Layer2_Mule'], amount=row['Amount_Lost'])
    G.add_edge(row['Layer2_Mule'], row['Layer3_Mule'], amount=row['Amount_Lost'])
    G.add_edge(row['Layer3_Mule'], row['Target_ATM_ID'], amount=row['Amount_Lost'])

# Degree Centrality Calculation for Mule Hub Detection
print("📊 Calculating Graph Centrality Metrics for Mule Hubs...")
degree_centrality = nx.degree_centrality(G)
df['Mule_Hub_Risk_Score'] = df['Layer1_Mule'].map(degree_centrality).fillna(0)

# 2. Machine Learning Feature Pipeline
le_modus = LabelEncoder()
le_pincode = LabelEncoder()

df['Modus_Operandi_Enc'] = le_modus.fit_transform(df['Modus_Operandi'])
df['Target_Pincode_Enc'] = le_pincode.fit_transform(df['Target_Pincode'].astype(str))

X = df[['Modus_Operandi_Enc', 'Amount_Lost', 'Time_Lag_Mins', 'Is_Crypto_POS_Node', 'Mule_Hub_Risk_Score']]
y = df['Target_Pincode_Enc']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"🎯 FORTIVEXA Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Save Artifacts
joblib.dump(model, 'fortivexa_model.pkl', compress=3)
joblib.dump(le_modus, 'fortivexa_le_modus.pkl')
joblib.dump(le_pincode, 'fortivexa_le_pincode.pkl')
joblib.dump(G, "fortivexa_graph.pkl", compress=3)

print("💾 All FORTIVEXA Artifacts Saved Successfully!")
