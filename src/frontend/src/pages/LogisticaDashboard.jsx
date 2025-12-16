// frontend/src/pages/LogisticaDashboard.jsx - PROFESSIONAL & COMPLETE (v2.1)
import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import OrderService from "../services/orderService";
import ModalDetallePedido from "../components/ModalDetallePedido";
import DashboardHeader from "../components/DashboardHeader";
import "../styles/LogisticaDashboard.css";

export default function LogisticaDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("todos");
  const [selectedPedido, setSelectedPedido] = useState(null);

  // Force fetching from the new unified endpoint
  const cargarPedidos = useCallback(async () => {
    setLoading(true);
    console.log("🔄 LogisticaDashboard: Cargando pedidos desde panel unificado...");
    try {
      const data = await OrderService.getLogisticsPanelOrders();
      console.log("✅ Datos recibidos:", data);
      
      const pedidosData = data.results || data;
      setPedidos(Array.isArray(pedidosData) ? pedidosData : []);
      setError("");
    } catch (err) {
      console.error("❌ Error cargando pedidos:", err);
      setError("Error al cargar pedidos. Intente actualizar.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    console.log("🚀 LogisticaDashboard MOUNTED");
    cargarPedidos();
  }, [cargarPedidos]);

  const handleCambiarEstado = async (pedidoId, nuevoEstado) => {
    if (!window.confirm(`¿Cambiar pedido #${pedidoId} a "${nuevoEstado}"?`)) return;

    try {
      await OrderService.updateOrderStatus(pedidoId, nuevoEstado);
      setSuccess(`✓ Pedido #${pedidoId} actualizado`);
      await cargarPedidos();
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      setError(err.response?.data?.error || "Error al cambiar estado");
      setTimeout(() => setError(""), 5000);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const pedidosFiltrados = pedidos.filter((p) => {
    if (filtroEstado === "todos") return true;
    return p.estado === filtroEstado;
  });

  const stats = {
    total: pedidos.length,
    pendientes: pedidos.filter((p) => p.estado === "pendiente").length,
    preparando: pedidos.filter((p) => p.estado === "preparando").length,
    enTransito: pedidos.filter((p) => p.estado === "en_transito").length,
    entregados: pedidos.filter((p) => p.estado === "entregado").length,
  };

  if (loading && pedidos.length === 0) {
    return (
      <div className="logistica-dashboard">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Cargando centro de operaciones...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="logistica-dashboard">
      <DashboardHeader title="🚚 Centro de Operaciones Logísticas" />

      {error && <div className="alert alert-error"><span>⚠️</span> {error}</div>}
      {success && <div className="alert alert-success"><span>✓</span> {success}</div>}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📦</div>
          <div className="stat-content">
            <h3>{stats.pendientes}</h3>
            <p>Pendientes</p>
            <span className="stat-detail">Por procesar</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⚙️</div>
          <div className="stat-content">
            <h3>{stats.preparando}</h3>
            <p>Preparando</p>
            <span className="stat-detail">En proceso</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🚚</div>
          <div className="stat-content">
            <h3>{stats.enTransito}</h3>
            <p>En Tránsito</p>
            <span className="stat-detail">En ruta</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{stats.entregados}</h3>
            <p>Historial Entregas</p>
            <span className="stat-detail">Completados</span>
          </div>
        </div>
      </div>

      <div className="filtros-container">
        <div className="filtros">
          <button className={`filtro-btn ${filtroEstado === "todos" ? "active" : ""}`} onClick={() => setFiltroEstado("todos")}>
            Todos ({pedidos.length})
          </button>
           <button className={`filtro-btn ${filtroEstado === "pendiente" ? "active" : ""}`} onClick={() => setFiltroEstado("pendiente")}>
            Pendientes ({stats.pendientes})
          </button>
          <button className={`filtro-btn ${filtroEstado === "preparando" ? "active" : ""}`} onClick={() => setFiltroEstado("preparando")}>
            Preparando ({stats.preparando})
          </button>
          <button className={`filtro-btn ${filtroEstado === "en_transito" ? "active" : ""}`} onClick={() => setFiltroEstado("en_transito")}>
            En Tránsito ({stats.enTransito})
          </button>
          <button className={`filtro-btn ${filtroEstado === "entregado" ? "active" : ""}`} onClick={() => setFiltroEstado("entregado")}>
            Historial ({stats.entregados})
          </button>
        </div>
      </div>

      <div className="pedidos-container">
        <div className="section-header">
          <h2><span key={filtroEstado}>{filtroEstado === 'entregado' ? 'Historial de Pedidos' : 'Gestión de Envíos'}</span></h2>
          <button onClick={cargarPedidos} className="btn-refresh">🔄 Actualizar</button>
        </div>

        {pedidosFiltrados.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <h3>No hay pedidos en esta sección</h3>
          </div>
        ) : (
          <div className="pedidos-grid">
            {pedidosFiltrados.map((pedido) => (
              <div key={pedido.id} className={`pedido-card ${pedido.estado}`}>
                <div className="pedido-header">
                  <div className="pedido-id">
                    <span className="label">Pedido</span>
                    <span className="value">#{pedido.id}</span>
                  </div>
                  <span className={`badge badge-${pedido.estado}`}>{pedido.estado}</span>
                </div>
                <div className="pedido-body">
                  <div className="info-row">
                    <span className="icon">👤</span>
                    <div className="info-content">
                      <span className="label">Cliente</span>
                      <span className="value">{pedido.cliente_nombre || "N/A"}</span>
                    </div>
                  </div>
                  <div className="info-row">
                    <div className="info-content" style={{width: '100%'}}>
                       <div style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem', marginBottom:'4px'}}>
                          <span>📅 Solicitud:</span>
                          <strong>{new Date(pedido.fecha_creacion).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} {new Date(pedido.fecha_creacion).toLocaleDateString()}</strong>
                       </div>
                       {pedido.estado === 'entregado' && (
                           <div style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem', color:'#10b981'}}>
                              <span>🏁 Entrega:</span>
                              <strong>{new Date(pedido.fecha_actualizacion).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} {new Date(pedido.fecha_actualizacion).toLocaleDateString()}</strong>
                           </div>
                       )}
                    </div>
                  </div>
                  <div className="info-row">
                    <span className="icon">💰</span>
                    <div className="info-content">
                      <span className="label">Total</span>
                      <span className="value total">${Number(pedido.total).toFixed(2)}</span>
                    </div>
                  </div>
                </div>
                <div className="pedido-actions">
                  <button className="btn-action btn-secondary" onClick={() => setSelectedPedido(pedido)}>
                    👁️ Ver Detalles
                  </button>
                  
                  {pedido.estado === "pendiente" && (
                     <button className="btn-action btn-primary" onClick={() => handleCambiarEstado(pedido.id, "preparando")}>
                       ⚙️ Preparar
                     </button>
                  )}
                  {pedido.estado === "preparando" && (
                    <button className="btn-action btn-transito" onClick={() => handleCambiarEstado(pedido.id, "en_transito")}>
                      🚚 Enviar
                    </button>
                  )}
                  {pedido.estado === "en_transito" && (
                    <button className="btn-action btn-entregado" onClick={() => handleCambiarEstado(pedido.id, "entregado")}>
                      ✓ Entregado
                    </button>
                  )}
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
          showStatusChange={true} // Allow manual override in modal too
          onStatusChange={async (id, status) => {
             await handleCambiarEstado(id, status);
             setSelectedPedido(null); // Close or update modal
          }}
        />
      )}
    </div>
  );
}
