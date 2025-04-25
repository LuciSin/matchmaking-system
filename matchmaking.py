'''
Atentie!
Acesa este primul draft al unui sistem de matchmaking pentru gameri.
Am incercat sa creez un sistem de matchmaking pentru gameri, care sa fie cat mai simplu si usor de folosit.
Am folosit un dictionar pentru a stoca datele utilizatorilor, un set pentru a verifica hartile preferate si o lista pentru a stoca numele utilizatorilor.
Am implementat o functie de inregistrare a utilizatorilor, care verifica daca numele utilizatorului este deja inregistrat, daca rank-ul este valid si daca hartile preferate sunt valide.
Acest cod este primul draft si nu are o intefata UI, pentru interfata UI am folosit flask, va rog sa vedeti app.py, acolo am implementat interfata UI.
'''


# Sistem de matchmaking pentru gameri.

#lista cu jucatorii (utilizatori)
user_list = []
#tuplu pt rank-urile disponibile
rank_levels = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
#set cu harta preferata a jucatorului
available_maps = {"Mirage", "Ancient", "Anubis", "Dust2", "Inferno", "Train"}

#un dictionar in care stocam toti jucatorii si informatiile acestora
#ex utiliare: user_data["lucaseen"] = {"rank": "1", "maps": {Mirage, Dust2}}
user_data = {}

#functia de adaugare jucator
def register_user(username, rank, maps):
    # verificam daca exista numele deja
    if username in user_data:
        print("⚠️ Jucatorul deja exista!")
        return False

    # verificam daca rankul este unul valid
    if rank not in rank_levels:
        print("⚠️ Rank-ul nu este valid!")
        return False

    # verificam daca toate hartile introduse sunt valide
    if not maps.issubset(available_maps):
        print("⚠️ Una sau mai multe harti nu sunt valide!")
        return False

    # salvam datele
    user_data[username] = {"rank": rank, "maps": maps}
    user_list.append(username)
    print(f"✅ {username} a fost înregistrat cu succes!")
    return True

# =====================
# TEST RAPID 
# =====================

#testam functia cu un un input valid
register_user("lucaseen", "10", {"Mirage", "Dust2"})
#testam sa adaugam un utilizator cu acelasi nume
register_user("lucaseen", "3", {"Train", "Anubis"})
#testma functia ccu un input invalid (rank ul nu este disponibil)!
register_user("lucaseen", "3", {"Train", "Anubis"})


#Functia propriu-zisa de matchmaking
def find_match(username):
    #verificam daca userul exista
    if username not in user_data:
        print("Utilizator inexistent")
        return None
    
    user_rank = user_data[username]["rank"]
    user_maps = user_data[username]["maps"]
    
    for other_user in user_list:
        if other_user == username:
            continue #sarim peste cel curent

        other_rank = user_data[other_user]["rank"]
        other_maps = user_data[other_user]["maps"]

        #verificam daca rankurile sunt la fel (as incerca sa fie apropiate dar inca nu am gasit o solutie) si daca au harti comune
        if user_rank == other_rank and not user_maps.isdisjoint(other_maps):
            return other_user
        
    return None
#test rapid
register_user("Player2", "10", {"Mirage"})
print(find_match("lucaseen"))  # Ar trebui sa returneze player 2

#salvare si incarcare csv

import csv

def save_to_csv():
    with open("users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Rank", "Maps"])
        for user in user_list:
            data = user_data[user]
            maps_str = ", ".join(data["maps"])
            writer.writerow([user, data["rank"], maps_str])
        print("datele au fost salvate")

def load_from_csv():
    try:
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Sărim peste antet
            for row in reader:
                username = row[0]
                rank = row[1]
                maps = set(row[2].split(", "))
                user_list.append(username)
                user_data[username] = {"rank": rank, "maps": maps}
        print("datele dvs au fost incarcate")
    except FileNotFoundError:
        print("din pacate fisierul dvs nu a fost gasit oh nu")

#meniuri interactive cu if, elif si while

def main_menu():
    while True:
        print("\n Matchmaking System 🎮")
        print("1. Inregistreaza un nou jucator")
        print("2. Cauta un alt jucator")
        print("3. Salveaza datele")
        print("4. Incarca datele")
        print("5. Iesire...")

        try:
            opt = int(input("Alege o optiune: "))
        except ValueError:
            print("Introdu un numar valid:")
            continue

        if opt == 1:
            name = input("Nume: ")
            rank = input(f"Rank ({', '.join(rank_levels)}): ")
            maps_input = input("Harti preferate (de exemplu Mirage, Inferno, etc): ")
            maps = set(maps_input.split(", "))
            register_user(name, rank, maps)

        elif opt == 2:
            name = input("Numele tau: ")
            match = find_match(name)
            if match:
                print(f"🎯 Match found: {match}!")
            else:
                print("❌ Din pacate nu am gasit un utilizator potrivit, incearca mai tarziu.")
        elif opt == 3:
            save_to_csv()
        elif opt == 4:
            load_from_csv()
        elif opt == 5:
            print("La revedere!")
            break
        else:
            print("OPTIUNE INVALIDA.")
        
main_menu()
#probleme pe care le am si inca nu stiu cum sa le rezolv: 
#1. poti adauga date la infinit si sa spamezi csv-ul cu noi intrari asemanatoare
#2. chiar daca gresesti la un anumit pas, eroarea o primesti tocmai la final 
#3. momentan algoritmul este unul exagerat de simplu, jucatorul gasit este ales in ordinea alfabetica daca respecta conditia rank-ului (o solutie aici ar fi sa implementez
#un scor de potrivire, adica un algoritm care cauta cat mai multe harti in comun si o diferenta de rank cat mai mica, dar momentan e hard-coded, totusi e un proiect care m-a
#ajutat sa inteleg mult mai bine cum functioneza anumite aspecte din python.)