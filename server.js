const express = require('express');
const cors = require('cors'); // Importa il pacchetto cors
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// Abilita CORS per tutte le richieste
app.use(cors());

// Middleware per gestire le richieste JSON
app.use(bodyParser.json());

// Definisci una rotta di esempio
app.post('/run-script', (req, res) => {
  const inputData = req.body.data || '';

  const python = spawn('python', ['script.py', inputData]);

  let output = '';
  python.stdout.on('data', (data) => {
    output += data.toString();
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on('close', (code) => {
    console.log(`Processo Python terminato con codice ${code}`);
    res.json({ output: output });
  });
});

// Avvia il server
app.listen(port, () => {
  console.log(`Server in ascolto su http://localhost:${port}`);
});
