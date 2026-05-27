import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [isVerifying, setIsVerifying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('Sẵn sàng xác thực');

  const startVerification = () => {
    if (isVerifying) return;
    setIsVerifying(true);
    setProgress(0);
    setStatusText('Đang kết nối camera...');

    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += 1;
      setProgress(currentProgress);

      if (currentProgress === 15) {
        setStatusText('Đang tìm kiếm khuôn mặt...');
      } else if (currentProgress === 45) {
        setStatusText('Đang trích xuất đặc trưng sinh trắc học...');
      } else if (currentProgress === 75) {
        setStatusText('Đang đối chiếu dữ liệu backend...');
      } else if (currentProgress >= 100) {
        clearInterval(interval);
        setStatusText('Xác thực thành công!');
      }
    }, 40); 
  };

  return (
    <div className="dashboard-wrapper">
      <header className="dashboard-header">
        <div className="db-container header-inner">
          <div className="logo" onClick={() => navigate('/')}>
            SmartFace
          </div>
          <button className="btn-back" onClick={() => navigate('/')}>
            Quay lại trang chủ
          </button>
        </div>
      </header>
      <main className="dashboard-main">
        <div className="db-container main-grid">
          <div className="video-column">
            <div className={`video-frame ${isVerifying ? 'active-scan' : ''}`}>
              <video id="backend-video" autoPlay playsInline muted></video>
              {isVerifying && <div className="scan-line"></div>}
              <div className="video-placeholder">
                <svg viewBox="0 0 24 24" fill="currentColor" className="camera-icon">
                  <path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/>
                </svg>
                <p> Video Stream</p>
                <span className="stream-status">
                  {isVerifying ? 'Hệ thống đang gọi camera...' : 'Chưa kết nối luồng'}
                </span>
              </div>
            </div>
          </div>
          <div className="control-column">
            <div className="control-card">
              <h2 className="control-title">Bắt đầu xác thực</h2>
              <p className="control-desc">
                Nhấn vào nút bên dưới để hệ thống bắt đầu kết nối camera và xác minh khuôn mặt của bạn.
              </p>
              
              <button 
                className={`btn-action-verify ${isVerifying ? 'disabled' : ''}`}
                onClick={startVerification}
                disabled={isVerifying}
              >
                {isVerifying ? 'Đang nhận diện...' : 'Bắt đầu xác thực'}
              </button>
              {isVerifying && (
                <div className="progress-section">
                  <div className="progress-header">
                    <span className="status-label">{statusText}</span>
                    <span className="percent-label">{progress}%</span>
                  </div>
                  <div className="progress-bar-track">
                    <div className="progress-bar-fill" style={{ width: `${progress}%` }}></div>
                  </div>
                </div>
              )}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
};

export default Dashboard;