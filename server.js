const express = require('express');
const bodyParser = require('body-parser');
const { execFile } = require('child_process');
const path = require('path');

const app = express();
app.use(bodyParser.json());
app.use(express.static(__dirname));

// Route qui reçoit le code depuis l'interface HTML et exécute venin.py
app.post('/run', (req, res) => {
    const codeVenin = req.body.code;

    // Appelle directement ton interpréteur Python local avec venin.py
    execFile('python3', [path.join(__dirname, 'venin.py'), codeVenin], (error, stdout, stderr) => {
        let output = stdout || '';
        if (stderr) output += '\n' + stderr;
        if (error && !stdout && !stderr) output = 'Erreur lors de l\'exécution : ' + error.message;
        res.json({ output: output });
    });
});

app.listen(3000, () => {
    console.log('🐍 IDE Venin démarré sur http://localhost:3000');
});