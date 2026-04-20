/**
 * Cleitinho TI - Main JavaScript
 * Utility functions and UI components
 */

// Toast notification system
const toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 4000) {
        this.init();

        const toastEl = document.createElement('div');
        toastEl.className = `toast ${type}`;
        toastEl.innerHTML = `
            <i class="fas ${this.getIcon(type)}"></i>
            <span>${message}</span>
        `;

        this.container.appendChild(toastEl);

        setTimeout(() => {
            toastEl.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toastEl.remove(), 300);
        }, duration);
    },

    getIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle',
        };
        return icons[type] || icons.info;
    },

    success(message) { this.show(message, 'success'); },
    error(message) { this.show(message, 'error'); },
    warning(message) { this.show(message, 'warning'); },
    info(message) { this.show(message, 'info'); },
};

// Confirmation modal
function confirmAction(message, onConfirm) {
    const modal = document.createElement('div');
    modal.className = 'modal-backdrop';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.zIndex = '9999';

    modal.innerHTML = `
        <div class="modal-content" style="max-width: 400px; background: white; padding: 1.5rem; border-radius: 0.75rem;">
            <div class="modal-header" style="border: none; padding: 0 0 1rem 0;">
                <h5 class="modal-title">Confirmação</h5>
            </div>
            <div class="modal-body" style="padding: 0 0 1.5rem 0;">
                <p style="margin: 0;">${message}</p>
            </div>
            <div class="modal-footer" style="border: none; padding: 0; gap: 0.5rem; display: flex; justify-content: flex-end;">
                <button class="btn btn-outline-secondary cancel-btn">Cancelar</button>
                <button class="btn btn-danger confirm-btn">Confirmar</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    const close = () => modal.remove();

    modal.querySelector('.cancel-btn').addEventListener('click', close);
    modal.querySelector('.confirm-btn').addEventListener('click', () => {
        close();
        onConfirm();
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) close();
    });
}

// Sidebar toggle for mobile
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    sidebar?.classList.toggle('active');
    overlay?.classList.toggle('active');
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(value || 0);
}

// Format date
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    }).format(date);
}

// Format phone
function formatPhone(phone) {
    if (!phone) return '-';
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 11) {
        return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 7)}-${cleaned.slice(7)}`;
    } else if (cleaned.length === 10) {
        return `(${cleaned.slice(0, 2)}) ${cleaned.slice(2, 6)}-${cleaned.slice(6)}`;
    }
    return phone;
}

// Status badges
function getStatusBadge(status) {
    const statusMap = {
        'aberta': { label: 'Aberta', class: 'badge-status-open' },
        'em_andamento': { label: 'Em Andamento', class: 'badge-status-progress' },
        'aguardando_pecas': { label: 'Aguardando Peças', class: 'badge-status-progress' },
        'concluida': { label: 'Concluída', class: 'badge-status-completed' },
        'cancelada': { label: 'Cancelada', class: 'badge-status-cancelled' },
    };
    const s = statusMap[status] || { label: status, class: '' };
    return `<span class="badge ${s.class}">${s.label}</span>`;
}

// Search functionality
function setupSearch(inputId, callback, debounceMs = 300) {
    const input = document.getElementById(inputId);
    if (!input) return;

    let timeout;
    input.addEventListener('input', (e) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            callback(e.target.value);
        }, debounceMs);
    });
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const inputs = form.querySelectorAll('[required]');

    inputs.forEach((input) => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Clear form
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.reset();
    form.querySelectorAll('.is-invalid').forEach((el) => {
        el.classList.remove('is-invalid');
    });
}

// Loading state
function setLoading(buttonId, loading) {
    const btn = document.getElementById(buttonId);
    if (!btn) return;

    if (loading) {
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML = '<span class="loading-spinner"></span> Carregando...';
        btn.disabled = true;
    } else {
        btn.innerHTML = btn.dataset.originalText || btn.innerHTML;
        btn.disabled = false;
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    // Create sidebar overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.addEventListener('click', toggleSidebar);
    document.body.appendChild(overlay);

    // Set active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach((link) => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Export functions
window.toast = toast;
window.confirmAction = confirmAction;
window.toggleSidebar = toggleSidebar;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.formatPhone = formatPhone;
window.getStatusBadge = getStatusBadge;
window.setupSearch = setupSearch;
window.validateForm = validateForm;
window.clearForm = clearForm;
window.setLoading = setLoading;