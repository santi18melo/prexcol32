// src/services/orderService.js
import { axiosInstance } from "./api";

/**
 * OrderService - Service for order-related API calls
 * Base URL: /productos/pedidos/
 */

const OrderService = {
  /**
   * Create a new order
   * @param {Object} orderData - { tienda_id, detalles, notas, ... }
   */
  async createOrder(orderData) {
    try {
      const response = await axiosInstance.post("/productos/pedidos/crear_pedido/", orderData);
      return response.data;
    } catch (error) {
      console.error("Error creating order:", error);
      throw error;
    }
  },

  /**
   * Get user's order history
   * @param {Object} params - Pagination params
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async getMyOrders(params = {}) {
    try {
      const response = await axiosInstance.get("/productos/pedidos/mis_pedidos/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching my orders:", error);
      throw error;
    }
  },

  /**
   * Get all orders (Admin)
   */
  async getAllOrders(params = {}) {
    try {
      const response = await axiosInstance.get("/productos/pedidos/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching all orders:", error);
      throw error;
    }
  },

  /**
   * Get order details by ID
   */
  async getOrder(orderId) {
    try {
      const response = await axiosInstance.get(`/productos/pedidos/${orderId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching order ${orderId}:`, error);
      throw error;
    }
  },

  /**
   * Update order status
   */
  async updateOrderStatus(orderId, newStatus) {
    try {
      const response = await axiosInstance.post(
        `/productos/pedidos/${orderId}/cambiar_estado/`,
        { estado: newStatus }
      );
      return response.data;
    } catch (error) {
      console.error(`Error updating order ${orderId} status:`, error);
      throw error;
    }
  },
  
  // Alias
  async cambiarEstadoPedido(pedidoId, nuevoEstado) {
      return this.updateOrderStatus(pedidoId, nuevoEstado);
  },

  /**
   * Get pending orders (Buyer/Comprador dashboard?)
   * Note: The backend endpoint name is 'pendientes'
   */
  async getPendingOrders(params = {}) {
    try {
      const response = await axiosInstance.get("/productos/pedidos/pendientes/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching pending orders:", error);
      throw error;
    }
  },

  /**
   * Get orders in preparation (Logistics)
   */
  async getOrdersInPreparation(params = {}) {
    try {
      const response = await axiosInstance.get("/productos/pedidos/en_preparacion/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching orders in preparation:", error);
      throw error;
    }
  },

  /**
   * Get all logistics orders (Consolidated panel)
   */
  async getLogisticsPanelOrders(params = {}) {
    try {
      const response = await axiosInstance.get("/productos/pedidos/panel_logistica/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching logistics panel orders:", error);
      throw error;
    }
  },

  /**
   * Get order details items
   * Typically the order object includes details, but there is an endpoint too.
   */
  async getOrderDetailsItems(pedidoId) {
    try {
      const response = await axiosInstance.get("/productos/detalles-pedido/por_pedido/", {
          params: { pedido_id: pedidoId }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching details for order ${pedidoId}:`, error);
      throw error;
    }
  },
};

export default OrderService;
