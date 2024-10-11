const express = require('express');
const multer = require('multer');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const app = express();
const port = 3000;

// Abilita CORS
app.use(cors());

// Configura multer per il caricamento dei file
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/'); // Cartella dove salvare i file
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname); // Usa il nome originale del file
  }
});

const upload = multer({ storage: storage });

// Rotta per caricare il file ZIP
app.post('/upload', upload.single('zipFile'), (req, res) => {
  const filePath = path.join(__dirname, 'uploads', req.file.originalname);
  
  console.log('File caricato:', filePath);

  // Esegui lo script Python e passagli il percorso del file ZIP
  const python = spawn('py', ['script.py', filePath]); // 'py' per Windows, usa 'python3' per altri OS
  
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
