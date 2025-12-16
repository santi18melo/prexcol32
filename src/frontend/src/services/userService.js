// src/services/userService.js
import { axiosInstance } from "./api";

/**
 * UserService - Service for user profile and management
 * Base URL: /usuarios/
 */

const UserService = {
  /**
   * Get current user profile
   */
  async getProfile() {
    try {
      const response = await axiosInstance.get("/usuarios/me/");
      return response.data;
    } catch (error) {
      console.error("Error fetching user profile:", error);
      throw error;
    }
  },

  /**
   * Update current user profile
   */
  async updateProfile(profileData) {
    try {
      const isFormData = profileData instanceof FormData;
      const config = isFormData ? { headers: { "Content-Type": "multipart/form-data" } } : {};
      
      const response = await axiosInstance.patch("/usuarios/me/", profileData, config);
      return response.data;
    } catch (error) {
      console.error("Error updating user profile:", error);
      throw error;
    }
  },

  /**
   * Get all users (Admin only)
   * @param {Object} params - search, page, etc
   * @returns {Promise<Object>} { meta, results: [...] }
   */
  async getAllUsers(params = {}) {
    try {
      const response = await axiosInstance.get("/usuarios/", { params });
      // Return full response for pagination
      return response.data;
    } catch (error) {
      console.error("Error fetching users:", error);
      throw error;
    }
  },

  /**
   * Get all active providers (Admin only)
   * Now paginated in backend.
   */
  async getProveedores(params = {}) {
    try {
      const response = await axiosInstance.get("/usuarios/proveedores/", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching providers:", error);
      throw error;
    }
  },

  /**
   * Create a new user (Admin only)
   */
  async createUser(userData) {
    try {
      const response = await axiosInstance.post("/usuarios/", userData);
      return response.data;
    } catch (error) {
      console.error("Error creating user:", error);
      throw error;
    }
  },

  /**
   * Update a user (Admin only)
   */
  async updateUser(userId, userData) {
    try {
        const response = await axiosInstance.patch(`/usuarios/${userId}/`, userData);
        return response.data;
    } catch (error) {
        console.error(`Error updating user ${userId}:`, error);
        throw error;
    }
  },

  /**
   * Delete a user (Admin only)
   */
  async deleteUser(userId) {
    try {
        await axiosInstance.delete(`/usuarios/${userId}/`);
        return true;
    } catch (error) {
        console.error(`Error deleting user ${userId}:`, error);
        throw error;
    }
  },

  /**
   * Change user password
   * @param {Object} passwordData - { old_password, new_password }
   */
  async changePassword(passwordData) {
    try {
      const response = await axiosInstance.post("/usuarios/change-password/", passwordData);
      return response.data;
    } catch (error) {
      console.error("Error changing password:", error);
      throw error;
    }
  },

  /**
   * Deactivate current user account
   */
  async deactivateAccount() {
    try {
      const response = await axiosInstance.post("/usuarios/deactivate/");
      return response.data;
    } catch (error) {
      console.error("Error deactivating account:", error);
      throw error;
    }
  },
};

export default UserService;
