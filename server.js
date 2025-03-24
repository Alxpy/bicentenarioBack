const express = require('express');
const path = require('path');
const cors = require('cors');
const serveIndex = require('serve-index');
const helmet = require('helmet');

const app = express();

// Enable CORS
app.use(cors({
  origin: '*', // Permite cualquier origen
  methods: ['*'], // Métodos permitidos
  allowedHeaders: ['*']
}));

app.use(helmet({
  crossOriginResourcePolicy: false,
}));

// Serve static files and enable directory listing for /images
const imagesPath = path.join(__dirname, 'public/imagenes');
app.use(
  '/images',
  express.static(imagesPath),
  serveIndex(imagesPath, { icons: true, view: 'details' }) // Enable file listing with icons and detailed view
);

// Start the server on port 3000
app.listen(3000, () => {
  console.log('Servidor corriendo en http://127.0.0.1:3000');
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Error en el servidor');
});