
# HealthKart Influencer Campaign Dashboard

## 📦 Files & Assumptions

This dashboard uses 4 CSV files with the following schemas:

1. **influencers.csv**
   - Columns: `influencer_id`, `name`, `category`, `gender`, `follower_count`, `platform`

2. **posts.csv**
   - Columns: `influencer_id`, `platform`, `date`, `url`, `caption`, `reach`, `likes`, `comments`

3. **tracking_data.csv**
   - Columns: `source`, `campaign`, `influencer_id`, `user_id`, `product`, `date`, `orders`, `revenue`

4. **payouts.csv**
   - Columns: `influencer_id`, `basis`, `rate`, `payout_orders`, `total_payout`

## ✅ Assumptions

- All monetary values are in INR.
- ROAS is calculated as `revenue / total_payout`.
- ROI is calculated as `(revenue - payout) / payout`.
- `orders` in `tracking_data.csv` refers to total converted orders.
- `total_payout` is precomputed in the payouts file based on `rate * orders` (or per post if basis is 'post').
- Influencer ranking starts at 1 for better readability.

## ⚙️ Setup Instructions

1. Clone or download this project.
2. Install required libraries:

```bash
pip install streamlit pandas plotly fpdf
```

3. Run the dashboard:

```bash
streamlit run app.py
```

4. Upload all 4 CSV files via the sidebar.
5. Explore KPIs, top influencers, post engagement, poor ROI warnings.
6. Export insights as CSV and PDF.

---
(c) 2025 HealthKart Data Team
