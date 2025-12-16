import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { useTranslation } from '../context/I18nContext';
import LanguageSelector from './LanguageSelector';
import { getMediaURL } from '../config/api.js';
import '../styles/DashboardHeader.css';

const DashboardHeader = ({ title }) => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);

  const handleLogout = () => {
    logout();
    setTimeout(() => {
      console.log('[DashboardHeader] Redirecting to /login');
      window.location.replace('/login');
    }, 200);
  };

  const getImageUrl = (path) => {
    return getMediaURL(path) || null;
  };

  return (
    <div className="dashboard-header">
      <div className="header-content">
        <div className="header-left">
           <h1 style={{ color: theme === 'dark' ? '#f1f5f9' : 'black' }}>{title}</h1>
        </div>

        <div className="header-right" style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            {/* Documentation Link */}
            <a 
              href={`${getMediaURL('')}/docs/`} 
              target="_blank" 
              rel="noopener noreferrer"
              className="btn-link"
              style={{ 
                  color: theme === 'dark' ? '#cbd5e1' : '#64748b', 
                  textDecoration: 'none', 
                  fontSize: '0.9rem', 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '6px',
                  padding: '6px 12px',
                  borderRadius: '6px',
                  background: theme === 'dark' ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)'
              }}
            >
              <span>📚</span> <span className="hide-mobile">{t('documentation.docs')}</span>
            </a>
            
            {/* Theme Toggle */}
            <button 
                onClick={toggleTheme}
                style={{ 
                    background: 'transparent', 
                    border: theme === 'dark' ? '1px solid #475569' : '1px solid #e2e8f0', 
                    borderRadius: '8px',
                    cursor: 'pointer', 
                    fontSize: '1.2rem', 
                    padding: '6px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'all 0.2s',
                    width: '36px',
                    height: '36px'
                }}
                title={theme === 'light' ? t('theme.switchToDark') : t('theme.switchToLight')}
            >
                {theme === 'light' ? '🌙' : '☀️'}
            </button>

            {/* Language Selector */}
            <LanguageSelector />

            {/* User Profile */}
            <div 
              className="user-menu-container" 
              style={{ position: 'relative', cursor: 'pointer' }}
              onClick={() => setShowDropdown(!showDropdown)}
            >
              <div className="user-profile-trigger" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div className="profile-text">
                   <span style={{ display: 'block', fontWeight: 'bold', fontSize: '0.9rem', color: theme === 'dark' ? '#f1f5f9' : '#1e293b' }}>
                        {user?.nombre}
                   </span>
                   <span style={{ display: 'block', fontSize: '0.75rem', color: theme === 'dark' ? '#94a3b8' : '#64748b', textTransform: 'capitalize' }}>
                        {user?.rol}
                   </span>
                </div>
                <div className="profile-avatar" style={{ width: '40px', height: '40px', borderRadius: '50%', overflow: 'hidden', border: `2px solid ${theme === 'dark' ? '#475569' : '#e2e8f0'}` }}>
                   {user?.imagen ? (
                      <img src={getImageUrl(user.imagen)} alt="Perfil" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                   ) : (
                      <div style={{ width: '100%', height: '100%', background: '#3b82f6', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                        {user?.nombre?.charAt(0) || "U"}
                      </div>
                   )}
                </div>
                <span style={{ fontSize: '0.8rem', color: theme === 'dark' ? '#94a3b8' : '#64748b' }}>▼</span>
              </div>

              {showDropdown && (
                <div className="user-dropdown" style={{
                  position: 'absolute',
                  top: '120%',
                  right: 0,
                  width: '220px',
                  background: theme === 'dark' ? '#1e293b' : 'white',
                  borderRadius: '12px',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1)',
                  border: `1px solid ${theme === 'dark' ? '#334155' : '#f1f5f9'}`,
                  zIndex: 50,
                  overflow: 'hidden'
                }}>
                  <div className="dropdown-header" style={{ padding: '16px', borderBottom: `1px solid ${theme === 'dark' ? '#334155' : '#f1f5f9'}`, background: theme === 'dark' ? '#0f172a' : '#f8fafc' }}>
                    <p style={{ margin: 0, fontWeight: 'bold', color: theme === 'dark' ? '#f1f5f9' : '#334155' }}>{t('users.myAccount')}</p>
                    <p style={{ margin: 0, fontSize: '0.8rem', color: '#94a3b8' }}>{user?.email}</p>
                  </div>
                  <ul style={{ listStyle: 'none', padding: '8px 0', margin: 0 }}>
                    <li>
                      <button 
                        onClick={(e) => { e.stopPropagation(); navigate('/profile'); setShowDropdown(false); }}
                        style={{ width: '100%', textAlign: 'left', padding: '10px 16px', border: 'none', background: 'transparent', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '10px', color: theme === 'dark' ? '#cbd5e1' : '#475569', fontSize: '0.9rem' }}
                        onMouseOver={(e) => e.target.style.background = theme === 'dark' ? '#334155' : '#f8fafc'}
                        onMouseOut={(e) => e.target.style.background = 'transparent'}
                      >
                        <span>👤</span> {t('users.myProfile')}
                      </button>
                    </li>
                    <li>
                      <button 
                        onClick={(e) => { e.stopPropagation(); navigate('/settings'); setShowDropdown(false); }}
                        style={{ width: '100%', textAlign: 'left', padding: '10px 16px', border: 'none', background: 'transparent', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '10px', color: theme === 'dark' ? '#cbd5e1' : '#475569', fontSize: '0.9rem' }}
                        onMouseOver={(e) => e.target.style.background = theme === 'dark' ? '#334155' : '#f8fafc'}
                        onMouseOut={(e) => e.target.style.background = 'transparent'}
                      >
                        <span>⚙️</span> {t('users.settings')}
                      </button>
                    </li>
                    <li style={{ borderTop: `1px solid ${theme === 'dark' ? '#334155' : '#f1f5f9'}`, marginTop: '8px', paddingTop: '8px' }}>
                      <button 
                        onClick={(e) => { e.stopPropagation(); handleLogout(); }}
                        style={{ width: '100%', textAlign: 'left', padding: '10px 16px', border: 'none', background: 'transparent', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '10px', color: '#ef4444', fontSize: '0.9rem', fontWeight: '500' }}
                        onMouseOver={(e) => e.target.style.background = theme === 'dark' ? '#450a0a' : '#fef2f2'}
                        onMouseOut={(e) => e.target.style.background = 'transparent'}
                      >
                        <span>🚪</span> {t('common.logout')}
                      </button>
                    </li>
                  </ul>
                </div>
              )}
            </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardHeader;
