from flask import Flask, render_template, request, redirect, url_for
from barcode import generate_barcode_image
import uuid

app = Flask(__name__)

tickets = []

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        token = request.form["token"]
        event_name = request.form["event_name"]
        date = request.form["date"]
        section = request.form["section"]
        row = request.form["row"]
        seat = request.form["seat"]
        tid = str(uuid.uuid4())[:8]
        tickets.append({
            "id": tid,
            "token": token,
            "event_name": event_name,
            "date": date,
            "section": section,
            "row": row,
            "seat": seat
        })
        return redirect(url_for("ticket", ticket_id=tid))
    return render_template("form.html")

@app.route("/ticket/<ticket_id>")
def ticket(ticket_id):
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        return "Ticket not found", 404
    barcode_img = generate_barcode_image(ticket["token"])
    return render_template("ticket.html", ticket=ticket, barcode_img=barcode_img)

if __name__ == "__main__":
    app.run(debug=True)
