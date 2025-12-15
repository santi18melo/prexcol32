// src/services/productService.js
import { axiosInstance } from "./api";

/**
 * ProductService - Service for product-related API calls
 * Base URL: /productos/productos/
 */

const ProductService = {
  /**
   * Get all products (public access)
   * @param {Object} params - Query params (page, page_size, search, etc)
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async listProducts(params = {}) {
    try {
      const response = await axiosInstance.get("/productos/productos/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching products:", error);
      throw error;
    }
  },

  /**
   * Get products by store
   * @param {number} tiendaId
   * @param {Object} params
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async listProductsByStore(tiendaId, params = {}) {
    try {
      const response = await axiosInstance.get("/productos/productos/por_tienda/", {
        params: { tienda_id: tiendaId, ...params }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching products for store ${tiendaId}:`, error);
      throw error;
    }
  },

  /**
   * Get products for current provider
   */
  async getMyProducts(params = {}) {
    try {
      const response = await axiosInstance.get("/productos/productos/mis_productos/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching my products:", error);
      throw error;
    }
  },

  /**
   * Get product by ID
   * @param {number} productId
   */
  async getProduct(productId) {
    try {
      const response = await axiosInstance.get(`/productos/productos/${productId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching product ${productId}:`, error);
      throw error;
    }
  },

  /**
   * Search products by name (Helper)
   * @param {string} query
   */
  async searchProducts(query) {
    return this.listProducts({ search: query });
  },

  /**
   * Create new product (Admin only)
   */
  async createProduct(productData) {
    try {
      const response = await axiosInstance.post("/productos/productos/", productData);
      return response.data;
    } catch (error) {
      console.error("Error creating product:", error);
      throw error;
    }
  },

  /**
   * Update product
   */
  async updateProduct(productId, productData) {
    try {
      const response = await axiosInstance.put(`/productos/productos/${productId}/`, productData);
      return response.data;
    } catch (error) {
      console.error(`Error updating product ${productId}:`, error);
      throw error;
    }
  },

  /**
   * Delete product
   */
  async deleteProduct(productId) {
    try {
      await axiosInstance.delete(`/productos/productos/${productId}/`);
      return true;
    } catch (error) {
      console.error(`Error deleting product ${productId}:`, error);
      throw error;
    }
  },

  /**
   * Adjust Stock
   * @param {number} productId
   * @param {string} operacion - 'aumentar' | 'reducir'
   * @param {number} cantidad
   */
  async adjustStock(productId, operacion, cantidad) {
    try {
      const response = await axiosInstance.post(`/productos/productos/${productId}/ajustar_stock/`, {
        operacion,
        cantidad
      });
      return response.data;
    } catch (error) {
      console.error(`Error adjusting stock for ${productId}:`, error);
      throw error;
    }
  },

  /**
   * Upload Image
   */
  async uploadImage(productId, formData) {
    try {
      const response = await axiosInstance.post(`/productos/productos/${productId}/subir_imagen/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      console.error(`Error uploading image for ${productId}:`, error);
      throw error;
    }
  },

  /**
   * Assign Provider
   */
  async assignProvider(productId, proveedorId) {
    try {
      const response = await axiosInstance.post(`/productos/productos/${productId}/asignar_proveedor/`, {
        proveedor_id: proveedorId
      });
      return response.data;
    } catch (error) {
      console.error(`Error assigning provider for ${productId}:`, error);
      throw error;
    }
  },
};

export default ProductService;
