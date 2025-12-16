// src/services/invoiceService.js
import { axiosInstance } from "./api";

const InvoiceService = {
  /**
   * Obtener factura por ID de pedido
   */
  async getByOrderId(pedidoId) {
    try {
      const response = await axiosInstance.get(`/productos/pedidos/${pedidoId}/ver_factura/`);
      return response.data;
    } catch (error) {
      // Ignorar 404 (no existe factura)
      if (error.response && error.response.status === 404) return null;
      console.error("Error fetching invoice:", error);
      throw error;
    }
  },

  /**
   * Crear nueva factura para un pedido
   */
  async createInvoice(pedidoId) {
    try {
      // Usamos una acción directa sobre el pedido para generar su factura
      const response = await axiosInstance.post(`/productos/pedidos/${pedidoId}/generar_factura/`);
      return response.data;
    } catch (error) {
       console.error("Error creating invoice:", error);
       throw error;
    }
  }
};

export default InvoiceService;
