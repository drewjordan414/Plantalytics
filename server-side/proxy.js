const express = require('express');
const request = require('request');

const app = express();
const port = 3000;
const apiKEY = "mr_oVBJyJU8T8JhSYfsR1bligkBN0gIq7cva_2tMX1E";

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});

app.get('/plants/search', (req, res) => {
  const searchTerm = req.query.q;
  request(
    { url: `https://trefle.io/api/v1/plants/search?token=${apiKEY}&q=${searchTerm}` },
    (error, response, body) => {
      if (error || response.statusCode !== 200) {
        return res.status(500).json({ type: 'error', message: error.message });
      }
      res.json(JSON.parse(body));
    }
  );
});

app.listen(port, () => console.log(`Proxy server running on port ${port}`));
