from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

#lista cu jucatorii, tuplu, set cu hartile preferate ale jucatorului si dictionar in care stocam jucatorii si informatiile acestora
user_list = []
rank_levels = [str(i) for i in range(1, 11)]
available_maps = {"Mirage", "Ancient", "Anubis", "Dust2", "Inferno", "Train"}
user_data = {}


def register_user(username, rank, maps):
    if username in user_data:
        return "⚠️ Jucatorul deja exista!"
    if rank not in rank_levels:
        return "⚠️ Rank-ul nu este valid!"
    if not maps.issubset(available_maps):
        return "⚠️ Una sau mai multe harti nu sunt valide!"

    user_data[username] = {"rank": rank, "maps": maps}
    user_list.append(username)
    return f"✅ {username} a fost înregistrat cu succes!"

def find_match(username):
    if username not in user_data:
        return None

    user_rank = user_data[username]["rank"]
    user_maps = user_data[username]["maps"]

    for other_user in user_list:
        if other_user == username:
            continue
        other_rank = user_data[other_user]["rank"]
        other_maps = user_data[other_user]["maps"]
        if user_rank == other_rank and not user_maps.isdisjoint(other_maps):
            return other_user
    return None

def save_to_csv():
    with open("users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Rank", "Maps"])
        for user in user_list:
            data = user_data[user]
            maps_str = ", ".join(data["maps"])
            writer.writerow([user, data["rank"], maps_str])

def load_from_csv():
    try:
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                username = row[0]
                rank = row[1]
                maps = set(row[2].split(", "))
                user_list.append(username)
                user_data[username] = {"rank": rank, "maps": maps}
    except FileNotFoundError:
        pass


#Rute flask

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    match = None

    if request.method == "POST":
        action = request.form["action"]

        if action == "register":
            username = request.form["username"]
            rank = request.form["rank"]
            maps = set(request.form.getlist("maps"))
            message = register_user(username, rank, maps)

        elif action == "match":
            username = request.form["username"]
            match = find_match(username)
            if not match:
                message = "❌ Nu am găsit un meci potrivit."

        elif action == "save":
            save_to_csv()
            message = "💾 Datele au fost salvate."

        elif action == "load":
            load_from_csv()
            message = "📂 Datele au fost încărcate."

    return render_template("index.html", ranks=rank_levels, maps=available_maps, message=message, match=match)

if __name__ == "__main__":
    app.run(debug=True)