// src/services/storeService.js
import { axiosInstance } from "./api";

/**
 * StoreService - Service for store/tienda related API calls
 * Base URL: /productos/tiendas/
 */

const StoreService = {
  /**
   * Get all active stores (public/auth)
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async listStores() {
    try {
      const response = await axiosInstance.get("/productos/tiendas/");
      return response.data;
    } catch (error) {
      console.error("Error fetching stores:", error);
      throw error;
    }
  },

  /**
   * Get stores managed by current user
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async getMyStores() {
    try {
      const response = await axiosInstance.get("/productos/tiendas/mis_tiendas/");
      return response.data;
    } catch (error) {
      console.error("Error fetching my stores:", error);
      throw error;
    }
  },

  /**
   * Get store detail
   * @param {number} storeId
   * @returns {Promise<Object>} Store object
   */
  async getStore(storeId) {
    try {
      const response = await axiosInstance.get(`/productos/tiendas/${storeId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching store ${storeId}:`, error);
      throw error;
    }
  },

  /**
   * Create new store
   * @param {Object} storeData
   */
  async createStore(storeData) {
    try {
      const response = await axiosInstance.post("/productos/tiendas/", storeData);
      return response.data;
    } catch (error) {
      console.error("Error creating store:", error);
      throw error;
    }
  },

  /**
   * Update store
   * @param {number} storeId
   * @param {Object} storeData
   */
  async updateStore(storeId, storeData) {
    try {
      const response = await axiosInstance.patch(`/productos/tiendas/${storeId}/`, storeData);
      return response.data;
    } catch (error) {
      console.error(`Error updating store ${storeId}:`, error);
      throw error;
    }
  },

  /**
   * Delete store
   * @param {number} storeId
   */
  async deleteStore(storeId) {
    try {
      await axiosInstance.delete(`/productos/tiendas/${storeId}/`);
      return true;
    } catch (error) {
      console.error(`Error deleting store ${storeId}:`, error);
      throw error;
    }
  },
};

export default StoreService;
