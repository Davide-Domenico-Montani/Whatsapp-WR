import sys

# Leggi i dati dal terminale (passati dal server)
input_data = sys.argv[1] if len(sys.argv) > 1 else 'Nessun dato ricevuto'

# Esegui l'elaborazione necessaria (es. un semplice print)
output = f"Ricevuto: {input_data}. Elaborato Python!"

# Stampa il risultato (che verrà catturato dal server Node.js)
print(output)
