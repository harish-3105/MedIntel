import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Verify dist folder exists
const distPath = path.join(__dirname, 'dist');
console.log('Checking dist folder at:', distPath);
if (!fs.existsSync(distPath)) {
  console.error('❌ ERROR: dist folder not found!');
  process.exit(1);
}
console.log('✓ dist folder exists');

// Log dist contents
const distContents = fs.readdirSync(distPath);
console.log('dist folder contains:', distContents);

// Serve static files from dist directory
app.use(express.static(distPath));

// Handle React Router - serve index.html for all routes
app.get('*', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ MedIntel Frontend running on port ${PORT}`);
  console.log(`Server listening on http://0.0.0.0:${PORT}`);
});
