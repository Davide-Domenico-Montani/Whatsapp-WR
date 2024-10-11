##in input i dati inseriti dallla persona
import zipfile
import os
import re
import pandas as pd
zip_file_path = r"C:\Users\david\Desktop\test\uploads"

# Cerca il primo file ZIP nella cartella
zip_files = [f for f in os.listdir(zip_file_path) if f.endswith('.zip')]

if not zip_files:
    print("Nessun file ZIP trovato nella cartella.")
    exit()

# Prendi il primo file ZIP
zip_file_path = os.path.join(zip_file_path, zip_files[0])
print(f"Primo file ZIP trovato: {zip_file_path}") 

# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # List all files in the ZIP archive
    file_list = zip_ref.namelist()
    print("Files in the ZIP:", file_list)

    # Access and read the first file in the list
    file_to_read = file_list[0]  # Assuming you want to read the first file

    # Read the file content without extracting
    with zip_ref.open(file_to_read) as f:
        content = f.read().decode('utf-8')  # Adjust decoding based on the file type


#in content c'è la chat giusta
pattern = r"(\d{2}/\d{2}/\d{2}), (\d{2}):\d{2} - ([^:]+): (.+)"

# Variabili per i dati
data = []
ora = []
mittente = []
contenuto = []
lines = content.split('\n')

# Processa ogni riga
for line in lines:
    match = re.match(pattern, line)
    if match:
        # Estrai le variabili
        data.append(match.group(1))
        ora.append(match.group(2))  # Solo l'ora, senza i minuti
        mittente.append(match.group(3))
        contenuto.append(match.group(4))

df = pd.DataFrame({
    'Data': data,
    'Ora': ora,
    'Mittente': mittente,
    'Contenuto': contenuto
})

# Mostra il DataFrame

#da qua in poi esempio di analisi testuale:

#ora ciclo per vedere il giorno con piu messaggi 

messaggi_per_giorno = df.groupby('Data').size().reset_index(name='Totale_Messaggi')

# Trova il giorno con il massimo numero di messaggi
giorno_con_piu_messaggi = messaggi_per_giorno.loc[messaggi_per_giorno['Totale_Messaggi'].idxmax()]

# Mostra il risultato
print(f"Giorno con più messaggi: {giorno_con_piu_messaggi['Data']}, Totale messaggi: {giorno_con_piu_messaggi['Totale_Messaggi']}")


def determina_momento(ora):
    ora_int = int(ora.split(':')[0])  # Estrae l'ora come intero
    if 6 <= ora_int < 12:
        return 'Mattina'
    elif 12 <= ora_int < 18:
        return 'Pomeriggio'
    elif 18 <= ora_int < 23:
        return 'Sera'
    else:
        return 'Notte'

# Aggiungi la colonna 'Momento' al DataFrame
df['Momento'] = df['Ora'].apply(determina_momento)

messaggi_per_ora = df.groupby('Momento').size().reset_index(name='Totale_Messaggi_ora')

# Trova l'ora con il massimo numero di messaggi
ora_con_piu_messaggi = messaggi_per_ora.loc[messaggi_per_ora['Totale_Messaggi_ora'].idxmax()]

# Mostra il risultato
print(f"Momento con più messaggi: {ora_con_piu_messaggi['Momento']}")


#ora persona piu attiva
persona_p_mex=df.groupby('Mittente').size().reset_index(name='Totale_Messaggi_pers')

p_con_piu_messaggi = persona_p_mex.loc[persona_p_mex['Totale_Messaggi_pers'].idxmax()]

print(f"Persona con più messaggi: {p_con_piu_messaggi['Mittente']}, Totale messaggi: {p_con_piu_messaggi['Totale_Messaggi_pers']}")
