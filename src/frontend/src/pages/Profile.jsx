// src/pages/Profile.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "../context/I18nContext";
import UserService from "../services/userService";
import Loader from "../components/Loader";
import "../styles/Profile.css";

export default function Profile() {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editing, setEditing] = useState(false);

  const [profileData, setProfileData] = useState({
    nombre: "",
    email: "",
    telefono: "",
    direccion: "",
    rol: "",
    imagen: null, // URL or File object
  });
  
  const [previewImage, setPreviewImage] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await UserService.getProfile();
      setProfileData({
        nombre: data.nombre || "",
        email: data.email || "",
        telefono: data.telefono || "",
        direccion: data.direccion || "",
        rol: data.rol || "",
        imagen: data.imagen || null,
      });
      if (data.imagen) {
        setPreviewImage(data.imagen);
      }
    } catch (err) {
      console.error("Error loading profile:", err);
      setError(t('errors.generic'));
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfileData({ ...profileData, [name]: value });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProfileData({ ...profileData, imagen: file });
      setPreviewImage(URL.createObjectURL(file));
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setSaving(true);

    try {
      // Validate form
      if (!profileData.nombre.trim()) {
        throw new Error(t('validation.required'));
      }
      if (!profileData.email.trim()) {
        throw new Error(t('validation.email'));
      }

      // Prepare FormData
      const formData = new FormData();
      formData.append("nombre", profileData.nombre);
      formData.append("email", profileData.email);
      formData.append("telefono", profileData.telefono);
      formData.append("direccion", profileData.direccion);
      
      // Only append image if it's a File object (new upload)
      if (profileData.imagen instanceof File) {
        formData.append("imagen", profileData.imagen);
      }

      // Update profile
      const updated = await UserService.updateProfile(formData);
      
      setProfileData({
        nombre: updated.nombre || "",
        email: updated.email || "",
        telefono: updated.telefono || "",
        direccion: updated.direccion || "",
        rol: updated.rol || "",
        imagen: updated.imagen || null,
      });
      
      if (updated.imagen) {
        setPreviewImage(updated.imagen);
      }

      setSuccess(t('profile.updateSuccess'));
      setEditing(false);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      console.error("Error updating profile:", err);
      const errorMsg =
        err?.response?.data?.error ||
        err?.response?.data?.detail ||
        err?.message ||
        "Error al actualizar el perfil";
      setError(errorMsg);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditing(false);
    loadProfile(); // Reload original data
  };

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <div className="profile-header-section">
          <h2>👤 {t('users.myProfile')}</h2>
          {!editing && (
            <button onClick={() => setEditing(true)} className="btn-edit-profile">
              ✏️ {t('common.edit')}
            </button>
          )}
        </div>

        <div className="profile-content">
          <form onSubmit={handleSave}>
            {/* Image Section */}
            <div className="profile-image-section">
               <div className="image-wrapper">
                  {previewImage ? (
                    <img 
                    src={previewImage.startsWith('http') || previewImage.startsWith('blob') ? previewImage : `http://localhost:8000${previewImage}`} 
                    alt="Perfil" 
                    className="profile-img-large" 
                  />
                  ) : (
                    <div className="profile-placeholder-large">
                      {profileData.nombre?.charAt(0) || "U"}
                    </div>
                  )}
                  
                  {editing && (
                    <label htmlFor="imagen-upload" className="image-upload-btn" title={t('profile.changePhoto')}>
                      <span>📷</span>
                      <input
                        id="imagen-upload"
                        type="file"
                        accept="image/*"
                        onChange={handleImageChange}
                        style={{ display: "none" }}
                      />
                    </label>
                  )}
               </div>
            </div>

            {/* Alerts */}
            {error && (
              <div className="alert alert-error">
                <span>⚠️</span> {error}
              </div>
            )}
            {success && (
              <div className="alert alert-success">
                <span>✓</span> {success}
              </div>
            )}

            {/* Form Fields */}
            <div className="profile-form-grid">
              <div className="form-group">
                <label>{t('profile.fullName')} *</label>
                <input
                  type="text"
                  name="nombre"
                  value={profileData.nombre}
                  onChange={handleInputChange}
                  disabled={!editing}
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>{t('common.email')} *</label>
                <input
                  type="email"
                  name="email"
                  value={profileData.email}
                  onChange={handleInputChange}
                  disabled={!editing}
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>{t('common.phone')}</label>
                <input
                  type="tel"
                  name="telefono"
                  value={profileData.telefono}
                  onChange={handleInputChange}
                  disabled={!editing}
                  className="form-input"
                  placeholder={t('profile.phonePlaceholder')}
                />
              </div>

              <div className="form-group">
                <label>{t('users.role')}</label>
                <input
                  type="text"
                  name="rol"
                  value={profileData.rol.toUpperCase()}
                  disabled
                  className="form-input"
                />
              </div>

              <div className="form-group full-width">
                <label>{t('common.address')}</label>
                <textarea
                  name="direccion"
                  value={profileData.direccion}
                  onChange={handleInputChange}
                  disabled={!editing}
                  rows="3"
                  className="form-input form-textarea"
                  placeholder={t('profile.addressPlaceholder')}
                />
              </div>
            </div>

            {/* Actions */}
            {editing && (
              <div className="form-actions">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="btn-cancel"
                  disabled={saving}
                >
                  {t('common.cancel')}
                </button>
                <button type="submit" className="btn-save" disabled={saving}>
                  {saving ? t('common.saving') : `💾 ${t('common.save')}`}
                </button>
              </div>
            )}
          </form>

          <div className="back-section">
            <button onClick={() => navigate(-1)} className="btn-back">
              ← {t('common.back')}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
