// src/services/paymentService.js
import { axiosInstance } from "./api";

/**
 * PaymentService - Service for payment-related API calls
 * Base URL: /pagos/pagos/
 */

const PaymentService = {
  /**
   * Get available payment methods
   * @param {Object} params - params
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async getPaymentMethods(params = {}) {
    try {
      const response = await axiosInstance.get("/pagos/metodos-pago/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching payment methods:", error);
      throw error;
    }
  },

  /**
   * Create a new payment
   * @param {Object} paymentData - Payment data { pedido, monto, estado, metodo_pago }
   */
  async createPayment(paymentData) {
    try {
      const response = await axiosInstance.post("/pagos/pagos/", paymentData);
      return response.data;
    } catch (error) {
      console.error("Error creating payment:", error);
      throw error;
    }
  },

  /**
   * Get user's payment history
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async getPaymentHistory(params = {}) {
    try {
      const response = await axiosInstance.get("/pagos/pagos/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching payment history:", error);
      throw error;
    }
  },

  /**
   * Get payment details by ID
   */
  async getPayment(paymentId) {
    try {
      const response = await axiosInstance.get(`/pagos/pagos/${paymentId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching payment ${paymentId}:`, error);
      throw error;
    }
  },

  /**
   * Get payment status
   */
  async getPaymentStatus(paymentId) {
    try {
      const response = await axiosInstance.get(`/pagos/pagos/${paymentId}/estado/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching payment ${paymentId} status:`, error);
      throw error;
    }
  },

  /**
   * Register a transaction for a payment
   */
  async registerTransaction(transactionData) {
    try {
      const response = await axiosInstance.post("/pagos/pagos/transaccion/", transactionData);
      return response.data;
    } catch (error) {
      console.error("Error registering transaction:", error);
      throw error;
    }
  },
};

export default PaymentService;
