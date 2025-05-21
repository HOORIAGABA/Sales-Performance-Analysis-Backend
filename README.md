# Sales Performance Analysis Backend (Powered by Gemini LLM)


![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Framework](https://img.shields.io/badge/FastAPI-Modern%20Python%20API-brightgreen)

This FastAPI application provides automated insights and strategic recommendations for sales teams using structured CSV/JSON data. It leverages Google Gemini (1.5 Flash) to generate human-like analytical feedback.

---

## Features

Upload sales data via CSV or JSON  
Analyze individual sales representative performance  
Evaluate overall team performance  
Generate monthly or quarterly trend forecasts  
Feedback powered by **Google Gemini LLM**

---

## File Structure


```
SALES_ANALYSIS_BACKEND/
├── main.py
├── utils.py
├── sales_data.csv
├── requirements.txt
├── .env
└── README.md
```

---

## Tech Stack

- **FastAPI** - Web framework for REST APIs
- **Pandas** - Data manipulation and transformation
- **Google Generative AI (Gemini)** - LLM for dynamic feedback
- **Uvicorn** - ASGI server
- **Python 3.10+**
- **dotenv** - For managing API secrets

---

## Setup Instructions

### 1. **Clone the repo**
   
   ```
   git clone <https://github.com/HOORIAGABA/Sales-Performance-Analysis-Backend>
   cd SALES_ANALYSIS_BACKEND
   ```

### 2. **Create virtual environment**

   ```
   python -m venv venv
   venv\Scripts\activate # on Windows
   ```

### 3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

### 4. **Create .env file**

```
GEMINI_API_KEY=your_google_generative_ai_key_here
```

### 5. **Run the server**

```
uvicorn main:app --reload
```

---

## API Endpoints

 **Upload Sales Data**
   `POST /upload_sales_data`

   - Accepts .csv or .json files
   - Validates schema and stores data in-memory

## Individual Rep Performance
   `GET /api/rep_performance?employee_id=8`

   - Returns LLM-generated feedback for the selected employee

## Team Performance
   `GET /api/team_performance`

   - Provides team-wide analysis, strengths, bottlenecks & strategies

## Sales Trends
   `GET /api/performance_trends?time_period=monthly`
   or
   `GET /api/performance_trends?time_period=quarterly`

   - Performs temporal analysis and returns a detailed LLM forecast

---

## Notes
- Model used: gemini-1.5-flash (text-only generation)

- Make sure your Gemini API quota is not exceeded during usage

- Errors and API feedback are gracefully handled and returned

---

## Required CSV Columns
Uploaded data must include the following fields:

employee_id, employee_name, dated, lead_taken, tours_booked, 
applications, revenue_confirmed, avg_close_rate_30_days, avg_deal_value_30_days

---

## Final Remarks
This project demonstrates practical integration of LLMs into business analytics for automated reasoning, insights, and strategy generation. Ideal for enterprise sales analytics platforms, marketing teams, and decision-making tools.

---

## License
MIT License

---

