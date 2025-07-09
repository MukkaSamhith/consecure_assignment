import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    axios.get("/api/threats/stats").then(res => setStats(res.data));
  }, []);

  return (
    <div>
      <h1>Threat Intelligence Dashboard</h1>
      <p>Total Threats: {stats.total_threats}</p>
      <p>By Category:</p>
      <ul>
        {stats.by_category && Object.entries(stats.by_category).map(([key, val]) => (
          <li key={key}>{key}: {val}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
