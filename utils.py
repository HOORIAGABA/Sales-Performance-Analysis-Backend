import pandas as pd
import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ----------------- Validate Data ----------------------
def validate_sales_data(df: pd.DataFrame):
    required = {'employee_id', 'employee_name', 'dated', 'lead_taken', 'tours_booked',
                'applications', 'revenue_confirmed'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


# ----------------- LLM Prompt and API ----------------------
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def call_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)  # works for text-only generation
        return response.text
    except Exception as e:
        print(f"[Gemini ERROR] {e}")  # print in terminal
        return f"LLM Error: {str(e)}"


def generate_rep_prompt(rep_df: pd.DataFrame, name: str) -> str:
    total_leads = rep_df['lead_taken'].sum()
    total_apps = rep_df['applications'].sum()
    revenue = rep_df['revenue_confirmed'].sum()
    avg_close_rate = rep_df['avg_close_rate_30_days'].mean()
    tours_booked = rep_df['tours_booked'].sum()

    return (
        f"Analyze the performance of employee {name}.\n"
        f"Leads taken: {total_leads}\n"
        f"Tours booked: {tours_booked}\n"
        f"Applications: {total_apps}\n"
        f"Revenue Confirmed: ${revenue:.2f}\n"
        f"Average Close Rate (30 days): {avg_close_rate:.2f}%\n"
        f"Give detailed feedback on strengths, weaknesses, and recommendations."
    )


def generate_team_prompt(df: pd.DataFrame) -> str:
    total_leads = df['lead_taken'].sum()
    total_apps = df['applications'].sum()
    total_revenue = df['revenue_confirmed'].sum()
    top_performer = df.groupby("employee_name")['revenue_confirmed'].sum().idxmax()
    avg_deal = df['avg_deal_value_30_days'].mean()

    return (
        f"Analyze the overall performance of the sales team.\n"
        f"Total leads: {total_leads}\n"
        f"Total applications: {total_apps}\n"
        f"Total revenue: ${total_revenue:.2f}\n"
        f"Average deal value (30 days): ${avg_deal:.2f}\n"
        f"Top performer: {top_performer}\n"
        f"Provide team strengths, bottlenecks, and strategy suggestions."
    )


def generate_trends_prompt(df: pd.DataFrame, period: str) -> str:
    if period == "monthly":
        df['period'] = df['dated'].dt.to_period("M")
    else:
        df['period'] = df['dated'].dt.to_period("Q")

    grouped = df.groupby("period")['revenue_confirmed'].sum().reset_index()
    trends = "\n".join([f"{row['period']}: ${row['revenue_confirmed']:.2f}" for _, row in grouped.iterrows()])

    return (
        f"Analyze these sales revenue trends by {period}:\n{trends}\n"
        f"Identify growth or decline patterns, provide forecasting, and strategic insights."
    )
