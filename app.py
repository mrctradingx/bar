# app.py
import os
import base64
import json
import time
from flask import Flask, render_template, request, redirect
from pdf417gen import encode, render_image
from PIL import Image
from io import BytesIO
import random
import string

app = Flask(__name__)
TICKETS = {}

def generate_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tokens = request.form.get("tokens").strip().split("\n")
        seats = [s.strip() for s in request.form.get("seats").strip().split("\n")]
        event_name = request.form.get("event_name").strip()
        event_time = request.form.get("event_time").strip()
        event_venue = request.form.get("event_venue").strip()

        ticket_id = generate_id()
        TICKETS[ticket_id] = []

        for i, token in enumerate(tokens):
            seat_info = seats[i] if i < len(seats) else f"Seat {i+1}"
            TICKETS[ticket_id].append({
                "token": token.strip(),
                "seat": seat_info,
                "event": event_name,
                "time": event_time,
                "venue": event_venue
            })

        return redirect(f"/ticket/{ticket_id}")

    return render_template("form.html")

@app.route("/ticket/<ticket_id>")
def show_ticket(ticket_id):
    ticket_data = TICKETS.get(ticket_id)
    if not ticket_data:
        return "Ticket not found", 404
    return render_template("ticket.html", tickets=ticket_data)

@app.route("/barcode/<token>")
def barcode(token):
    try:
        codes = encode(token, columns=6, security_level=5)
        image = render_image(codes)  # returns PIL Image
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return app.response_class(buffer, mimetype='image/png')
    except Exception as e:
        return f"Error generating barcode: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
