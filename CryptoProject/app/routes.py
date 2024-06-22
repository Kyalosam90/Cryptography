from flask import Flask, request, jsonify, render_template 
import os
import sqlite3
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from twilio.rest import Client 
from .encryption import generate_key, encrypt_message, decrypt_message

app = Flask(__name__)
DATABASE = 'messages.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    plaintext = data['message'] # type: ignore
    to_number = data['to_number'] # type: ignore
    key = generate_key()
    ciphertext = encrypt_message(key, plaintext)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (ciphertext) VALUES (?)", (ciphertext,))
    conn.commit()
    
    otp = key.hex()
    send_otp_via_sms(to_number, otp)
    
    return jsonify({'status': 'Message sent and OTP sent via SMS'})

@app.route('/receive_message', methods=['POST'])
def receive_message():
    data = request.json
    otp = bytes.fromhex(data['otp']) # type: ignore
    message_id = data['message_id'] # type: ignore
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ciphertext FROM messages WHERE id = ?", (message_id,))
    row = cursor.fetchone()
    
    if row:
        ciphertext = row[0]
        plaintext = decrypt_message(otp, ciphertext)
        return jsonify({'message': plaintext})
    else:
        return jsonify({'error': 'Message not found'}), 404

def send_otp_via_sms(to_number, otp):
    account_sid = 'ACd24b5b4f6d9cd8993781c97951ada4a4'
    auth_token = 'e535b23538e462a5c3b6e7a130d34746'
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_='+13393090990',  # Replace with your Twilio number
            to=to_number
        )
        print("Message sent successfully")
        return message.sid
    except Exception as e:
        print(f"Failed to send message: {e}")
        return None
