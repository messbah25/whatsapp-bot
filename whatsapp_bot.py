from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from google.oauth2.service_account import Credentials

# Setup Flask
app = Flask(__name__)

@app.route("/")  
def home():
    return "Flask server is running!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "Webhook is active!"
    elif request.method == "POST":
        data = request.json  # Ambil data dari request
        print("Received data:", data)  # Debugging
        return {"status": "success", "message": "Data received"}, 200

# Setup Google Sheets API (Pindahkan ke dalam fungsi agar lebih aman)
def connect_to_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("C:/Users/MIsbahul Munir/Downloads/corded-sunup-450702-g2-de860d4b07d3.json", scopes=scope)
    client = gspread.authorize(creds)
    return client.open("cobachatbot").sheet1

@app.route("/bot", methods=["POST"])
def bot():
    sheet = connect_to_sheets()  # Inisialisasi saat fungsi dipanggil
    incoming_msg = request.form.get("Body", "").strip()  # Gunakan request.form untuk Twilio
    sender = request.form.get("From")

    response = MessagingResponse()
    msg = response.message()

    if incoming_msg.lower() == "data":
        data = sheet.get_all_records()
        if data:
            reply_text = "\n".join([f"{row['Nama']} - {row['Nomor HP']} - {row['Kota']}" for row in data])
        else:
            reply_text = "Data Google Sheets kosong."
    else:
        reply_text = "Ketik 'data' untuk melihat isi Google Sheets."

    msg.body(reply_text)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
