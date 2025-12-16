// src/pages/Settings.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import { useTranslation } from "../context/I18nContext";
import UserService from "../services/userService";
import "../styles/Settings.css";

export default function Settings() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  const { locale, changeLocale, t } = useTranslation();
  
  const [settings, setSettings] = useState({
    emailNotifications: true,
    orderNotifications: true,
    marketingEmails: false,
    language: locale || "es",
    theme: theme || "light",
    currency: "COP"
  });

  const [saved, setSaved] = useState(false);
  const [showPasswordChange, setShowPasswordChange] = useState(false);
  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: ""
  });
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState("");

  useEffect(() => {
    const savedSettings = localStorage.getItem("userSettings");
    if (savedSettings) {
      setSettings(prev => ({ ...prev, ...JSON.parse(savedSettings) }));
    }
  }, []);

  // Update local state when context changes
  useEffect(() => {
    setSettings(prev => ({ ...prev, theme: theme, language: locale }));
  }, [theme, locale]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === "checkbox" ? checked : value;

    setSettings(prev => ({
      ...prev,
      [name]: newValue
    }));

    // Apply changes immediately
    if (name === 'theme') {
        setTheme(newValue);
    }
    if (name === 'language') {
        changeLocale(newValue);
    }
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({ ...prev, [name]: value }));
    setPasswordError("");
  };

  const handleSavePassword = async (e) => {
    e.preventDefault();
    setPasswordError("");
    setPasswordSuccess("");

    // Validations
    if (!passwordData.currentPassword) {
      setPasswordError(t('settings.currentPasswordRequired'));
      return;
    }
    if (!passwordData.newPassword) {
      setPasswordError(t('settings.newPasswordRequired'));
      return;
    }
    
    // Strict Validation matching backend
    const password = passwordData.newPassword;
    if (password.length < 8) {
        setPasswordError("La contraseña debe tener al menos 8 caracteres.");
        return;
    }
    if (!/[A-Z]/.test(password)) {
        setPasswordError("La contraseña debe contener al menos una letra mayúscula.");
        return;
    }
    if (!/[a-z]/.test(password)) {
        setPasswordError("La contraseña debe contener al menos una letra minúscula.");
        return;
    }
    if (!/[0-9]/.test(password)) {
        setPasswordError("La contraseña debe contener al menos un número.");
        return;
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        setPasswordError("La contraseña debe contener al menos un carácter especial.");
        return;
    }

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setPasswordError(t('validation.passwordMatch'));
      return;
    }

    try {
      await UserService.changePassword({
        old_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      });
      
      setPasswordSuccess(t('settings.passwordChanged'));
      setPasswordData({ currentPassword: "", newPassword: "", confirmPassword: "" });
      
      setTimeout(() => {
        setPasswordSuccess("");
        setShowPasswordChange(false);
      }, 3000);
    } catch (error) {
      console.error("Error changing password:", error);
      setPasswordError(error.response?.data?.error || error.response?.data?.detail || t('errors.generic'));
    }
  };

  const handleSave = async () => {
    try {
      localStorage.setItem("userSettings", JSON.stringify(settings));
      setSaved(true);
      setTimeout(() => navigate("/dashboard"), 1500);
    } catch (error) {
      console.error("Error saving settings:", error);
      alert(t('errors.generic'));
    }
  };

  const handleDeactivateAccount = async () => {
    if (window.confirm(t('settings.confirmDeactivate'))) {
      try {
        await UserService.deactivateAccount();
        alert(t('settings.accountDeactivated'));
        logout();
        navigate("/login");
      } catch (error) {
        console.error("Error deactivating:", error);
        alert(t('errors.generic'));
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="settings-container">
      <div className="settings-card">
        <h1 className="settings-title">⚙️ {t('users.settings')}</h1>
        
        {/* User Info */}
        <section className="settings-section">
          <h2 className="section-title">👤 {t('settings.userInfo')}</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">{t('common.name')}:</span>
              <span className="info-value">{user?.nombre || "N/A"}</span>
            </div>
            <div className="info-item">
              <span className="info-label">{t('common.email')}:</span>
              <span className="info-value">{user?.email || "N/A"}</span>
            </div>
            <div className="info-item">
              <span className="info-label">{t('users.role')}:</span>
              <span className="info-value">{user?.rol?.toUpperCase() || "N/A"}</span>
            </div>
          </div>
        </section>

        {/* Password Change */}
        <section className="settings-section">
          <h2 className="section-title">🔒 {t('settings.security')}</h2>
          {!showPasswordChange ? (
            <button 
              onClick={() => setShowPasswordChange(true)} 
              className="btn-secondary"
            >
              🔑 {t('settings.changePassword')}
            </button>
          ) : (
            <form onSubmit={handleSavePassword} className="password-form">
              {passwordError && (
                <div className="alert alert-error">⚠️ {passwordError}</div>
              )}
              {passwordSuccess && (
                <div className="alert alert-success">✓ {passwordSuccess}</div>
              )}
              
              <div className="form-group">
                <label>{t('settings.currentPassword') }*</label>
                <input
                  type="password"
                  name="currentPassword"
                  value={passwordData.currentPassword}
                  onChange={handlePasswordChange}
                  className="form-input"
                  required
                />
              </div>
              
              <div className="form-group">
                <label>{t('settings.newPassword')} *</label>
                <input
                  type="password"
                  name="newPassword"
                  value={passwordData.newPassword}
                  onChange={handlePasswordChange}
                  className="form-input"
                  required
                />
                
                {/* Visual Password Requirements */}
                <div className="password-requirements">
                   <p className="requirements-title">Requisitos de contraseña:</p>
                   <ul className="requirements-list">
                      <li className={passwordData.newPassword.length >= 8 ? "valid" : "invalid"}>
                        {passwordData.newPassword.length >= 8 ? "✓" : "○"} Mínimo 8 caracteres
                      </li>
                      <li className={/[A-Z]/.test(passwordData.newPassword) ? "valid" : "invalid"}>
                        {/[A-Z]/.test(passwordData.newPassword) ? "✓" : "○"} Una mayúscula
                      </li>
                      <li className={/[a-z]/.test(passwordData.newPassword) ? "valid" : "invalid"}>
                        {/[a-z]/.test(passwordData.newPassword) ? "✓" : "○"} Una minúscula
                      </li>
                      <li className={/[0-9]/.test(passwordData.newPassword) ? "valid" : "invalid"}>
                        {/[0-9]/.test(passwordData.newPassword) ? "✓" : "○"} Un número
                      </li>
                      <li className={/[!@#$%^&*(),.?":{}|<>]/.test(passwordData.newPassword) ? "valid" : "invalid"}>
                        {/[!@#$%^&*(),.?":{}|<>]/.test(passwordData.newPassword) ? "✓" : "○"} Un carácter especial
                      </li>
                   </ul>
                </div>
              </div>
              
              <div className="form-group">
                <label>{t('settings.confirmPassword')} *</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={passwordData.confirmPassword}
                  onChange={handlePasswordChange}
                  className="form-input"
                  required
                />
                 {passwordData.confirmPassword && passwordData.newPassword !== passwordData.confirmPassword && (
                    <small className="error-text">Las contraseñas no coinciden</small>
                 )}
              </div>
              
              <div className="form-actions">
                <button 
                  type="button" 
                  onClick={() => {
                    setShowPasswordChange(false);
                    setPasswordData({ currentPassword: "", newPassword: "", confirmPassword: "" });
                    setPasswordError("");
                  }} 
                  className="btn-cancel"
                >
                  {t('common.cancel')}
                </button>
                <button 
                  type="submit" 
                  className="btn-save"
                  disabled={
                    !passwordData.currentPassword ||
                    !passwordData.newPassword ||
                    passwordData.newPassword !== passwordData.confirmPassword ||
                    passwordData.newPassword.length < 8 ||
                    !/[A-Z]/.test(passwordData.newPassword) ||
                    !/[a-z]/.test(passwordData.newPassword) ||
                    !/[0-9]/.test(passwordData.newPassword) ||
                    !/[!@#$%^&*(),.?":{}|<>]/.test(passwordData.newPassword)
                  }
                >
                  💾 {t('common.save')}
                </button>
              </div>
            </form>

          )}
        </section>

        {/* Notifications */}
        <section className="settings-section">
          <h2 className="section-title">🔔 {t('settings.notifications')}</h2>
          <div className="setting-item">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="emailNotifications"
                checked={settings.emailNotifications}
                onChange={handleChange}
                className="checkbox-input"
              />
              {t('settings.emailNotifications')}
            </label>
          </div>
          <div className="setting-item">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="orderNotifications"
                checked={settings.orderNotifications}
                onChange={handleChange}
                className="checkbox-input"
              />
              {t('settings.orderNotifications')}
            </label>
          </div>
          <div className="setting-item">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="marketingEmails"
                checked={settings.marketingEmails}
                onChange={handleChange}
                className="checkbox-input"
              />
              {t('settings.marketingEmails')}
            </label>
          </div>
        </section>

        {/* Preferences */}
        <section className="settings-section">
          <h2 className="section-title">🎨 {t('settings.preferences')}</h2>
          <div className="setting-item">
            <label className="select-label">
              {t('language.select')}:
              <select
                name="language"
                value={settings.language}
                onChange={handleChange}
                className="select-input"
              >
                <option value="es">{t('language.spanish')}</option>
                <option value="en">{t('language.english')}</option>
              </select>
            </label>
          </div>
          <div className="setting-item">
            <label className="select-label">
              {t('theme.toggle')}:
              <select
                name="theme"
                value={settings.theme}
                onChange={handleChange}
                className="select-input"
              >
                <option value="light">{t('theme.light')}</option>
                <option value="dark">{t('theme.dark')}</option>
              </select>
            </label>
          </div>
          <div className="setting-item">
            <label className="select-label">
              {t('settings.currency')}:
              <select
                name="currency"
                value={settings.currency}
                onChange={handleChange}
                className="select-input"
              >
                <option value="COP">COP (Pesos Colombianos)</option>
                <option value="USD">USD (Dólares)</option>
                <option value="EUR">EUR (Euros)</option>
              </select>
            </label>
          </div>
        </section>

        {/* Actions */}
        <section className="settings-section">
          <h2 className="section-title">🔧 {t('common.actions')}</h2>
          <div className="button-group">
            <button onClick={handleSave} className="btn-save">
              {saved ? `✓ ${t('settings.saved')}` : `💾 ${t('common.save')}`}
            </button>
            <button onClick={handleLogout} className="btn-logout">
              🚪 {t('common.logout')}
            </button>
            <button onClick={handleDeactivateAccount} className="btn-danger">
              ⚠️ {t('settings.deactivateAccount')}
            </button>
          </div>
        </section>

        {saved && (
          <div className="alert alert-success">
            ✓ {t('settings.savedSuccess')}
          </div>
        )}
      </div>
    </div>
  );
}
