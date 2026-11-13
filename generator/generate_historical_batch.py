import os
import yaml
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Load configuration
with open("generator/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

np.random.seed(cfg["project"]["seed"])
OUT_DIR = cfg["project"]["output_dir"]
os.makedirs(OUT_DIR, exist_ok=True)

print("🚀 Starting UrbanCart Synthetic Data Generator...")

# ---------------------------------------------------------
# 1. GENERATE STORES (50 Stores across India)
# ---------------------------------------------------------
stores = []
store_Formats = ["Flagship", "Mall", "High-Street", "Dark-Store"]
store_idx = 1
for region, cities in cfg["regions"].items():
    for i in range(12 if region != "East" else 14):
        city = cities[i % len(cities)]
        fmt = np.random.choice(store_Formats, p=[0.15, 0.45, 0.30, 0.10])
        stores.append({
            "store_id": f"STR_{city[:3].upper()}_{store_idx:03d}",
            "store_name": f"UrbanCart {city} {fmt} #{i+1}",
            "city": city,
            "region": region,
            "store_format": fmt,
            "sq_ft": int(np.random.choice([2500, 4000, 6500, 10000])),
            "manager_email": f"manager.str{store_idx:03d}@urbancart.in",
            "opened_date": "2023-01-15"
        })
        store_idx += 1

df_stores = pd.DataFrame(stores[:cfg["scale"]["stores"]])
df_stores.to_csv(f"{OUT_DIR}/stores.csv", index=False)
print(f"✅ Generated {len(df_stores)} stores -> {OUT_DIR}/stores.csv")

# ---------------------------------------------------------
# 2. GENERATE ERP PRODUCTS (2,000 SKUs)
# ---------------------------------------------------------
products = []
brands = ["AureliaX", "UrbanPulse", "VedaCraft", "MetroWalk", "SonicWave", "LuxeHome"]
sku_idx = 1
for cat, details in cfg["categories"].items():
    count = int(cfg["scale"]["products"] / len(cfg["categories"]))
    for _ in range(count):
        subcat = np.random.choice(details["subcategories"])
        mrp = float(np.random.randint(details["price_range"][0], details["price_range"][1]))
        margin = np.random.uniform(details["margin_range"][0], details["margin_range"][1])
        cost = round(mrp * (1.0 - margin), 2)
        products.append({
            "sku_id": f"SKU_{cat[:3].upper()}_{sku_idx:04d}",
            "product_name": f"{np.random.choice(brands)} {subcat} {sku_idx}",
            "category": cat,
            "subcategory": subcat,
            "brand": np.random.choice(brands),
            "unit_cost_inr": cost,
            "mrp_inr": mrp,
            "safety_stock_default": int(np.random.choice([15, 25, 40, 60])),
            "is_active": True,
            "updated_at_utc": "2025-05-01T00:00:00Z"
        })
        sku_idx += 1

df_products = pd.DataFrame(products)
df_products.to_csv(f"{OUT_DIR}/erp_products.csv", index=False)
print(f"✅ Generated {len(df_products)} SKUs -> {OUT_DIR}/erp_products.csv")

# ---------------------------------------------------------
# 3. GENERATE CRM CUSTOMERS (100,000 Profiles with PII)
# ---------------------------------------------------------
first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Riya", "Aadhya", "Diya", "Ananya", "Priya", "Neha", "Rohan", "Sneha", "Vikram", "Pooja"]
last_names = ["Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Joshi", "Kulkarni", "Deshmukh", "Singh", "Gupta", "Mehta", "Chatterjee", "Das"]
all_cities = [c for cities in cfg["regions"].values() for c in cities]

n_cust = cfg["scale"]["customers"]
cust_ids = [f"CUST_{i:06d}" for i in range(1, n_cust + 1)]
f_Choice = np.random.choice(first_names, size=n_cust)
l_Choice = np.random.choice(last_names, size=n_cust)

df_customers = pd.DataFrame({
    "customer_id": cust_ids,
    "full_name": [f"{f} {l}" for f, l in zip(f_Choice, l_Choice)],
    "email": [f"{f.lower()}.{l.lower()}{i}@gmail.com" for i, (f, l) in enumerate(zip(f_Choice, l_Choice), 1)],
    "phone": [f"+9198{np.random.randint(10000000, 99999999)}" for _ in range(n_cust)],
    "city": np.random.choice(all_cities, size=n_cust),
    "loyalty_tier": np.random.choice(["Bronze", "Silver", "Gold", "Platinum"], size=n_cust, p=[0.50, 0.30, 0.15, 0.05]),
    "acquisition_channel": np.random.choice(["POS", "APP", "WEB", "INSTAGRAM_AD"], size=n_cust, p=[0.40, 0.30, 0.20, 0.10]),
    "created_at_utc": "2025-01-01T00:00:00Z"
})
df_customers.to_csv(f"{OUT_DIR}/crm_customers.csv", index=False)
print(f"✅ Generated {len(df_customers)} customers -> {OUT_DIR}/crm_customers.csv")

# ---------------------------------------------------------
# 4. GENERATE PROMOTIONS CALENDAR
# ---------------------------------------------------------
promos = [
    {"promo_id": "PRM_NONE", "promo_name": "No Promotion", "discount_type": "NONE", "discount_value": 0.0, "start_date": "2025-01-01", "end_date": "2027-12-31"},
    {"promo_id": "PRM_DIWALI_20", "promo_name": "Diwali Dhamaka 20% Off", "discount_type": "PERCENT", "discount_value": 20.0, "start_date": "2025-10-12", "end_date": "2025-10-26"},
    {"promo_id": "PRM_EOSS_30", "promo_name": "End of Season 30% Off", "discount_type": "PERCENT", "discount_value": 30.0, "start_date": "2026-01-02", "end_date": "2026-01-15"},
    {"promo_id": "PRM_MONSOON_15", "promo_name": "Monsoon Splash 15% Off", "discount_type": "PERCENT", "discount_value": 15.0, "start_date": "2026-07-01", "end_date": "2026-07-12"},
    {"promo_id": "PRM_DIWALI26_25", "promo_name": "Grand Diwali 2026 25% Off", "discount_type": "PERCENT", "discount_value": 25.0, "start_date": "2026-10-25", "end_date": "2026-11-10"},
]
df_promos = pd.DataFrame(promos)
df_promos.to_csv(f"{OUT_DIR}/promotions.csv", index=False)
print(f"✅ Generated {len(df_promos)} promotions -> {OUT_DIR}/promotions.csv")

# ---------------------------------------------------------
# 5. GENERATE HISTORICAL SALES (POS + ECOM) & RETURNS
# ---------------------------------------------------------
start_dt = pd.to_datetime(cfg["project"]["start_date"])
end_dt = pd.to_datetime(cfg["project"]["end_date"])
dates = pd.date_range(start_dt, end_dt, freq="D")

sku_lookup = df_products.set_index("sku_id")[["mrp_inr", "unit_cost_inr"]].to_dict("index")
sku_list = df_products["sku_id"].values
store_list = df_stores["store_id"].values
cust_list = df_customers["customer_id"].values

sales_rows = []
order_counter = 100000

for d in dates:
    mult = cfg["seasonality"]["weekend_multiplier"] if d.weekday() >= 5 else 1.0
    active_promo = "PRM_NONE"
    disc_pct = 0.0
    for fest in cfg["seasonality"]["festivals"]:
        if pd.to_datetime(fest["start"]) <= d <= pd.to_datetime(fest["end"]):
            mult *= fest["multiplier"]
            active_promo = "PRM_DIWALI_20" if "Diwali" in fest["name"] else "PRM_EOSS_30"
            disc_pct = 0.20
            break

    n_txns = int(np.random.normal(650 * mult, 50))
    chosen_skus = np.random.choice(sku_list, size=n_txns)
    chosen_stores = np.random.choice(store_list, size=n_txns)
    chosen_custs = np.random.choice(cust_list, size=n_txns)
    channels = np.random.choice(["POS", "WEB", "APP"], size=n_txns, p=[0.68, 0.14, 0.18])
    payments = np.random.choice(["UPI", "CREDIT_CARD", "DEBIT_CARD", "CASH", "COD"], size=n_txns, p=[0.55, 0.20, 0.12, 0.08, 0.05])
    qtys = np.random.choice([1, 2, 3, 4], size=n_txns, p=[0.70, 0.20, 0.07, 0.03])

    for i in range(n_txns):
        order_counter += 1
        sku = chosen_skus[i]
        mrp = sku_lookup[sku]["mrp_inr"]
        cost = sku_lookup[sku]["unit_cost_inr"]
        q = int(qtys[i])
        gross = round(mrp * q, 2)
        disc = round(gross * disc_pct, 2)
        tax = round((gross - disc) * 0.12, 2)
        net = round(gross - disc + tax, 2)

        sales_rows.append({
            "event_id": f"evt_{order_counter}",
            "order_id": f"ORD_{d.strftime('%Y%m%d')}_{order_counter}",
            "line_item_id": 1,
            "event_time_utc": (d + timedelta(hours=int(np.random.randint(9, 22)), minutes=int(np.random.randint(0, 59)))).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "store_id": chosen_stores[i],
            "customer_id": chosen_custs[i],
            "sku_id": sku,
            "channel_code": channels[i],
            "promo_id": active_promo,
            "payment_type": payments[i],
            "qty": q,
            "unit_price_inr": mrp,
            "gross_amount_inr": gross,
            "discount_amount_inr": disc,
            "tax_amount_inr": tax,
            "net_amount_inr": net,
            "cogs_amount_inr": round(cost * q, 2)
        })

df_sales = pd.DataFrame(sales_rows)

# Inject 0.5% dirty rows for Silver Quarantine testing
n_dirty = int(len(df_sales) * cfg["data_quality_injection"]["dirty_row_rate"])
dirty_indices = np.random.choice(df_sales.index, size=n_dirty, replace=False)
df_sales.loc[dirty_indices[:n_dirty//2], "qty"] = -5
df_sales.loc[dirty_indices[n_dirty//2:], "sku_id"] = None

# Split into POS and E-Commerce datasets
df_pos = df_sales[df_sales["channel_code"] == "POS"].copy()
df_ecom = df_sales[df_sales["channel_code"].isin(["WEB", "APP"])].copy()

df_pos.to_parquet(f"{OUT_DIR}/pos_historical.parquet", index=False)
df_ecom.to_parquet(f"{OUT_DIR}/ecom_orders.parquet", index=False)
print(f"✅ Generated {len(df_pos):,} POS rows & {len(df_ecom):,} E-Com rows (with {n_dirty:,} quarantine test rows)")

# ---------------------------------------------------------
# 6. GENERATE HISTORICAL RETURNS (5.5% Return Rate)
# ---------------------------------------------------------
valid_sales = df_sales.dropna(subset=["sku_id"]).query("qty > 0")
df_returns = valid_sales.sample(frac=0.055, random_state=42).copy()
df_returns["return_id"] = [f"RET_{i:07d}" for i in range(1, len(df_returns) + 1)]
df_returns["original_order_id"] = df_returns["order_id"]
df_returns["return_qty"] = 1
df_returns["refund_amount_inr"] = df_returns["unit_price_inr"]
df_returns["return_reason"] = np.random.choice(
    ["SIZE_ISSUE", "DEFECTIVE", "CHANGED_MIND", "WARDROBING_SUSPECT"],
    size=len(df_returns), p=[0.45, 0.25, 0.22, 0.08]
)
df_returns["receipt_present"] = np.random.choice([True, False], size=len(df_returns), p=[0.92, 0.08])

return_cols = ["return_id", "original_order_id", "event_time_utc", "store_id", "customer_id", "sku_id", "channel_code", "return_qty", "refund_amount_inr", "return_reason", "receipt_present"]
df_returns[return_cols].to_parquet(f"{OUT_DIR}/returns_historical.parquet", index=False)
print(f"✅ Generated {len(df_returns):,} Return records -> {OUT_DIR}/returns_historical.parquet")

# ---------------------------------------------------------
# 7. GENERATE WMS INVENTORY SNAPSHOT (Recent 30 Days x 50 Stores x Top 500 SKUs)
# ---------------------------------------------------------
recent_dates = dates[-30:]
top_skus = sku_list[:500]
inv_rows = []

for d in recent_dates:
    d_str = d.strftime("%Y-%m-%d")
    for st in store_list:
        opening = np.random.randint(5, 120, size=len(top_skus))
        sold = np.random.randint(0, 8, size=len(top_skus))
        received = np.where(opening < 20, np.random.randint(25, 60, size=len(top_skus)), 0)
        closing = np.maximum(0, opening - sold + received)
        for idx, sku in enumerate(top_skus):
            inv_rows.append({
                "snapshot_date": d_str,
                "store_id": st,
                "sku_id": sku,
                "opening_stock_qty": int(opening[idx]),
                "received_qty": int(received[idx]),
                "sold_qty": int(sold[idx]),
                "closing_stock_qty": int(closing[idx]),
                "reorder_point_qty": 20
            })

df_inv = pd.DataFrame(inv_rows)
df_inv.to_parquet(f"{OUT_DIR}/wms_inventory_snapshot.parquet", index=False)
print(f"✅ Generated {len(df_inv):,} Inventory Snapshot rows -> {OUT_DIR}/wms_inventory_snapshot.parquet")
print("🎉 All Historical Batch Files Generated Successfully in generator/output/!")