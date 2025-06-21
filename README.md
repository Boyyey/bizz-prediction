# Dynamic Pricing Engine

**Short Description:**
A modern, user-friendly desktop app that uses AI to suggest the best prices for your products based on demand, time, and competitor data. Built with Python and PyQt5, it features a beautiful dark UI and requires no coding skills to use.

![Dynamic Pricing Engine Banner](https://img.shields.io/badge/Pricing%20AI-Dark%20Mode-blue)

A beautiful, modern desktop app for AI-powered dynamic pricing. Suggests the best price for a product based on demand, time, and competitors. Built with Python, PyQt5, and scikit-learn.

---

## ✨ Features
- **Modern dark UI** inspired by popular apps
- **Upload your own CSV** or use sample data
- **AI price suggestions** using regression
- **Competitor price scraping** (demo)
- **Download results** as CSV
- **No coding required** for end users

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-github-username/dynamic-pricing-engine.git
cd dynamic-pricing-engine
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python main_qt.py
```

---

## 📝 Usage
- Click **Upload CSV** to load your data, or use the sample provided.
- (Optional) Enter competitor URLs and click **Scrape Competitor Prices**.
- Click **Suggest Prices** to get AI-powered price suggestions.
- Download your results as CSV.

---

## 📦 Project Structure
```
dynamic_pricing_engine/
├── main_qt.py            # PyQt5 GUI app
├── app.py                # (Optional) Streamlit app
├── model/
│   └── regression.py     # Regression model
├── scraper/
│   └── competitor_scraper.py # Competitor price scraper
├── data/
│   └── data_loader.py    # Data loading utilities
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🤖 Tech Stack
- Python 3.8+
- PyQt5
- scikit-learn
- pandas, numpy
- requests, beautifulsoup4

---

## 💡 Business Value
Maximizes revenue and competitiveness by suggesting optimal prices based on real data and market conditions.

---

