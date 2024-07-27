const express = require('express');
const axios = require('axios');
const app = express();
const port = process.env.PORT || 3000;

const IPDATA_API_KEY = process.env.IPDATA_API_KEY;

app.get('/', async (req, res) => {
  try {
    const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    const response = await axios.get(`https://api.ipdata.co/${ip}?api-key=${IPDATA_API_KEY}`);
    const ipData = response.data;

    // Log the IP data
    console.log('IP Address:', ipData.ip);
    console.log('City:', ipData.city);
    console.log('Region:', ipData.region);
    console.log('Country:', ipData.country_name);
    console.log('Latitude:', ipData.latitude);
    console.log('Longitude:', ipData.longitude);

    // Send the IP data as the response
    res.send(
      `IP Address: ${ipData.ip}\n` +
      `City: ${ipData.city}\n` +
      `Region: ${ipData.region}\n` +
      `Country: ${ipData.country_name}\n` +
      `Latitude: ${ipData.latitude}\n` +
      `Longitude: ${ipData.longitude}`
    );
  } catch (error) {
    res.status(500).send('Error fetching IP data: ' + error.toString());
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
