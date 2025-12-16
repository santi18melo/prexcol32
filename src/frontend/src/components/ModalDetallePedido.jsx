import React, { useEffect, useState } from 'react';
import { useTranslation } from '../context/I18nContext';
import OrderService from '../services/orderService';
import InvoiceService from '../services/invoiceService';
import '../styles/ModalEdicion.css';

export default function ModalDetallePedido({ pedido, onClose, showStatusChange = false, onStatusChange }) {
  const { t } = useTranslation();
  const [detalles, setDetalles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentStatus, setCurrentStatus] = useState(pedido?.estado);
  const [invoice, setInvoice] = useState(null);

  useEffect(() => {
    if (pedido) {
      cargarDetalles();
      cargarFactura();
      setCurrentStatus(pedido.estado);
    }
  }, [pedido]);

  const cargarDetalles = async () => {
    setLoading(true);
    try {
      const data = await OrderService.getOrderDetailsItems(pedido.id);
      // Handle both array and paginated response
      const items = Array.isArray(data) ? data : (data.results || []);
      setDetalles(Array.isArray(items) ? items : []);
    } catch (err) {
      console.error("Error cargando detalles:", err);
      setError(t('errors.loadingOrders'));
    } finally {
      setLoading(false);
    }
  };

  const cargarFactura = async () => {
      try {
          const fact = await InvoiceService.getByOrderId(pedido.id);
          setInvoice(fact);
      } catch (e) {
          // Silent error or log
          console.log("Invoice info not available or error:", e);
      }
  };

  // Helper para traducir estados
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

  const handleStatusChange = (e) => {
      const newStatus = e.target.value;
      setCurrentStatus(newStatus);
      if (onStatusChange) {
          onStatusChange(pedido.id, newStatus);
      }
  };

  const handleDownloadInvoice = () => {
      if (invoice && invoice.archivo_pdf) {
          let url = invoice.archivo_pdf;
          // Force absolute URL to backend if not already
          if (!url.startsWith('http')) {
             url = `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
          }
          window.open(url, '_blank');
      } else {
          alert(t('orders.invoiceNotAvailable'));
      }
  };

  const handleShare = async () => {
      if (!invoice || !invoice.archivo_pdf) {
           alert(t('orders.invoiceNotAvailable'));
           return;
      }
       
      let url = invoice.archivo_pdf;
      if (!url.startsWith('http')) {
           url = `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
      }

      const shareData = {
           title: `${t('common.invoice')} ${invoice.numero_factura || 'Prex Col'}`,
           text: t('messages.shareMessage', { id: pedido.id, url }),
           url: url
      };

      try {
           if (navigator.share) {
               await navigator.share(shareData);
           } else {
               await navigator.clipboard.writeText(url);
               alert(t('messages.linkCopied'));
           }
      } catch (err) {
           console.error("Error al compartir:", err);
      }
  };

  const handleWhatsAppShare = () => {
      if (!invoice || !invoice.archivo_pdf) return;
      const url = getFullUrl(invoice.archivo_pdf);
      const text = t('messages.shareMessage', { id: pedido.id, url });
      window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
  };

  const handleSupport = () => {
      // Emergency support
      const message = t('messages.emergencyMessage', { id: pedido.id });
      window.open(`https://wa.me/573246648181?text=${encodeURIComponent(message)}`, '_blank');
  };

  if (!pedido) return null;

  const formatDate = (dateString) => {
      if (!dateString) return 'Pendiente';
      const date = new Date(dateString);
      return isNaN(date.getTime()) ? 'Fecha inválida' : date.toLocaleString();
  };

  const handleGenerarFactura = async () => {
      try {
          alert(t('orders.invoiceGenerating'));
          const newInvoice = await InvoiceService.createInvoice(pedido.id);
          setInvoice(newInvoice);
          alert(t('orders.invoiceGenerated'));
      } catch (e) {
          console.error(e);
          alert(t('errors.generic') + ": " + (e.response?.data?.error || e.message));
      }
  };

  return (
    <div className="modal-overlay" onClick={onClose} style={{color: 'black'}}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px', color: 'black' }}>
        
        <div className="modal-header" style={{ borderBottom: '1px solid #e2e8f0', paddingBottom: '15px', marginBottom: '15px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{color: '#1e293b', margin: 0, fontSize: '1.5rem', fontWeight: '800'}}>📦 {t('orders.orderDetail', { id: pedido.id })}</h2>
          <button className="modal-close" onClick={onClose} style={{color: '#64748b', fontSize: '1.5rem', background: 'none', border: 'none', cursor: 'pointer'}}>✕</button>
        </div>

        <div className="modal-body" style={{ padding: '0 20px 20px', color: 'black' }}>
          {/* Info General */}
          <div style={{ marginBottom: '20px', padding: '15px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
             <p style={{color: 'black'}}><strong>{t('common.client')}:</strong> {pedido.cliente_nombre || (pedido.cliente && pedido.cliente.nombre) || 'N/D'}</p>
             <p style={{color: 'black'}}><strong>{t('common.store')}:</strong> {pedido.tienda_nombre || (pedido.tienda && pedido.tienda.nombre) || 'N/D'}</p>
             <p style={{color: 'black'}}><strong>{t('orders.requestDate')}:</strong> {formatDate(pedido.fecha_creacion)}</p>
             {pedido.estado === 'entregado' ? (
               <p style={{color: '#10b981'}}><strong>{t('orders.deliveryDate')}:</strong> {formatDate(pedido.fecha_actualizacion)}</p>
             ) : (
                <p style={{color: 'black'}}><strong>{t('orders.lastUpdate')}:</strong> {formatDate(pedido.fecha_actualizacion)}</p>
             )}
             <div style={{marginTop: '10px', color: 'black'}}>
                 <strong>{t('common.status')}:</strong> 
                 {showStatusChange ? (
                     <select 
                        value={currentStatus} 
                        onChange={handleStatusChange}
                        style={{marginLeft: '10px', padding: '4px', borderRadius: '4px', border: '1px solid #cbd5e1', color: 'black'}}
                     >
                        <option value="pendiente">{t('orders.status.pending')}</option>
                        <option value="preparando">{t('orders.status.preparing')}</option>
                        <option value="en_transito">{t('orders.status.inTransit')}</option>
                        <option value="entregado">{t('orders.status.delivered')}</option>
                        <option value="cancelado">{t('orders.status.cancelled')}</option>
                     </select>
                 ) : (
                    <span className={`badge badge-${pedido.estado}`} style={{marginLeft: '5px'}}>{getStatusLabel(pedido.estado)}</span>
                 )}
             </div>
             {pedido.notas && <p style={{marginTop: '10px', color: 'black'}}><strong>{t('common.notes')}:</strong> {pedido.notas}</p>}
          </div>

          {/* Lista de Productos */}
          <h3 style={{color: 'black', borderBottom: '2px solid #e2e8f0', paddingBottom: '10px', marginBottom: '15px'}}>{t('products.title')}</h3>
          {loading ? (
            <p style={{color: 'black'}}>{t('common.loading')}</p>
          ) : error ? (
            <p className="error-text">{error}</p>
          ) : (
            <div className="detalles-list" style={{ maxHeight: '300px', overflowY: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', color: 'black' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid #e2e8f0', textAlign: 'left', background: '#f1f5f9' }}>
                    <th style={{ padding: '10px', color: '#334155' }}>{t('common.product')}</th>
                    <th style={{ padding: '10px', color: '#334155' }}>{t('common.quantity')}</th>
                    <th style={{ padding: '10px', color: '#334155' }}>{t('common.price')}</th>
                    <th style={{ padding: '10px', color: '#334155' }}>{t('common.subtotal')}</th>
                  </tr>
                </thead>
                <tbody>
                  {detalles.map((detalle) => (
                    <tr key={detalle.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '10px', color: 'black' }}>{detalle.producto_nombre || detalle.producto}</td>
                      <td style={{ padding: '10px', color: 'black' }}>{detalle.cantidad}</td>
                      <td style={{ padding: '10px', color: 'black' }}>${Number(detalle.precio_unitario).toFixed(2)}</td>
                      <td style={{ padding: '10px', color: 'black' }}>${(Number(detalle.precio_unitario) * detalle.cantidad).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                    <tr style={{ borderTop: '2px solid #e2e8f0', fontWeight: 'bold', background: '#f8fafc' }}>
                        <td colSpan="3" style={{ padding: '10px', textAlign: 'right', color: 'black' }}>{t('common.total')}:</td>
                        <td style={{ padding: '10px', color: 'black' }}>${Number(pedido.total).toFixed(2)}</td>
                    </tr>
                </tfoot>
              </table>
            </div>
          )}
        </div>

        <div className="modal-actions" style={{ padding: '20px', borderTop: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
              <div>
                  {invoice ? (
                      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                        <button className="btn-primary" onClick={handleDownloadInvoice} style={{ background: '#48bb78', borderColor: '#48bb78', padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                            📄 <span style={{fontSize: '0.9rem'}}>{t('orders.actions.viewInvoice')}</span>
                        </button>
                        <button className="btn-primary" onClick={handleWhatsAppShare} style={{ background: '#25D366', borderColor: '#25D366', padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                            💬 <span style={{fontSize: '0.9rem'}}>{t('orders.actions.shareWhatsApp')}</span>
                        </button>
                        <button className="btn-primary" onClick={handleShare} style={{ background: '#3b82f6', borderColor: '#3b82f6', padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                            🔗 <span style={{fontSize: '0.9rem'}}>{t('orders.actions.copyLink')}</span>
                        </button>
                      </div>
                  ) : (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <span style={{ color: '#64748b', fontStyle: 'italic', fontSize: '0.9rem' }}>{t('orders.invoiceNotAvailable')}</span>
                          {pedido.estado === 'entregado' && (
                            <button className="btn-secondary" onClick={handleGenerarFactura} style={{ fontSize: '0.9rem', padding: '6px 12px' }}>
                                {t('orders.actions.generateInvoice')}
                            </button>
                          )}
                      </div>
                  )}
              </div>
              <button className="btn-cancel" onClick={onClose} style={{ padding: '8px 16px' }}>
                {t('common.close')}
              </button>
          </div>

          <button 
                onClick={handleSupport}
                style={{ 
                    background: '#fee2e2', 
                    border: '1px solid #ef4444', 
                    color: '#dc2626', 
                    padding: '10px', 
                    borderRadius: '6px',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '10px',
                    width: '100%'
                }}
          >
                🆘 {t('orders.actions.contactSupport')}
          </button>
        </div>
      </div>
    </div>
  );
}
