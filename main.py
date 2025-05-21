from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd
import os
from utils import (
    validate_sales_data,
    generate_rep_prompt,
    generate_team_prompt,
    generate_trends_prompt,
    call_gemini
)
import io

# ------------------- ENV SETUP ---------------------
load_dotenv()
app = FastAPI(title="Sales Performance Analysis with Gemini LLM")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- GLOBAL STATE ---------------------
sales_data = pd.DataFrame()


# ------------------- FILE UPLOAD ENDPOINT ---------------------
@app.post("/upload_sales_data")
async def upload_sales_data(file: UploadFile = File(...)):
    """
    ✅ Fulfills: Flexible Data Ingestion (CSV/JSON)
    """
    global sales_data
    contents = await file.read()

    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        elif file.filename.endswith(".json"):
            df = pd.read_json(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        validate_sales_data(df)
        df['dated'] = pd.to_datetime(df['dated'], errors='coerce')
        sales_data = df
        return {"message": f"Uploaded '{file.filename}' with {len(df)} records."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


@app.get("/")
async def health_check():
    return {"message": "Sales LLM API is running."}


# ------------------- INDIVIDUAL REP ENDPOINT ---------------------
@app.get("/api/rep_performance")
async def rep_performance(employee_id: int = Query(...)):
    """
    ✅ Fulfills: /api/rep_performance GET
    ✅ Fulfills: LLM-generated feedback for individual representative
    """
    if sales_data.empty:
        raise HTTPException(status_code=400, detail="No data uploaded.")

    rep_df = sales_data[sales_data["employee_id"] == employee_id]
    if rep_df.empty:
        raise HTTPException(status_code=404, detail="Employee not found.")

    employee_name = rep_df.iloc[0]['employee_name']
    prompt = generate_rep_prompt(rep_df, employee_name)
    feedback = call_gemini(prompt)

    return {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "feedback": feedback
    }


# ------------------- TEAM PERFORMANCE ENDPOINT ---------------------
@app.get("/api/team_performance")
async def team_performance():
    """
    ✅ Fulfills: /api/team_performance GET
    ✅ Fulfills: Team-wide analysis using LLM
    """
    if sales_data.empty:
        raise HTTPException(status_code=400, detail="No data uploaded.")

    prompt = generate_team_prompt(sales_data)
    feedback = call_gemini(prompt)
    return {"feedback": feedback}


# ------------------- TRENDS & FORECAST ENDPOINT ---------------------
@app.get("/api/performance_trends")
async def performance_trends(time_period: str = Query(..., description="monthly or quarterly")):
    """
    ✅ Fulfills: /api/performance_trends GET
    ✅ Fulfills: Trend analysis + LLM-based forecasting
    """
    if sales_data.empty:
        raise HTTPException(status_code=400, detail="No data uploaded.")
    if time_period not in ["monthly", "quarterly"]:
        raise HTTPException(status_code=400, detail="time_period must be 'monthly' or 'quarterly'")

    prompt = generate_trends_prompt(sales_data.copy(), time_period)
    feedback = call_gemini(prompt)
    return {"time_period": time_period, "feedback": feedback}
