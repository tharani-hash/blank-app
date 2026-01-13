# SupplySyncAI — Inventory EDA (Streamlit)

This workspace contains a Streamlit app for inventory EDA.

## Files

- `app.py` — main Streamlit app (Inventory EDA)
- `requirements.txt` — Python dependencies

## Local build & run

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the app with Streamlit:

```bash
streamlit run app.py
```

Open the URL printed by Streamlit (usually http://localhost:8501) in your browser.

## Notes

- The app expects a CSV with columns used in the code (e.g. `stock_value`, `fill_rate_pct`, `stockout_pct`, `inventory_turnover`, `model_confidence_score`, `product_id`, `store_id`, `delivery_time_mins`, `fuel_cost`, `route_efficiency_score`, `transfer_qty`, `transfer_cost`).
- If you already have `streamlit_app.py`, you can remove or ignore it; the app entry here is `app.py`.
