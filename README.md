# 📊 IT Job Market Dashboard — Gujarat, India

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8+-11557c?style=for-the-badge&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13+-4c8cbf?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

> ⚠️ **Educational Purpose Only** — Data is synthetically simulated.
> Built as part of my **Final Year B.Tech Engineering Internship.**

</div>

---

## 📌 About This Project

This is a **Streamlit web dashboard** I built as a second project on top of
my main [IT Job Market Analysis](https://github.com/Jayr1612/it-market-job-data-analysis)
project.

The idea was simple — I had already collected and analysed **6,647 IT job
listings** from Gujarat, India. Instead of keeping those insights locked inside
a Jupyter notebook, I wanted to make them accessible to anyone through an
**interactive web interface** — with live filters, clickable charts, and a
searchable data table.

No web development experience was needed. **Streamlit converts Python code
directly into a web application.**

---

## 🔗 Part of a 2-Project Series

| Project | What it does |
|---------|-------------|
| [📊 IT Job Market Analysis](https://github.com/Jayr1612/it-market-job-data-analysis) | Data scraping, cleaning, EDA, 16 charts |
| **📈 IT Job Market Dashboard** ← You are here | Interactive web dashboard using that data |

---

## 🌐 What is Streamlit?

Streamlit is an **open-source Python library** that lets you build interactive
web apps using only Python — no HTML, CSS, or JavaScript needed.

```python
# Normal Python (Jupyter / script)
import matplotlib.pyplot as plt
plt.bar(cities, counts)
plt.show()          # shows a static chart

# With Streamlit (becomes a web app!)
import streamlit as st
city = st.selectbox('Select City', ['Surat', 'Ahmedabad'])
st.bar_chart(data[data['city'] == city])
# → dropdown appears in browser, chart updates live!
```

Think of it like turning your data analysis notebook into a website that
anyone can use — without knowing any web development.

---

## 🎛️ Dashboard Features

| Section | What It Shows |
|---------|--------------|
| **Sidebar Filters** | Filter by City, Portal, Job Type, Domain |
| **KPI Cards** | Total jobs, portals, internships, median salary |
| **City Distribution** | Bar chart — jobs per city |
| **Portal Comparison** | Bar chart — jobs per portal |
| **Domain Trends** | Top 15 IT domains ranked |
| **City × Domain Heatmap** | Which domain is hot in which city |
| **Job Type Donut** | Full-time vs Internship vs Contract split |
| **Top 25 Skills** | Most demanded tech skills |
| **Salary Boxplots** | Salary distribution by city and domain |
| **Experience Distribution** | Fresher to principal level breakdown |
| **Top 15 Companies** | Most active hiring companies |
| **Jobs Over Time** | Daily posting trend with 7-day average |
| **Insight Cards** | Top city, domain, skill, internship count |
| **Data Table** | Searchable table + CSV download button |

---

## 📊 Dataset Used

| Detail | Value |
|--------|-------|
| **Total Records** | 6,647 |
| **Cities** | Surat · Ahmedabad · Vadodara · Gandhinagar |
| **Portals** | Naukri · LinkedIn · Indeed · Glassdoor · Internshala |
| **IT Domains** | 20 |
| **Internships** | 1,078 |
| **Median Salary** | ₹7.6 LPA |
| **Date Range** | Last 90 days |

Dataset collected and processed in the
[main analysis project](https://github.com/Jayr1612/it-market-job-data-analysis).

---

## 🛠️ Tools & Libraries Used

### Streamlit
- Main framework for building the web dashboard
- Handles UI components — dropdowns, sliders, buttons, tables
- Converts Python code into a browser-accessible web app
- `st.sidebar` for filters, `st.metric` for KPI cards,
  `st.dataframe` for tables

### Pandas
- Loads the CSV dataset into a DataFrame
- Applies filters based on sidebar selections
- Groups and aggregates data for each chart
- Powers the searchable data table

### Matplotlib
- Core chart library used for all visualizations
- Bar charts, box plots, line charts, histograms
- Configured with `Agg` backend for Streamlit compatibility

### Seaborn
- Built on top of Matplotlib for better-looking charts
- Used for heatmaps (`sns.heatmap`) and colour palettes
- Makes the City × Domain heatmap and salary charts

### NumPy
- Numerical operations behind the charts
- Handles NaN values in salary and experience columns

---

## 📁 Project Structure

```
it-job-market-dashboard/
│
├── dashboard.py               ← Main Streamlit app
├── final_merged_jobs.csv      ← Dataset (6,647 records)
├── requirements.txt           ← All dependencies
├── .gitignore                 ← Python gitignore
└── README.md                  ← This file
```

---

## 🚀 How to Run Locally

### Step 1 — Clone the repo
```bash
git clone https://github.com/Jayr1612/it-job-market-dashboard.git
cd it-job-market-dashboard
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the dashboard
```bash
streamlit run dashboard.py
```

### Step 4 — Open in browser
```
http://localhost:8501
```

Browser usually opens automatically. If not — copy the URL above manually.

---

## 💡 How the Filtering Works

When you select a filter in the sidebar — for example **City = Surat** —
the dashboard filters the entire dataset and all 10+ charts update
simultaneously:

```python
# Sidebar selection
sel_cities = st.multiselect('City', ['Surat','Ahmedabad',...])

# Filter applied to full dataset
df = df_raw[df_raw['city'].isin(sel_cities)]

# All charts use the filtered df automatically
city_counts = df['city'].value_counts()
```

This is the main advantage of Streamlit over a static notebook — everything
is reactive and updates in real time.

---

## 📸 Dashboard Preview

### KPI Cards + City Distribution
> Charts auto-generate when you run the app locally

### City × Domain Heatmap
> Shows which IT domain is most active in each city

### Salary Analysis
> Boxplots comparing salary across cities and top domains

---

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `FileNotFoundError` | Make sure CSV is in the same folder |
| Browser doesn't open | Go to `http://localhost:8501` manually |
| Port already in use | Run `streamlit run dashboard.py --server.port 8502` |
| Blank white screen | Wait 10 seconds and refresh the page |

---

## ⚠️ Educational Disclaimer

```
This project was made for learning and internship portfolio purposes.
All data is synthetically generated — not real job market data.
Streamlit dashboard is built for demonstration of data visualization skills.
Part of Final Year B.Tech Engineering Internship project.
```

---

## 👨‍💻 Author

**Jayr — Final Year B.Tech Student**
**Computer Science / Information Technology**

- 🐙 GitHub: [@Jayr1612](https://github.com/Jayr1612)
- 📊 Main Project: [IT Job Market Analysis](https://github.com/Jayr1612/it-market-job-data-analysis)

---

<div align="center">

*Made with ❤️ — Gujarat, India 🇮🇳*

⭐ Star this repo if you found it useful!

</div>
