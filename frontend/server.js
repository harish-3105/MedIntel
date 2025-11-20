import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || 'https://medintel-backend.onrender.com';

// Add body parser middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

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

// Proxy API requests to backend
app.use('/api', async (req, res) => {
  const url = `${API_URL}${req.url}`;
  console.log(`Proxying ${req.method} ${req.url} to ${url}`);
  
  try {
    const fetch = (await import('node-fetch')).default;
    
    const options = {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    };
    
    // Add body for POST/PUT/PATCH requests
    if (['POST', 'PUT', 'PATCH'].includes(req.method)) {
      options.body = JSON.stringify(req.body);
    }
    
    const response = await fetch(url, options);
    const contentType = response.headers.get('content-type');
    
    // Parse response based on content type
    let data;
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }
    
    res.status(response.status).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ 
      error: 'Proxy error', 
      details: error.message,
      backend_url: API_URL 
    });
  }
});

// Serve static files from dist directory
app.use(express.static(distPath));

// Handle React Router - serve index.html for all routes
app.get('*', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ MedIntel Frontend running on port ${PORT}`);
  console.log(`Server listening on http://0.0.0.0:${PORT}`);
  console.log(`Proxying API requests to: ${API_URL}`);
});
