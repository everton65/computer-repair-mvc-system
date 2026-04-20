/**
 * Cleitinho TI - API Client
 * Handles all communication with the backend API
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

const api = {
    /**
     * Make a request to the API
     */
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Erro na requisição');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // GET request
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    // POST request
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // PUT request
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // DELETE request
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },

    // Clientes
    clientes: {
        getAll: (search) => {
            const query = search ? `?search=${encodeURIComponent(search)}` : '';
            return api.get(`/clientes/${query}`);
        },
        getById: (id) => api.get(`/clientes/${id}`),
        create: (data) => api.post('/clientes/', data),
        update: (id, data) => api.put(`/clientes/${id}`, data),
        delete: (id) => api.delete(`/clientes/${id}`),
    },

    // Peças
    pecas: {
        getAll: (search) => {
            const query = search ? `?search=${encodeURIComponent(search)}` : '';
            return api.get(`/pecas/${query}`);
        },
        getById: (id) => api.get(`/pecas/${id}`),
        create: (data) => api.post('/pecas/', data),
        update: (id, data) => api.put(`/pecas/${id}`, data),
        delete: (id) => api.delete(`/pecas/${id}`),
    },

    // Serviços
    servicos: {
        getAll: (clienteId) => {
            const query = clienteId ? `?cliente_id=${clienteId}` : '';
            return api.get(`/servicos/${query}`);
        },
        getById: (id) => api.get(`/servicos/${id}`),
        create: (data) => api.post('/servicos/', data),
        update: (id, data) => api.put(`/servicos/${id}`, data),
        delete: (id) => api.delete(`/servicos/${id}`),
    },

    // Ordens de Serviço
    ordens: {
        getAll: (filters) => {
            const params = new URLSearchParams();
            if (filters?.cliente_id) params.append('cliente_id', filters.cliente_id);
            if (filters?.status) params.append('status', filters.status);
            const query = params.toString() ? `?${params.toString()}` : '';
            return api.get(`/ordens/${query}`);
        },
        getById: (id) => api.get(`/ordens/${id}`),
        create: (data) => api.post('/ordens/', data),
        update: (id, data) => api.put(`/ordens/${id}`, data),
        delete: (id) => api.delete(`/ordens/${id}`),
    },

    // Relatórios
    relatorios: {
        dashboard: () => api.get('/relatorios/dashboard'),
        clientes: () => api.get('/relatorios/clientes'),
        servicos: () => api.get('/relatorios/servicos'),
        pecas: () => api.get('/relatorios/pecas'),
        ordens: (status) => {
            const query = status ? `?status=${status}` : '';
            return api.get(`/relatorios/ordens${query}`);
        },
    },
};

// Export for use in other files
window.api = api;