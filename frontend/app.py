from idlelib.iomenu import errors

import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
APIURL = 'http://127.0.0.1:5000/api'

@app.route('/')
def index():
    """Главная страница"""
    response = requests.get(f"{APIURL}/rooms")
    if response.status_code == 200:
        rooms = response.json()
    else:
        rooms = []
    return render_template("list.html", rooms=rooms)

@app.route('/create', methods=['GET','POST'])
def create_room():
    """Создание нового номера"""
    if request.method == 'POST':
        data = {
            "room_number": int(request.form['room_number']),
            "type": request.form['type'],
            "price_per_night": float(request.form['price_per_night']),
            "is_available": "is_available" in request.form,
            "capacity": int(request.form['capacity']),
            "description": request.form.get('description', "")
        }

        response = requests.post(f"{APIURL}/rooms", json=data)
        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            error = response.json().get("detail", "Ошибка при создании")
            return render_template("form.html", room=None, error=error)

        # GET запрос - показываем пустую форму
        return render_template("form.html", room=None, error=None)

@app.route('/edit/int:room_id>', methods=['GET','POST'])
def edit_room(room_id):
    """Редактирование номера"""
    if request.method == 'POST':
        data = {
            "room_number": int(request.form['room_number']),
            "type": request.form['type'],
            "price_per_night": float(request.form['price_per_night']),
            "is_available": "is_available" in request.form,
            "capacity": int(request.form['capacity']),
            "description": request.form.get('description', "")
        }

        response = requests.put(f"{APIURL}/rooms/{room_id}", json=data)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            error = response.json().get("detail", "Ошибка при обновлении")
            return render_template("form.html", room=None, error=error)

        # GET запро - загружаем данные номера для редактирования
        response = requests.get(f"{APIURL}/rooms/{room_id}")
        if response.status_code == 200:
            room = response.json()
        else:
            room = None
            error = "Номер не найден"
            return render_template("form.html", room = None, error = error)

        return render_template("form.html", room = room, error=None)

    @app.route('/delete/<int:room_id>')
    def delete_room(room_id):
        """Удаление номера"""
        requests.delete(f"{APIURL}/rooms/{room_id}")
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run(debug=True, port = 5000)


