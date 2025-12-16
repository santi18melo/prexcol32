import React, { useState, useEffect } from 'react';
import { useTranslation } from '../context/I18nContext';
import { useNavigate } from 'react-router-dom';
import './HelpButton.css';

const HelpButton = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);

  const openManual = () => {
    // Abrir el manual en una nueva pestaña
    window.open('http://localhost:8000/api/docs/MANUAL_USUARIO_COMPLETO.html', '_blank');
  };

  const toggleModal = () => {
    setShowModal(!showModal);
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+H - Abrir/Cerrar ayuda
      if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        toggleModal();
      }
      // F1 - Abrir manual completo
      if (e.key === 'F1') {
        e.preventDefault();
        openManual();
      }
      // Esc - Cerrar modal
      if (e.key === 'Escape' && showModal) {
        setShowModal(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [showModal]);

  return (
    <>
      {/* Botón flotante */}
      <div className="help-button-container">
        <button 
          className="help-button" 
          onClick={toggleModal}
          title={t('help.buttonTitle')}
          aria-label={t('help.help')}
        >
          <span className="help-icon">🆘</span>
        </button>
      </div>

      {/* Modal de ayuda rápida */}
      {showModal && (
        <div className="help-modal-overlay" onClick={toggleModal}>
          <div className="help-modal" onClick={(e) => e.stopPropagation()}>
            <div className="help-modal-header">
              <h3>🆘 {t('help.helpCenter')}</h3>
              <button className="close-btn" onClick={toggleModal}>✕</button>
            </div>
            
            <div className="help-modal-content">
              <div className="help-section">
                <h4>📖 {t('help.documentation')}</h4>
                <button className="help-link-btn" onClick={openManual}>
                  📚 {t('help.userManual')}
                </button>
                <button className="help-link-btn" onClick={() => window.open('http://localhost:8000/api/docs/', '_blank')}>
                  📄 {t('help.technicalDocs')}
                </button>
              </div>

              <div className="help-section">
                <h4>🎯 {t('help.quickAccess')}</h4>
                <div className="quick-links">
                  <button className="help-link-btn" onClick={() => { navigate('/dashboard'); setShowModal(false); }}>
                    🏠 {t('help.dashboard')}
                  </button>
                  <button className="help-link-btn" onClick={() => { navigate('/profile'); setShowModal(false); }}>
                    👤 {t('help.myProfile')}
                  </button>
                  <button className="help-link-btn" onClick={() => { navigate('/settings'); setShowModal(false); }}>
                    ⚙️ {t('help.settings')}
                  </button>
                </div>
              </div>

              <div className="help-section">
                <h4>📞 {t('help.support')}</h4>
                <div className="support-info">
                  <p>
                    📧 <strong>{t('help.email')}:</strong>{' '}
                    <a href="mailto:prexcoloficial@gmail.com" style={{color: '#3b82f6'}}>
                      prexcoloficial@gmail.com
                    </a>
                  </p>
                  <p>
                    📞 <strong>{t('help.phone')}:</strong>{' '}
                    <a href="https://wa.me/573246648181" target="_blank" rel="noopener noreferrer" style={{color: '#25D366'}}>
                      +57 3246648181
                    </a>
                  </p>
                  <p>🕐 <strong>{t('help.schedule')}:</strong> {t('help.scheduleHours')}</p>
                </div>
              </div>

              <div className="help-section">
                <h4>⌨️ {t('help.keyboardShortcuts')}</h4>
                <div className="keyboard-shortcuts">
                  <div className="shortcut">
                    <kbd>Ctrl</kbd> + <kbd>H</kbd>
                    <span>{t('help.shortcutHelp')}</span>
                  </div>
                  <div className="shortcut">
                    <kbd>F1</kbd>
                    <span>{t('help.shortcutManual')}</span>
                  </div>
                  <div className="shortcut">
                    <kbd>Esc</kbd>
                    <span>{t('help.shortcutClose')}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="help-modal-footer">
              <p className="version-info">{t('help.version')}</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default HelpButton;
