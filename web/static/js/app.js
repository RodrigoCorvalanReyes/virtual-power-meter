// Virtual Power Meter - Main JavaScript Application

class VirtualPowerMeterApp {
    constructor() {
        this.websocket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.updateStatusIndicator();
        this.startStatusPolling();
    }
    
    bindEvents() {
        // Page visibility handling
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.refreshStatus();
            }
        });
        
        // Connection status handling
        window.addEventListener('online', () => {
            this.refreshStatus();
        });
        
        window.addEventListener('offline', () => {
            this.updateStatusIndicator(false);
        });
    }
    
    // Status Management
    async refreshStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            this.updateStatusIndicator(data.is_running);
            return data;
        } catch (error) {
            console.error('Error fetching status:', error);
            this.updateStatusIndicator(false);
            return null;
        }
    }
    
    updateStatusIndicator(isRunning = null) {
        const indicator = document.getElementById('status-indicator');
        if (!indicator) return;
        
        if (isRunning === null) {
            indicator.innerHTML = '<span class="badge bg-warning"><i class="fas fa-circle me-1"></i>Verificando...</span>';
        } else if (isRunning) {
            indicator.innerHTML = '<span class="badge bg-success"><i class="fas fa-circle me-1"></i>Conectado</span>';
        } else {
            indicator.innerHTML = '<span class="badge bg-secondary"><i class="fas fa-circle me-1"></i>Desconectado</span>';
        }
    }
    
    startStatusPolling() {
        // Poll status every 10 seconds
        setInterval(() => {
            this.refreshStatus();
        }, 10000);
    }
    
    // WebSocket Management
    connectWebSocket() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            return;
        }
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = (event) => {
            console.log('WebSocket connected');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.onWebSocketOpen(event);
        };
        
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.onWebSocketMessage(data);
        };
        
        this.websocket.onclose = (event) => {
            console.log('WebSocket disconnected');
            this.isConnected = false;
            this.onWebSocketClose(event);
            this.attemptReconnect();
        };
        
        this.websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.onWebSocketError(error);
        };
    }
    
    disconnectWebSocket() {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
        }
        this.isConnected = false;
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.log('Max reconnection attempts reached');
            return;
        }
        
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
        
        console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
        
        setTimeout(() => {
            this.connectWebSocket();
        }, delay);
    }
    
    // WebSocket Event Handlers (to be overridden by pages)
    onWebSocketOpen(event) {
        // Override in specific pages
    }
    
    onWebSocketMessage(data) {
        // Override in specific pages
    }
    
    onWebSocketClose(event) {
        // Override in specific pages
    }
    
    onWebSocketError(error) {
        // Override in specific pages
    }
    
    // Utility Methods
    formatValue(value, dataType, decimals = 2) {
        if (Array.isArray(value)) {
            return value.map(v => this.formatValue(v, dataType, decimals)).join(', ');
        }
        
        if (typeof value === 'number') {
            if (dataType === 'FLOAT32') {
                return value.toFixed(decimals);
            } else {
                return value.toString();
            }
        }
        
        return value.toString();
    }
    
    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString();
    }
    
    showNotification(message, type = 'info', duration = 5000) {
        const toast = this.createToast(message, type);
        document.body.appendChild(toast);
        
        // Show toast
        const bsToast = new bootstrap.Toast(toast, {
            delay: duration
        });
        bsToast.show();
        
        // Remove from DOM after hiding
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
    
    createToast(message, type) {
        const toastId = 'toast-' + Date.now();
        const iconMap = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        };
        
        const colorMap = {
            'success': 'text-success',
            'error': 'text-danger',
            'warning': 'text-warning',
            'info': 'text-info'
        };
        
        const toast = document.createElement('div');
        toast.className = 'toast position-fixed top-0 end-0 m-3';
        toast.id = toastId;
        toast.style.zIndex = '9999';
        
        toast.innerHTML = `
            <div class="toast-header">
                <i class="${iconMap[type] || iconMap.info} ${colorMap[type] || colorMap.info} me-2"></i>
                <strong class="me-auto">Virtual Power Meter</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        return toast;
    }
    
    // API Helper Methods
    async apiRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const mergedOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    async startSimulator() {
        try {
            const data = await this.apiRequest('/api/start', { method: 'POST' });
            
            if (data.status === 'success') {
                this.showNotification(data.message, 'success');
                setTimeout(() => this.refreshStatus(), 1000);
            } else {
                this.showNotification(data.message, 'error');
            }
            
            return data;
        } catch (error) {
            this.showNotification('Error de conexión: ' + error.message, 'error');
            throw error;
        }
    }
    
    async stopSimulator() {
        try {
            const data = await this.apiRequest('/api/stop', { method: 'POST' });
            
            if (data.status === 'success') {
                this.showNotification(data.message, 'success');
                setTimeout(() => this.refreshStatus(), 1000);
            } else {
                this.showNotification(data.message, 'error');
            }
            
            return data;
        } catch (error) {
            this.showNotification('Error de conexión: ' + error.message, 'error');
            throw error;
        }
    }
    
    // Chart Helper Methods
    createRealtimeChart(ctx, config) {
        const defaultConfig = {
            type: 'line',
            data: {
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'realtime',
                        realtime: {
                            duration: 60000,
                            refresh: 2000,
                            delay: 1000,
                            onRefresh: config.onRefresh || function() {}
                        }
                    },
                    y: {
                        beginAtZero: false
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                }
            }
        };
        
        const mergedConfig = this.deepMerge(defaultConfig, config);
        return new Chart(ctx, mergedConfig);
    }
    
    deepMerge(target, source) {
        const output = Object.assign({}, target);
        if (this.isObject(target) && this.isObject(source)) {
            Object.keys(source).forEach(key => {
                if (this.isObject(source[key])) {
                    if (!(key in target))
                        Object.assign(output, { [key]: source[key] });
                    else
                        output[key] = this.deepMerge(target[key], source[key]);
                } else {
                    Object.assign(output, { [key]: source[key] });
                }
            });
        }
        return output;
    }
    
    isObject(item) {
        return item && typeof item === "object" && !Array.isArray(item);
    }
    
    // Local Storage Helpers
    saveToLocalStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.warn('Failed to save to localStorage:', error);
        }
    }
    
    loadFromLocalStorage(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.warn('Failed to load from localStorage:', error);
            return defaultValue;
        }
    }
    
    removeFromLocalStorage(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.warn('Failed to remove from localStorage:', error);
        }
    }
}

// Global instance
const app = new VirtualPowerMeterApp();

// Global helper functions for backward compatibility
window.startSimulator = () => app.startSimulator();
window.stopSimulator = () => app.stopSimulator();
window.refreshStatus = () => app.refreshStatus();

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VirtualPowerMeterApp;
}

// Make app available globally
window.VirtualPowerMeterApp = VirtualPowerMeterApp;
window.app = app;