import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DashboardHeader from "../components/DashboardHeader";
import AdminUsersTab from "../components/admin/tabs/AdminUsersTab";
import AdminStoresTab from "../components/admin/tabs/AdminStoresTab";
import AdminProductsTab from "../components/admin/tabs/AdminProductsTab";
import AdminOrdersTab from "../components/admin/tabs/AdminOrdersTab";
import UserService from "../services/userService";
import ProductService from "../services/productService";
import StoreService from "../services/storeService";
import OrderService from "../services/orderService";
import SimpleChart from "../components/admin/SimpleChart";
import AdminCategoriesTab from "../components/admin/tabs/AdminCategoriesTab";
import LiveMetricsModal from "../components/admin/LiveMetricsModal";
import "../styles/dashboardAdmin.css";
import CategoryService from "../services/categoryService";

const tabs = [
  { id: "users", label: "Usuarios", Component: AdminUsersTab },
  { id: "stores", label: "Tiendas", Component: AdminStoresTab },
  { id: "products", label: "Productos", Component: AdminProductsTab },
  { id: "categories", label: "Categorías", Component: AdminCategoriesTab },
  { id: "orders", label: "Pedidos", Component: AdminOrdersTab },
];

export default function DashboardAdmin() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(tabs[0].id);
  
  // Data State
  const [users, setUsers] = useState([]);
  const [stores, setStores] = useState([]);
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [categories, setCategories] = useState([]);
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(false);

  // Stats State
  const [stats, setStats] = useState({ users: 0, stores: 0, products: 0, orders: 0, categories: 0 });

  // Fetch Data per Tab
  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
        if (activeTab === 'users') {
             const u = await UserService.getAllUsers();
             setUsers(u.results || u || []);
        } else if (activeTab === 'stores') {
             const t = await StoreService.listStores();
             setStores(t.results || t || []);
        } else if (activeTab === 'products') {
             const [p, t, prov, c] = await Promise.all([
                 ProductService.listProducts(),
                 StoreService.listStores(),
                 UserService.getProveedores(),
                 CategoryService.getAll()
             ]);
             setProducts(p.results || p || []);
             setStores(t.results || t || []);
             setProviders(prov.results || prov || []);
             setCategories(c || []); // CategoryService might need checking
        } else if (activeTab === 'categories') {
             const c = await CategoryService.getAll();
             setCategories(c.results || c || []);
        } else if (activeTab === 'orders') {
             const o = await OrderService.getAllOrders();
             setOrders(o.results || o || []);
        }
    } catch (error) {
        console.error("Error fetching dashboard data:", error);
    } finally {
        setLoading(false);
    }
  }, [activeTab]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Fetch Stats on Mount
  useEffect(() => {
    const loadStats = async () => {
        try {
            const [u, s, p, o, c] = await Promise.all([
                UserService.getAllUsers(),
                StoreService.listStores(),
                ProductService.listProducts(),
                OrderService.getAllOrders(),
                CategoryService.getAll()
            ]);
            setStats({
                users: u?.length || 0,
                stores: s?.length || 0,
                products: p?.length || 0,
                orders: o?.length || 0,
                categories: c?.length || 0
            });
        } catch (e) {
            console.error("Error loading stats:", e);
        }
    };
    loadStats();
  }, []);

  // Handlers
  // Helper helper to format errors
  const getErrorMessage = (error) => {
      if (error.response?.data) {
          const data = error.response.data;
          if (typeof data === 'string') return data;
          if (data.detail) return data.detail;
          
          // Combine all field errors
          return Object.entries(data)
              .map(([key, value]) => {
                  const message = Array.isArray(value) ? value.join(' ') : value;
                  // Capitalize field name
                  const fieldName = key.charAt(0).toUpperCase() + key.slice(1);
                  return `${fieldName}: ${message}`;
              })
              .join('\n');
      }
      return error.message || "Error desconocido";
  };

  const handleUserCreate = async (data) => {
    try {
        await UserService.createUser(data);
        await fetchData();
    } catch (error) {
        console.error("Failed to create user:", error);
        alert("Error al crear usuario:\n" + getErrorMessage(error));
    }
  };

  const handleUserUpdate = async (data) => {
    try {
        const { id, ...updateData } = data; // Separate ID from data
        await UserService.updateUser(id, updateData);
        await fetchData();
    } catch (error) {
        console.error("Failed to update user:", error);
        alert("Error al actualizar usuario:\n" + getErrorMessage(error));
    }
  };

   const handleUserDelete = async (id) => {
    if(!window.confirm("¿Estás seguro de eliminar este usuario?")) return;
    try {
        await UserService.deleteUser(id);
        await fetchData();
    } catch (error) {
        console.error("Failed to delete user:", error);
         alert("Error al eliminar usuario:\n" + getErrorMessage(error));
    }
  };
  
  const getComponentProps = () => {
      switch(activeTab) {
          case 'users':
              return { 
                  usuarios: users, 
                  loading, 
                  onCreate: handleUserCreate, 
                  onUpdate: handleUserUpdate, 
                  onDelete: handleUserDelete 
              };
          case 'stores':
              return { 
                  tiendas: stores, 
                  loading,
                  onCreate: async (d) => { await StoreService.createStore(d); fetchData(); },
                  onUpdate: async (d) => { await StoreService.updateStore(d.id, d); fetchData(); },
                  onDelete: async (id) => { await StoreService.deleteStore(id); fetchData(); }
              };
          case 'products':
              return { 
                  productos: products, 
                  loading,
                  tiendas: stores,
                  proveedores: providers,
                  categorias: categories,
                  onCreate: async (d) => { await ProductService.createProduct(d); fetchData(); },
                  onUpdate: async (d) => { await ProductService.updateProduct(d.id, d); fetchData(); },
                  onDelete: async (id) => { await ProductService.deleteProduct(id); fetchData(); }
              };
          case 'orders':
              return { 
                  pedidos: orders, 
                  loading,
                  onUpdate: async (d) => { await OrderService.updateOrderStatus(d.id, d.estado); fetchData(); }
              };
          case 'categories':
              return {
                  categorias: categories,
                  loading,
                  onCreate: async (d) => { await CategoryService.create(d); fetchData(); },
                  onUpdate: async (d) => { await CategoryService.update(d.id, d); fetchData(); },
                  onDelete: async (id) => { await CategoryService.delete(id); fetchData(); }
              };
          default:
              return {};
      }
  };

  const ActiveComponent = tabs.find(t => t.id === activeTab)?.Component || (() => <div>Tab not found</div>);
  const activeProps = getComponentProps();

  const [showMetrics, setShowMetrics] = useState(false);

  return (
    <div className="dashboard-admin">
      <DashboardHeader title="Panel de Administración" />
      
      {/* Overview Section: Stats + Quick Actions */}
      <div className="overview-section" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px', padding: '0 40px', marginBottom: '30px' }}>
          
          {/* Stats Grid */}
          <div className="stats-grid" style={{ padding: 0, margin: 0, gridTemplateColumns: 'repeat(2, 1fr)' }}>
             <div className="stat-card">
               <div className="stat-icon">👥</div>
               <div className="stat-content">
                 <h3>{stats.users}</h3>
                 <p>Usuarios</p>
                 <span className="stat-detail">Registrados</span>
               </div>
             </div>
             <div className="stat-card">
               <div className="stat-icon">🏪</div>
               <div className="stat-content">
                 <h3>{stats.stores}</h3>
                 <p>Tiendas</p>
                 <span className="stat-detail">Activas</span>
               </div>
             </div>
             <div className="stat-card">
               <div className="stat-icon">📦</div>
               <div className="stat-content">
                 <h3>{stats.products}</h3>
                 <p>Productos</p>
                 <span className="stat-detail">En catálogo</span>
               </div>
             </div>
             <div className="stat-card">
               <div className="stat-icon">🧾</div>
               <div className="stat-content">
                 <h3>{stats.orders}</h3>
                 <p>Pedidos</p>
                 <span className="stat-detail">Totales</span>
               </div>
             </div>
          </div>

          {/* Quick Actions & Charts */}
          <div className="actions-chart-column" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              
              {/* Quick Actions Card */}
              <div className="content-section" style={{ padding: '20px', borderRadius: '16px', animation: 'none' }}>
                  <h3 style={{ margin: '0 0 15px 0', fontSize: '1.1rem' }}>⚡ Acciones Rápidas</h3>
                  <button 
                    className="btn-primary" 
                    style={{ width: '100%', marginBottom: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}
                    onClick={() => navigate('/admin/asignar-productos')}
                  >
                    <span>🔗</span> Asignar Productos Masivo
                  </button>
                  <button 
                    className="btn-primary" 
                    style={{ width: '100%', background: '#fff', color: '#3182ce', border: '1px solid #3182ce' }}
                    onClick={() => setActiveTab('orders')}
                  >
                    <span>🧾</span> Ver Últimos Pedidos
                  </button>
              </div>

              {/* Activity Chart */}
              <div 
                className="content-section" 
                style={{ padding: '20px', borderRadius: '16px', animation: 'none', background: 'linear-gradient(135deg, #2b6cb0 0%, #2c5282 100%)', color: 'white', cursor: 'pointer' }}
                onClick={() => setShowMetrics(true)}
                title="Clic para ver métricas en tiempo real"
              >
                 <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                    <h3 style={{ margin: 0, fontSize: '1rem', color: 'white' }}>📈 Actividad Reciente</h3>
                    <span style={{ fontSize: '0.7rem', background: '#ffffff33', padding: '2px 6px', borderRadius: '4px' }}>🔴 EN VIVO</span>
                 </div>
                 <SimpleChart values={[3, 7, 5, 10, 8, 12, 9]} onClick={() => setShowMetrics(true)} />
              </div>

          </div>
      </div>
      
      <nav className="dashboard-admin__nav">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`dashboard-admin__tab ${activeTab === tab.id ? "active" : ""}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>
      <section className="dashboard-admin__content">
        <ActiveComponent {...activeProps} />
      </section>

      {/* Live Metrics Modal */}
      {showMetrics && <LiveMetricsModal onClose={() => setShowMetrics(false)} />}
    </div>
  );
}
