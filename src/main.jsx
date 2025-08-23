import React from 'react';
import ReactDOM from 'react-dom/client';
import HomePage from './HomePage'; // Update import ini ke HomePage


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <HomePage /> {/* Gunakan komponen HomePage */}
  </React.StrictMode>
);


