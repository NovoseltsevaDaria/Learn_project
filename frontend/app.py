import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000"


@app.route("/")
def index():
    select_mode = request.args.get('select', 'false').lower() == 'true'
    response = requests.get(f"{API_URL}/rooms")
    if response.status_code == 200:
        rooms = response.json()
    else:
        rooms = []
    return render_template("list.html", rooms=rooms, select_mode=select_mode)


@app.route("/create", methods=["GET", "POST"])
def create_room():
    if request.method == "POST":
        data = {
            "room_number": int(request.form["room_number"]),
            "type": request.form["type"],
            "price_per_night": float(request.form["price_per_night"]),
            "is_available": "is_available" in request.form,
            "capacity": int(request.form["capacity"]),
            "description": request.form.get("description", ""),
            "has_washing_machine": "has_washing_machine" in request.form,
            "has_dishwasher": "has_dishwasher" in request.form
        }
        response = requests.post(f"{API_URL}/rooms", json=data)
        if response.status_code == 201:
            return redirect(url_for("index"))
        else:
            error = response.json().get("detail", "Ошибка при создании")
            return render_template("form.html", room=None, error=error)
    return render_template("form.html", room=None, error=None)


@app.route("/edit/<int:room_id>", methods=["GET", "POST"])
def edit_room(room_id):
    if request.method == "POST":
        data = {
            "room_number": int(request.form["room_number"]),
            "type": request.form["type"],
            "price_per_night": float(request.form["price_per_night"]),
            "is_available": "is_available" in request.form,
            "capacity": int(request.form["capacity"]),
            "description": request.form.get("description", ""),
            "has_washing_machine": "has_washing_machine" in request.form,
            "has_dishwasher": "has_dishwasher" in request.form
        }
        response = requests.put(f"{API_URL}/rooms/{room_id}", json=data)
        if response.status_code == 200:
            return redirect(url_for("index"))
        else:
            error = response.json().get("detail", "Ошибка при обновлении")
            return render_template("form.html", room=None, error=error)

    # GET запрос — загружаем данные номера
    response = requests.get(f"{API_URL}/rooms/{room_id}")
    if response.status_code == 200:
        room = response.json()
        return render_template("form.html", room=room, error=None)
    else:
        error = "Номер не найден"
        return render_template("form.html", room=None, error=error)


@app.route("/delete/<int:room_id>")
def delete_room(room_id):
    requests.delete(f"{API_URL}/rooms/{room_id}")
    return redirect(url_for("index"))


@app.route("/delete-selected", methods=["POST"])
def delete_selected():
    """Массовое удаление выбранных номеров"""
    selected_ids = request.form.getlist("selected_rooms")
    for room_id in selected_ids:
        requests.delete(f"{API_URL}/rooms/{room_id}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)