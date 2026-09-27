import pandas as pd
import numpy as np
import json
import joblib
import networkx as nx
import os

print("🔄 Processing and merging all FORTIVEXA dataset records...")

df = pd.read_csv("fortivexa_synthetic_dataset.csv")

# 1. Summary Statistics
total_incidents = len(df)
total_amount_lost = float(df['Amount_Lost'].sum())
avg_amount_lost = float(df['Amount_Lost'].mean())
avg_time_lag = float(df['Time_Lag_Mins'].mean())
crypto_pos_count = int((df['Is_Crypto_POS_Node'] == 1).sum())
atm_count = total_incidents - crypto_pos_count

# 2. City & Pincode Profiles
city_stats = {}
for city, grp in df.groupby('Target_City'):
    pincode = str(grp['Target_Pincode'].iloc[0])
    city_stats[city] = {
        "city": city,
        "pincode": pincode,
        "lat": float(grp['ATM_Latitude'].mean()),
        "lon": float(grp['ATM_Longitude'].mean()),
        "total_incidents": int(len(grp)),
        "total_amount": float(grp['Amount_Lost'].sum()),
        "avg_time_lag": float(round(grp['Time_Lag_Mins'].mean(), 1)),
        "atm_count": int(grp['Target_ATM_ID'].nunique()),
        "crypto_nodes": int((grp['Is_Crypto_POS_Node'] == 1).sum()),
        "mcc_distribution": grp['MCC_Code'].astype(str).value_counts().to_dict(),
        "modus_distribution": grp['Modus_Operandi'].value_counts().to_dict()
    }

# 3. Modus Operandi Analysis
modus_stats = {}
for modus, grp in df.groupby('Modus_Operandi'):
    modus_stats[modus] = {
        "count": int(len(grp)),
        "total_amount": float(grp['Amount_Lost'].sum()),
        "avg_amount": float(round(grp['Amount_Lost'].mean(), 2)),
        "avg_time_lag": float(round(grp['Time_Lag_Mins'].mean(), 1)),
        "top_cities": grp['Target_City'].value_counts().head(3).to_dict(),
        "top_pincodes": grp['Target_Pincode'].astype(str).value_counts().head(3).to_dict()
    }

# 4. Bank Analysis (Layer 1 Mule Banks)
df['Layer1_Bank'] = df['Layer1_Mule'].apply(lambda x: x.split('_')[1] if '_' in str(x) else 'UNKNOWN')
bank_stats = df['Layer1_Bank'].value_counts().to_dict()

# 5. Graph Intelligence & Top Mule Hubs
print("🕸️ Extracting graph centrality and mule syndicates...")
G = joblib.load("fortivexa_graph.pkl")
degree_dict = nx.degree_centrality(G)
sorted_nodes = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:30]

top_mule_hubs = []
for node, score in sorted_nodes:
    node_type = "ATM Node" if "ATM" in node else ("Mule Layer 2" if "MULE2" in node else ("Mule Layer 3" if "MULE3" in node else "Mule Layer 1"))
    top_mule_hubs.append({
        "node_id": node,
        "type": node_type,
        "centrality_score": float(round(score, 6)),
        "risk_tier": "CRITICAL" if score > 0.0003 else "ELEVATED"
    })

# 6. Sample Records for Table & Live Exploration (First 1,000 detailed records for client-side search & display)
sample_records = []
for _, row in df.head(1000).iterrows():
    sample_records.append({
        "complaint_id": str(row['Complaint_ID']),
        "modus_operandi": str(row['Modus_Operandi']),
        "amount_lost": float(row['Amount_Lost']),
        "timestamp": str(row['Incident_Timestamp']),
        "utr": str(row['UTR_Number']),
        "layer1_mule": str(row['Layer1_Mule']),
        "layer2_mule": str(row['Layer2_Mule']),
        "layer3_mule": str(row['Layer3_Mule']),
        "time_lag": int(row['Time_Lag_Mins']),
        "target_pincode": str(row['Target_Pincode']),
        "target_city": str(row['Target_City']),
        "target_atm_id": str(row['Target_ATM_ID']),
        "lat": float(row['ATM_Latitude']),
        "lon": float(row['ATM_Longitude']),
        "is_crypto": int(row['Is_Crypto_POS_Node']),
        "mcc_code": str(row['MCC_Code'])
    })

# 7. Hotspot ATMs (Unique ATMs with coordinates, city, and transaction volume)
atm_hotspots = []
for atm_id, grp in df.groupby('Target_ATM_ID'):
    first = grp.iloc[0]
    atm_hotspots.append({
        "atm_id": atm_id,
        "city": str(first['Target_City']),
        "pincode": str(first['Target_Pincode']),
        "lat": float(first['ATM_Latitude']),
        "lon": float(first['ATM_Longitude']),
        "is_crypto": int(first['Is_Crypto_POS_Node']),
        "mcc": str(first['MCC_Code']),
        "tx_count": int(len(grp)),
        "total_volume": float(grp['Amount_Lost'].sum()),
        "cctv_active": True if int(str(hash(atm_id))[-1]) % 2 == 0 else False
    })
# Sort ATMs by transaction count
atm_hotspots = sorted(atm_hotspots, key=lambda x: x['tx_count'], reverse=True)

# 8. Time-Lag Velocity Buckets
time_buckets = {
    "< 30 Mins (Hyper-Urgent)": int((df['Time_Lag_Mins'] < 30).sum()),
    "30-120 Mins (Tactical Patrol)": int(((df['Time_Lag_Mins'] >= 30) & (df['Time_Lag_Mins'] < 120)).sum()),
    "2-6 Hours (Rapid Dispersion)": int(((df['Time_Lag_Mins'] >= 120) & (df['Time_Lag_Mins'] < 360)).sum()),
    "6-24 Hours (Holding Period)": int(((df['Time_Lag_Mins'] >= 360) & (df['Time_Lag_Mins'] < 1440)).sum()),
    "> 24 Hours (Delayed Strategy)": int((df['Time_Lag_Mins'] >= 1440).sum())
}

# Consolidated Web Payload
web_data = {
    "summary": {
        "total_incidents": total_incidents,
        "total_amount_lost": total_amount_lost,
        "avg_amount_lost": round(avg_amount_lost, 2),
        "avg_time_lag": round(avg_time_lag, 1),
        "crypto_pos_count": crypto_pos_count,
        "atm_count": atm_count,
        "total_graph_nodes": G.number_of_nodes(),
        "total_graph_edges": G.number_of_edges(),
        "total_atms_mapped": len(atm_hotspots)
    },
    "cities": city_stats,
    "modus_stats": modus_stats,
    "bank_stats": bank_stats,
    "time_buckets": time_buckets,
    "top_mule_hubs": top_mule_hubs,
    "atm_hotspots": atm_hotspots[:150],  # Top 150 ATMs for fast client map rendering
    "sample_records": sample_records
}

# Save as JSON
with open("fortivexa_data.json", "w", encoding="utf-8") as f:
    json.dump(web_data, f, indent=2)

# Also save as a JS file so index.html works with zero CORS issues even if opened via file:// protocol!
js_content = f"window.FORTIVEXA_DATA = {json.dumps(web_data, indent=2)};"
with open("fortivexa_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ Successfully exported web data:")
print(f"   • fortivexa_data.json ({os.path.getsize('fortivexa_data.json'):,} bytes)")
print(f"   • fortivexa_data.js ({os.path.getsize('fortivexa_data.js'):,} bytes)")
