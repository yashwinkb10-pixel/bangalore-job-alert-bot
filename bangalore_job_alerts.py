# bangalore_job_alerts.py
from telegram.ext import CommandHandler

import requests
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder
import schedule
import threading
import time
import asyncio
async def jobs(update, context):
    text = (
        "📊 *Today's Bangalore Job Summary*\n\n"
        "• Finance roles\n"
        "• Analytics roles\n"
        "• Data & high-paying positions\n\n"
        "📍 Location: Bangalore\n"
        "🏢 Companies: Top 50 companies in India\n\n"
        "⏰ Full detailed alerts are sent daily at *10 PM*.\n"
        "Stay tuned ✅"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# =============================
# 1️⃣ TELEGRAM DETAILS
# =============================
TELEGRAM_TOKEN = "8581528844:AAFK9_FvOgKTgGaZSxOCB4dqKuiEGIYcbO8"
CHAT_ID = " 8081752216"

# =============================
# 2️⃣ TOP COMPANIES (INDIA)
# =============================
COMPANIES = {
    "Deloitte": "https://www2.deloitte.com/in/en/careers/job-search.html",
    "Accenture": "https://www.accenture.com/in-en/careers/jobsearch",
    "Amazon": "https://www.amazon.jobs/en/locations/bangalore",
    "HSBC": "https://www.hsbc.com/careers",
    "JP Morgan": "https://careers.jpmorgan.com/global/en/home",
    "Goldman Sachs": "https://www.goldmansachs.com/careers",
    "Morgan Stanley": "https://www.morganstanley.com/people-opportunities",
    "EY": "https://www.ey.com/en_in/careers",
    "PwC": "https://www.pwc.in/careers.html",
    "KPMG": "https://kpmg.com/in/en/home/careers.html",
    "Flipkart": "https://www.flipkartcareers.com",
    "Microsoft": "https://careers.microsoft.com",
    "Google": "https://careers.google.com",
    "IBM": "https://www.ibm.com/careers"
}

# =============================
# 3️⃣ 100 KEYWORDS
# =============================
KEYWORDS = [
    "finance", "financial analyst", "fp&a", "accounting", "audit", "risk",
    "analytics", "data analyst", "business analyst", "strategy",
    "investment", "valuation", "equity", "treasury", "credit",
    "corporate finance", "management reporting", "forecasting",
    "budgeting", "pricing analyst", "market analyst", "research analyst",
    "data science", "data analytics", "business intelligence",
    "quantitative analyst", "financial modeling", "operations analyst",
    "finance associate", "finance executive", "cost analyst",
    "internal audit", "compliance", "portfolio analyst", "fund accounting",
    "capital markets", "investment banking", "corporate strategy",
    "performance analyst", "financial reporting", "MIS analyst",
    "revenue analyst", "growth analyst", "insights analyst",
    "commercial finance", "finance operations"
]

# =============================
# 4️⃣ SCRAPE COMPANY JOBS
# =============================
def fetch_company_jobs(company, url):
    jobs = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        for link in soup.find_all("a", href=True):
            title = link.get_text(strip=True)
            href = link["href"]

            if not title:
                continue

            text = title.lower()
            if any(k in text for k in KEYWORDS):
                if "bangalore" in text or "bengaluru" in text:
                    full_link = href if href.startswith("http") else url
                    jobs.append(f"{title} – {company}\n{full_link}")

        return jobs[:5]

    except:
        return []

# =============================
# 5️⃣ BUILD SUMMARY + JOB LIST
# =============================
def build_daily_message():
    finance = analytics = business = 0
    all_jobs = []

    for company, url in COMPANIES.items():
        jobs = fetch_company_jobs(company, url)

        for job in jobs:
            text = job.lower()
            if "finance" in text:
                finance += 1
            if "analytic" in text or "data" in text:
                analytics += 1
            if "business" in text or "strategy" in text:
                business += 1

        all_jobs.extend(jobs)

    if not all_jobs:
        return "📊 Bangalore Job Update\n\nNo relevant openings found today."

    message = (
        "📊 Bangalore Job Update (Today)\n\n"
        f"Summary:\n"
        f"• Finance roles: {finance}\n"
        f"• Analytics roles: {analytics}\n"
        f"• Business / High-paying roles: {business}\n\n"
        "📌 Openings (Apply links below):\n\n"
    )

    message += "\n\n".join(all_jobs[:15])
    return message

# =============================
# 6️⃣ SEND MESSAGE
# =============================
async def send_daily_alert(app):
    text = build_daily_message()
    await app.bot.send_message(chat_id=CHAT_ID, text=text)

# =============================
# 7️⃣ SCHEDULER (10 PM)
# =============================
def scheduler(app):
    schedule.every().day.at("22:00").do(
        lambda: asyncio.run_coroutine_threadsafe(send_daily_alert(app), app.loop)
    )
    while True:
        schedule.run_pending()
        time.sleep(60)

# =============================
# 8️⃣ START BOT
# =============================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("jobs", jobs))

    threading.Thread(target=scheduler, args=(app,), daemon=True).start()

    print("✅ Bangalore Job Alert Bot is running...")
    app.run_polling()

