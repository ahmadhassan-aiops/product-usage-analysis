# What really happened to product usage in January 2023?

**Live app:** [solution-usage-analysis.streamlit.app](https://solution-usage-analysis.streamlit.app/) · **Notebook and project folder:** [AIOPS-Portfolio-Projects](https://github.com/ahmadhassan-aiops/AIOPS-Portfolio-Projects/tree/main/1.%20Data-analysis-with-python-Projects/Usage_Analysis_of_Customers)

An interactive analysis by **Ahmad Hassan** (AI Engineer) of a software product's usage logs: 100 customers,
six features, June 2017 to January 2023. The question was why usage looked weak in January 2023.

- **Key findings**: January 2023 was the lowest January in the data, but the fall began in June 2022, when the
  Roadmap feature lost half its usage; no unusual group of customers is behind it.
- **Usage over time**: monthly minutes, sessions and active customers; every January compared; year-on-year change.
- **Features**: what each feature contributed to the change, feature trends, time per session.
- **Customers**: each customer against their own history, and how often such dips happen in a normal month.
- **Data & method**: preparation, anonymisation, how each question was answered, and limits.

Notebook: [AIOPS-Portfolio-Projects / Usage_Analysis_of_Customers](https://github.com/ahmadhassan-aiops/AIOPS-Portfolio-Projects/tree/main/1.%20Data-analysis-with-python-Projects/Usage_Analysis_of_Customers)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Rebuild the data: `python build_data.py "path/to/Usage_Analysis_of_Customers"` (folder with `usage_data.csv`).
Usernames are replaced with neutral customer labels during the build.

Structure: `app.py` (entry), `nav.py` (pages), `views/` (one module per page), `lib/` (data loading, charts, UI),
`build_data.py` (CSV to Parquet), `data/` (shipped with the app), `Dockerfile` (port 7860).
