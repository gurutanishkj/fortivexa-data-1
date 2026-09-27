import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')
np.random.seed(42)
random.seed(42)

def generate_fortivexa_dataset(num_records=10000):
    data = []
    
    pincode_map = {
        "600001": {"city": "Chennai Central", "lat": 13.0827, "lon": 80.2707},
        "600040": {"city": "Anna Nagar", "lat": 13.0850, "lon": 80.2101},
        "620001": {"city": "Trichy", "lat": 10.7905, "lon": 78.7047},
        "625001": {"city": "Madurai", "lat": 9.9252, "lon": 78.1198},
        "627001": {"city": "Tirunelveli", "lat": 8.7139, "lon": 77.7567},
        "110001": {"city": "New Delhi", "lat": 28.6139, "lon": 77.2090},
        "400001": {"city": "Mumbai", "lat": 18.9388, "lon": 72.8353}
    }
    
    pincodes = list(pincode_map.keys())
    fraud_types = ['UPI Phishing', 'Digital Arrest', 'Job Offer Fraud', 'Investment Scam', 'Credit Card Fraud']
    banks = ['SBI', 'HDFC', 'ICICI', 'AXIS', 'CANARA', 'IOB']
    mcc_codes = ['5541', '5944', '6011', '7995']  # Fuel, Jewellery, ATM Cash, Gambling
    
    # Realistic syndicate geographic affinity for high-precision model convergence (>80% confidence)
    pincode_affinity = {
        'UPI Phishing': ["600001", "600040"],
        'Digital Arrest': ["110001", "400001"],
        'Job Offer Fraud': ["620001", "625001"],
        'Investment Scam': ["400001", "600001"],
        'Credit Card Fraud': ["600040", "627001"]
    }
    
    start_date = datetime(2026, 1, 1)

    for i in range(1, num_records + 1):
        complaint_id = f"FORT-2026-{10000 + i}"
        fraud_type = random.choice(fraud_types)
        amount_lost = round(random.uniform(5000, 1000000), 2)
        
        incident_time = start_date + timedelta(days=random.randint(0, 200), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        utr_number = f"UTR2026{random.randint(100000000, 999999999)}"
        
        layer1_bank = random.choice(banks)
        layer1_mule = f"MULE1_{layer1_bank}_{random.randint(1000, 9999)}"
        layer2_mule = f"MULE2_{random.choice(banks)}_{random.randint(1000, 9999)}"
        layer3_mule = f"MULE3_{random.choice(banks)}_{random.randint(1000, 9999)}"
        
        # Syndicate modus operandi hotspot affinity with noise
        if random.random() < 0.85:
            target_pincode = random.choice(pincode_affinity[fraud_type])
        else:
            target_pincode = random.choice(pincodes)
        geo_info = pincode_map[target_pincode]
        
        atm_lat = geo_info["lat"] + round(random.uniform(-0.02, 0.02), 4)
        atm_lon = geo_info["lon"] + round(random.uniform(-0.02, 0.02), 4)
        
        atm_id = f"ATM_{layer1_bank}_{target_pincode}_{random.randint(10, 99)}"
        time_lag_mins = random.randint(5, 2880)  # Handles delayed cash-outs up to 48 hours
        is_crypto_pos = random.choices([0, 1], weights=[0.80, 0.20])[0]
        mcc_code = random.choice(mcc_codes) if is_crypto_pos else '6011'

        data.append({
            "Complaint_ID": complaint_id,
            "Modus_Operandi": fraud_type,
            "Amount_Lost": amount_lost,
            "Incident_Timestamp": incident_time.strftime("%Y-%m-%d %H:%M:%S"),
            "UTR_Number": utr_number,
            "Layer1_Mule": layer1_mule,
            "Layer2_Mule": layer2_mule,
            "Layer3_Mule": layer3_mule,
            "Time_Lag_Mins": time_lag_mins,
            "Target_Pincode": target_pincode,
            "Target_City": geo_info["city"],
            "Target_ATM_ID": atm_id,
            "ATM_Latitude": atm_lat,
            "ATM_Longitude": atm_lon,
            "Is_Crypto_POS_Node": is_crypto_pos,
            "MCC_Code": mcc_code
        })

    df = pd.DataFrame(data)
    df.to_csv("fortivexa_synthetic_dataset.csv", index=False)
    print(f"✅ Generated {num_records} FORTIVEXA records: fortivexa_synthetic_dataset.csv")

if __name__ == "__main__":
    generate_fortivexa_dataset(10000)
