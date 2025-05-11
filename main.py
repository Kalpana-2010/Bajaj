import os
import requests
from dotenv import load_dotenv

load_dotenv()

name = os.getenv("NAME")
reg_no = os.getenv("REG_NO")
email = os.getenv("EMAIL")

generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
payload = {
    "name": name,
    "regNo": reg_no,
    "email": email
}

try:
    print("Sending request to generate webhook...")
    res = requests.post(generate_url, json=payload)
    res.raise_for_status()
    data = res.json()
    webhook_url = data["webhook"]
    access_token = data["accessToken"]
    print("Webhook generated successfully.")
except Exception as e:
    print("Failed to generate webhook:", e)
    exit(1)

last_digit = int(reg_no[-1])
if last_digit % 2 == 0:
    question_url = "https://drive.google.com/file/d/1PO1ZvmDqAZJv77XRYsVben11Wp2HVb/view?usp=sharing"
else:
    question_url = "https://drive.google.com/file/d/1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY/view?usp=sharing"

print(f"Download your SQL question from:\n{question_url}")

# ==== STEP 3: Load SQL Query ====
try:
    with open("solution.sql", "r") as f:
        final_query = f.read().strip()
    if not final_query:
        raise ValueError("solution.sql is empty.")
except Exception as e:
    print("Error reading SQL solution:", e)
    exit(1)

# ==== STEP 4: Submit Final SQL Query ====
submit_url = "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
body = {
    "finalQuery": final_query
}

try:
    print("Submitting final SQL query...")
    submit_res = requests.post(submit_url, headers=headers, json=body)
    submit_res.raise_for_status()
    print("Submission successful!")
    print("Response:", submit_res.json())
except Exception as e:
    print("Submission failed:", e)