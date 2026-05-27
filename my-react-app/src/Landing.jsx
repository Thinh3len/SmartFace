import React from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

const Landing = () => {
  const navigate = useNavigate();

  const features = [
    {
      id: 1,
      text: "Giao diện đơn giản - Dễ sử dụng",
      icon: (
        <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25M19.5 5.25a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25m15 0V13.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 13.5V5.25" />
        </svg>
      )
    },
    {
      id: 2,
      text: "Độ chính xác cao",
      icon: (
        <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0110 21a3.745 3.745 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.746 3.746 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0114 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
        </svg>
      )
    },
    {
      id: 3,
      text: "Đơn giản hóa quy trình",
      icon: (
        <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
        </svg>
      )
    },
    {
      id: 4,
      text: "Mang lại tính công bằng cao",
      icon: (
        <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0-17.25a9 9 0 019 9M12 3a9 9 0 00-9 9m9 5.25a9 9 0 01-9-9m9 9a9 9 0 009-9M5.625 7.5h12.75M5.625 12h12.75m-12.75 4.5h12.75" />
        </svg>
      )
    }
  ];

  return (
    <div className="landing-wrapper">
      <video autoPlay loop muted playsInline className="background-video">
        <source src="/intro.mp4" type="video/mp4" />
      </video>
      
      <div className="content-container"></div>

      <header className="header">
        <div className="container header-container">
          <div className="header-left">
            <a href="#home" className="logo">SmartFace</a>
          </div>
          <div className="header-right"></div>
        </div>
      </header>

      <main className="hero-section">
        <div className="container">
          <div className="hero-left">
            <h1>Xác thực miễn phí với SmartFace</h1>
            <button 
              className="btn-dangnhap" 
              onClick={() => navigate('/Dashboard')}
            >
              Đăng nhập ngay!
            </button>
          </div>
        </div>
      </main>

      <section className="features-section">
        <div className="container features-grid">
          {features.map((item) => (
            <div key={item.id} className="feature-item">
              <div className="icon-box">
                {item.icon}
              </div>
              <div className="feature-text">
                {item.text}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Landing;