from pathlib import Path


# Legge il file CSV degli studenti e restituisce una lista di dizionari.
def leggi_studenti(nome_file):
    percorso = Path(__file__).with_name(nome_file)
    studenti = []

    with percorso.open("r", encoding="utf-8") as file:
        # La prima riga è l'intestazione: la ignoro.
        next(file, None)

        for riga in file:
            riga = riga.strip()
            if not riga:
                continue

            # Divido la riga in 5 campi: ID, cognome, nome, classe, media
            id_str, cognome, nome, classe, media_str = [campo.strip() for campo in riga.split(",")]

            # Converto i dati dal tipo stringa a quello giusto.
            studente = {
                "id": int(id_str),
                "cognome": cognome,
                "nome": nome,
                "classe": classe,
                "media": float(media_str),
            }

            # Aggiungo lo studente nella lista.
            studenti.append(studente)

    return studenti


# Legge il file con le richieste e restituisce tre informazioni:
# lista di ID, cognome da cercare e classe da analizzare.
def leggi_richieste(nome_file):
    percorso = Path(__file__).with_name(nome_file)

    with percorso.open("r", encoding="utf-8") as file:
        righe = [riga.strip() for riga in file if riga.strip()]

    if len(righe) != 3:
        raise ValueError("Il file richieste.txt deve contenere esattamente 3 righe.")

    # Prima riga: "103,107,115,110" -> lista di numeri interi
    id_richiesti = [int(x.strip()) for x in righe[0].split(",") if x.strip()]
    cognome = righe[1]
    classe = righe[2]

    return id_richiesti, cognome, classe


# Cerca uno studente per ID.
def cerca_per_id(studenti, id_da_cercare):
    for studente in studenti:
        if studente["id"] == id_da_cercare:
            return studente
    return None


# Stampa un singolo studente nel formato richiesto.
def stampa_studente(studente):
    print(f"{studente['id']} {studente['cognome']} {studente['nome']} {studente['classe']} {studente['media']}")


# Programma principale.
def main():
    # Carico i dati degli studenti.
    studenti = leggi_studenti("studenti.csv")
    id_richiesti, cognome_richiesto, classe_richiesta = leggi_richieste("richieste.txt")

    # 1) Ricerca per ID
    print("--- Ricerca per ID ---")
    for id_corrente in id_richiesti:
        studente = cerca_per_id(studenti, id_corrente)
        if studente is None:
            print(f"ID {id_corrente} non trovato")
        else:
            stampa_studente(studente)
    print()

    # 2) Ricerca per cognome, ignorando maiuscole/minuscole
    print(f"--- Ricerca per cognome: {cognome_richiesto} ---")
    trovati = [
        studente for studente in studenti
        if studente["cognome"].lower() == cognome_richiesto.lower()
    ]

    if trovati:
        for studente in trovati:
            stampa_studente(studente)
    else:
        print("Nessuno studente trovato")
    print()

    # 3) Calcolo della media della classe
    print(f"--- Media della classe {classe_richiesta} ---")
    studenti_classe = [
        studente for studente in studenti
        if studente["classe"] == classe_richiesta
    ]

    if not studenti_classe:
        print(f"Nessuno studente nella classe {classe_richiesta}")
    else:
        somma = sum(studente["media"] for studente in studenti_classe)
        media = somma / len(studenti_classe)
        print(f"Studenti considerati: {len(studenti_classe)}")
        print(f"Media: {media:.2f}")


if __name__ == "__main__":
    main()
