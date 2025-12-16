import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "../context/I18nContext";
import OrderService from "../services/orderService";
import { axiosInstance } from "../services/api";
import "../styles/CompradorDashboard.css"; // Reusing styles for now
import DashboardHeader from "../components/DashboardHeader";
import ModalDetallePedido from "../components/ModalDetallePedido";

export default function UnifiedDashboard() {
  const { user, logout } = useAuth();
  const { t } = useTranslation();
  const navigate = useNavigate();
  // Determine role for UI adjustments
  // Unified role: Logistica handles everything now
  const isLogistica = user?.rol === "logistica" || user?.rol === "admin";

  const [activeTab, setActiveTab] = useState("pendiente");
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [selectedPedido, setSelectedPedido] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredPedidos = pedidos.filter(p => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    const idMatch = p.id.toString().includes(term);
    const clientMatch = p.cliente_nombre?.toLowerCase().includes(term);
    const storeMatch = p.tienda_nombre?.toLowerCase().includes(term);
    return idMatch || clientMatch || storeMatch;
  });

  // ==================== CARGAR PEDIDOS ====================
  const cargarPedidos = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      let data = [];
      
      if (isLogistica) {
        // Use the unified endpoint for logistics to get all statuses
        // This avoids issues with pagination hiding items in specific statuses when using generic endpoints
        const res = await OrderService.getLogisticsPanelOrders();
        const allPedidos = res.results || res;
        
        // Filter locally based on activeTab
        if (activeTab === "pendiente") {
             data = allPedidos.filter(p => p.estado === "pendiente");
        } else if (activeTab === "preparando") {
             data = allPedidos.filter(p => p.estado === "preparando");
        } else if (activeTab === "en_transito") {
             data = allPedidos.filter(p => p.estado === "en_transito");
        } else if (activeTab === "entregado") {
             data = allPedidos.filter(p => p.estado === "entregado");
        } else {
             data = allPedidos; 
        }
      } else {
        // Fallback for non-logistics (e.g. Admin view specific or others) - though this component seems logistics focused now
        // Existing logic for safety
        if (activeTab === "pendiente") {
             const res = await OrderService.getPendingOrders();
             data = res.results || res;
        } else if (activeTab === "preparando") {
             const res = await OrderService.getOrdersInPreparation();
             data = res.results || res;
        } else {
             const res = await axiosInstance.get("/productos/pedidos/");
             const allPedidos = res.data.results || res.data;
             data = allPedidos.filter(p => p.estado === activeTab);
        }
      }

      setPedidos(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Error cargando pedidos:", err);
      if (err.response?.status !== 403) {
          setError(t('errors.loadingOrders') + " " + (err.response?.data?.detail || ""));
      } else {
          setPedidos([]); // Clear if no permission
      }
    } finally {
      setLoading(false);
    }
  }, [activeTab, isLogistica]);

  useEffect(() => {
    cargarPedidos();
  }, [cargarPedidos]);

  // ==================== HELPER - TRADUCIR ESTADOS ====================
  const getStatusLabel = (status) => {
    const statusMap = {
      'pendiente': t('orders.status.pending'),
      'preparando': t('orders.status.preparing'),
      'en_transito': t('orders.status.inTransit'),
      'entregado': t('orders.status.delivered'),
      'cancelado': t('orders.status.cancelled')
    };
    return statusMap[status] || status;
  };

  // ==================== CAMBIAR ESTADO ====================
  const handleCambiarEstado = async (pedidoId, nuevoEstado) => {
    if (!window.confirm(t('messages.confirmStatusChange', { id: pedidoId, status: getStatusLabel(nuevoEstado) }))) {
      return;
    }

    setError("");
    try {
      await OrderService.updateOrderStatus(pedidoId, nuevoEstado);
      setSuccess(t('orders.updateSuccess', { id: pedidoId, status: getStatusLabel(nuevoEstado) }));
      await cargarPedidos();
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      setError(err.response?.data?.error || t('errors.changingStatus'));
      setTimeout(() => setError(""), 5000);
    }
  };

  // ==================== RENDER HELPERS ====================
  const renderActions = (pedido) => {
    if (pedido.estado === "pendiente" && isLogistica) {
      return (
        <button
          className="btn-action btn-preparar"
          onClick={() => handleCambiarEstado(pedido.id, "preparando")}
        >
          ⚙️ {t('orders.actions.startPreparation')}
        </button>
      );
    }
    if (pedido.estado === "preparando" && isLogistica) {
      return (
        <button
          className="btn-action btn-listo"
          onClick={() => handleCambiarEstado(pedido.id, "en_transito")}
        >
          🚚 {t('orders.actions.startShipping')}
        </button>
      );
    }
    if (pedido.estado === "en_transito" && isLogistica) {
      return (
        <button
          className="btn-action btn-entregado"
          onClick={() => handleCambiarEstado(pedido.id, "entregado")}
        >
          ✓ {t('orders.actions.markDelivered')}
        </button>
      );
    }
    return null;
  };

  return (
    <div className="comprador-dashboard"> {/* Reusing class for layout */}
      <DashboardHeader title={`⚡ ${t('dashboard.operationsCenter')}`} />

      {/* ALERTS */}
      {error && <div className="alert alert-error"><span>⚠️</span> {error}</div>}
      {success && <div className="alert alert-success"><span>✓</span> {success}</div>}

      {/* TABS */}
      <div className="tabs-container" style={{ marginTop: 20, padding: '0 40px' }}>
        <div className="tabs">
          {isLogistica && (
            <button
                className={`tab ${activeTab === "pendiente" ? "active" : ""}`}
                onClick={() => setActiveTab("pendiente")}
            >
                📋 {t('tabs.pending')}
            </button>
          )}
          <button
            className={`tab ${activeTab === "preparando" ? "active" : ""}`}
            onClick={() => setActiveTab("preparando")}
          >
            ⚙️ {t('tabs.preparing')}
          </button>
          <button
            className={`tab ${activeTab === "en_transito" ? "active" : ""}`}
            onClick={() => setActiveTab("en_transito")}
          >
            🚚 {t('tabs.inTransit')}
          </button>
          <button
            className={`tab ${activeTab === "entregado" ? "active" : ""}`}
            onClick={() => setActiveTab("entregado")}
          >
            ✅ {t('tabs.delivered')}
          </button>
        </div>
      </div>

      {/* LISTA DE PEDIDOS */}
      <div className="pedidos-container" style={{ marginTop: 20 }}>
        <div className="section-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '15px' }}>
            <h2>
                <span key={activeTab}>
                    {activeTab === "pendiente" ? t('dashboard.logistics.newOrders') :
                     activeTab === "preparando" ? t('dashboard.logistics.inPreparation') :
                     activeTab === "en_transito" ? t('dashboard.logistics.inRoute') :
                     t('dashboard.logistics.deliveryHistory')}
                </span>
            </h2>

            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                <input 
                    type="text" 
                    placeholder={t('search.placeholder')} 
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{ padding: '8px 12px', borderRadius: '6px', border: '1px solid #ccc', minWidth: '200px' }}
                />
                
                <button onClick={cargarPedidos} className="btn-refresh">
                    🔄 {t('common.refresh')}
                </button>
            </div>
        </div>

        {loading ? (
             <div className="loading-container">
                <div className="spinner"></div>
                <p>{t('common.loading')}</p>
             </div>
        ) : filteredPedidos.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <h3>{searchTerm ? t('orders.noResults') : t('orders.noOrders')}</h3>
          </div>
        ) : (
          <div className="pedidos-grid">
            {filteredPedidos.map((pedido) => (
              <div key={pedido.id} className="pedido-card">
                <div className="pedido-header">
                  <div className="pedido-id">
                    <span className="label">{t('orders.order')}</span>
                    <span className="value">#{pedido.id}</span>
                  </div>
                  <span className={`badge badge-${pedido.estado}`}>
                    {getStatusLabel(pedido.estado)}
                  </span>
                </div>

                <div className="pedido-body">
                  <div className="info-row">
                    <span className="icon">👤</span>
                    <div className="info-content">
                      <span className="label">{t('common.client')}</span>
                      <span className="value">{pedido.cliente_nombre || "N/A"}</span>
                    </div>
                  </div>
                  <div className="info-row">
                    <span className="icon">🏪</span>
                    <div className="info-content">
                      <span className="label">{t('common.store')}</span>
                      <span className="value">{pedido.tienda_nombre || "N/A"}</span>
                    </div>
                  </div>
                  <div className="info-row">
                    <span className="icon">💰</span>
                    <div className="info-content">
                      <span className="label">{t('common.total')}</span>
                      <span className="value total">${Number(pedido.total).toFixed(2)}</span>
                    </div>
                  </div>
                  <div className="info-row">
                    <span className="icon">📅</span>
                    <div className="info-content">
                      <span className="label">{t('common.date')}</span>
                      <span className="value">
                        {new Date(pedido.fecha_creacion).toLocaleString()}
                      </span>
                    </div>
                  </div>
                  {pedido.notas && (
                    <div className="info-row">
                        <span className="icon">📝</span>
                        <div className="info-content">
                            <span className="label">{t('common.notes')}</span>
                            <span className="value">{pedido.notas}</span>
                        </div>
                    </div>
                  )}
                </div>

                <div className="pedido-actions">
                  <button 
                    className="btn-action btn-detalle"
                    onClick={() => setSelectedPedido(pedido)}
                    style={{ background: '#64748b', color: 'white', marginRight: '8px' }}
                  >
                    👁️ {t('orders.actions.viewDetails')}
                  </button>
                  {renderActions(pedido)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedPedido && (
        <ModalDetallePedido
          pedido={selectedPedido}
          onClose={() => setSelectedPedido(null)}
        />
      )}
    </div>
  );
}
