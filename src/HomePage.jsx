import React from 'react';
import './HomePage.css';  // Jangan lupa untuk membuat file CSS baru dengan nama yang sesuai

function HomePage() {
  return (
    <div className="container">
      <div className="card">
        <div className="icon">
          {/* Placeholder untuk ikon, bisa diganti dengan gambar */}
        </div>
        <div className="text">
          <h2>Help me <span className="highlight">HEAR</span></h2>
        </div>
      </div>
      <div className="card">
        <div className="icon">
          {/* Placeholder untuk ikon, bisa diganti dengan gambar */}
        </div>
        <div className="text">
          <h2>Help me <span className="highlight">SPEAK</span></h2>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
