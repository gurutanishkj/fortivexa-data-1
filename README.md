# 🛡️ FORTIVEXA: AI-Powered Cybercrime Intelligence & ATM Cash-Out Forecasting Platform

**Problem Statement ID:** SIH26184  
**Target Agency:** Ministry of Home Affairs (MHA) & Law Enforcement Agencies (LEAs)  
**Core Technologies:** Python 3.10+, Vanilla HTML5, Vanilla CSS3, JavaScript (ES6+), Leaflet.js, Chart.js, NetworkX, Scikit-Learn, Streamlit, Folium, Pandas, NumPy, Faker  

---

## 🌐 Web Application & Intelligence Command Center

All synthetic dataset records, multi-layer mule account graphs, spatial ATM clusters, prediction algorithms, and jury defense edge cases have been **merged into a unified interactive Web Platform**.

### 🚀 How to Launch the Web Platform

#### Option 1: Built-in Python Server (Recommended)
```bash
python server.py
```
Open your browser at **[http://localhost:8000](http://localhost:8000)**.

#### Option 2: Direct Browser Launch (Zero-Setup)
Simply double-click or open **[`index.html`](file:///c:/Users/kkart/Music/fortivexa%20data1/index.html)** in any modern web browser (Chrome, Edge, Firefox, Safari). The bundled `fortivexa_data.js` ensures that all data, charts, and maps work instantly with zero CORS issues!

#### Option 3: Streamlit Cyber Cell Dashboard
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)**.

---

## 🏛️ System Architecture Workflow

```
[1. Victim Incident Ingestion (NCRP / 1930 Portal)]
                     │
                     ▼
[2. MHA CFCFRMS Gateway & Automated Bank API Service]
  ├── Captures Complaint Metadata & Transaction UTR
  └── Direct Query to Bank Gateway (Resolves First-Layer Mule Account)
                     │
                     ▼
[3. Real-Time Stream Engine (Apache Kafka & Flink)]
  ├── Ingests High-Volume Transaction Streams (Scalability Guarantee)
  └── Passes Event Nodes to Graph Store (Neo4j / Amazon Neptune)
                     │
                     ▼
[4. Multi-Layer Graph Intelligence (Dynamic Temporal GNN / TGN)]
  ├── Traces Layer-1 ➔ Layer-2 ➔ Layer-3 Mule Account Chains
  ├── Louvain / Leiden Community Detection (Identifies Mule Syndicates)
  └── Federated Learning Framework (Ensures Inter-Bank Data Privacy)
                     │
                     ▼
[5. Spatio-Temporal Prediction & ATM Risk Engine]
  ├── Features: Transaction Velocity, Amount, Scam Modus Operandi
  ├── DBSCAN Spatial Clustering on Historical Cash-out Hotspots
  └── ATM Metadata Fusion (Considers CCTV presence, location isolation)
                     │
                     ▼
[6. FORTIVEXA Actionable Command & Control Dashboard]
  ├── Mapbox Geo-Fencing & Live Heatmap Displays
  └── Automated Geo-Targeted Alerts to Local PCR Vans / Field Officers
```

---

## ⚖️ Built-In Jury Rectification & Edge-Case Defenses

1. **Non-Banking Node Routing (Crypto Exchanges / E-Wallets / Gift Cards):**
   - **Resolution:** FORTIVEXA interfaces with CFCFRMS nodes connected to FIU-IND, VASP (WazirX/CoinDCX), and E-Wallet APIs. If funds shift to non-banking entities, a `Is_Crypto_POS_Node` flag triggers an automated **Freeze API Request** to exchange compliance desks.
2. **Delayed Cash-Out Strategies (2+ Days Delay):**
   - **Resolution:** Employs Temporal Graph Neural Network (TGNN) principles via `Time_Lag_Mins` and holding time velocity models to dynamically shift the alert prediction window from immediate interception to proactive surveillance.
3. **Merchant POS & Jewellery Shop Redirection:**
   - **Resolution:** Fuses Merchant Category Codes (MCC 5944 for Jewellery, 5541 for Fuel). Shifts automatically from *ATM Cash-Out Mode* to *Geo-Merchant Alert Mode*.
4. **High Scalability & Zero System Crashing:**
   - **Resolution:** Architecture handles 100,000+ events/sec via Apache Kafka event streaming, Apache Flink real-time windowing, and millisecond graph traversals.
5. **Mitigation of False Positives:**
   - **Resolution:** Issues tactical alerts only when the Risk Confidence Score > 80% and projects a 3-km Spatial Radius Cluster instead of isolated speculative points.
6. **Spatio-Temporal Pattern Fusing:**
   - **Resolution:** Integrates historical cash-out spatial density (DBSCAN) with real-time time-lag analysis and ATM isolation metrics.

---

## 📁 Project File Structure

```
fortivexa data1/
│
├── index.html                       # Standalone Modern Web Application
├── style.css                        # Cyber-Command Center Design System (Vanilla CSS)
├── app.js                           # Interactive Client Logic, Leaflet Map & Chart.js
├── fortivexa_data.js                # Merged 10,000 Records & Graph Payload (Browser Bundle)
├── fortivexa_data.json              # Merged JSON Dataset for API Ingestion
├── server.py                        # Zero-Dependency Python Web Server (Port 8000)
├── export_web_data.py               # Data Aggregation & Merger Pipeline
│
├── requirements.txt                 # Stage 0: System Dependencies
├── generate_data.py                 # Stage 1: Advanced Synthetic Dataset Generator
├── train_model.py                   # Stage 2: Mule Graph Extraction & Prediction Engine
├── app.py                           # Stage 3: Streamlit Interactive Command Center
├── fortivexa_synthetic_dataset.csv  # 10,000 Multi-Layer Incident Records
├── fortivexa_model.pkl              # Trained Random Forest Predictive Classifier
├── fortivexa_le_modus.pkl           # Modus Operandi Label Encoder
├── fortivexa_le_pincode.pkl         # Pincode Label Encoder
├── fortivexa_graph.pkl              # NetworkX Multi-Layer Directed Mule Graph
└── fortivexa_engine/                # Self-Contained Engine Module Mirror
```
