/**
 * Photo Upload Dialog Component
 * Upload de fotos de resultado de agendamentos
 * Com validação, preview e progress bar
 */

class PhotoUploadDialog {
    constructor(dialogId = 'photo-upload-dialog') {
        this.dialog = document.getElementById(dialogId);
        
        if (!this.dialog) {
            console.warn('Photo upload dialog not found');
            return;
        }
        
        this.fileInput = this.dialog.querySelector('#photo-input');
        this.preview = this.dialog.querySelector('#preview-image');
        this.placeholder = this.dialog.querySelector('#upload-placeholder');
        this.submitBtn = this.dialog.querySelector('#upload-submit-btn');
        this.progressContainer = this.dialog.querySelector('#upload-progress');
        this.progressFill = this.dialog.querySelector('#progress-fill');
        this.progressText = this.dialog.querySelector('#progress-text');
        this.fileInfo = this.dialog.querySelector('#file-info');
        this.fileName = this.dialog.querySelector('#file-name');
        this.fileSize = this.dialog.querySelector('#file-size');
        this.removeFileBtn = this.dialog.querySelector('#remove-file-btn');
        
        this.currentFile = null;
        this.appointmentId = null;
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Close buttons
        const closeBtns = this.dialog.querySelectorAll('[data-close-dialog]');
        closeBtns.forEach(btn => {
            btn.addEventListener('click', () => this.close());
        });
        
        // File input change
        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => {
                this.handleFileSelect(e);
            });
        }
        
        // Submit button
        if (this.submitBtn) {
            this.submitBtn.addEventListener('click', () => {
                this.handleUpload();
            });
        }
        
        // Remove file button
        if (this.removeFileBtn) {
            this.removeFileBtn.addEventListener('click', () => {
                this.removeFile();
            });
        }
    }
    
    open(appointmentId) {
        this.appointmentId = appointmentId;
        this.reset();
        this.dialog.showModal();
    }
    
    close() {
        this.dialog.close();
        this.reset();
    }
    
    reset() {
        this.currentFile = null;
        if (this.fileInput) this.fileInput.value = '';
        if (this.preview) this.preview.classList.add('hidden');
        if (this.placeholder) this.placeholder.classList.remove('hidden');
        if (this.submitBtn) this.submitBtn.disabled = true;
        if (this.progressContainer) this.progressContainer.classList.add('hidden');
        if (this.fileInfo) this.fileInfo.classList.add('hidden');
    }
    
    handleFileSelect(event) {
        const file = event.target.files?.[0];
        
        if (!file) return;
        
        // Validar tipo
        if (!this.validTypes.includes(file.type)) {
            if (window.toast) {
                window.toast.show('Formato inválido. Use JPG, PNG ou WebP', 'error');
            } else {
                alert('Formato inválido. Use JPG, PNG ou WebP');
            }
            this.fileInput.value = '';
            return;
        }
        
        // Validar tamanho
        if (file.size > this.maxFileSize) {
            if (window.toast) {
                window.toast.show('Arquivo muito grande. Máximo 5MB', 'error');
            } else {
                alert('Arquivo muito grande. Máximo 5MB');
            }
            this.fileInput.value = '';
            return;
        }
        
        // Validar extensão
        const ext = file.name.split('.').pop().toLowerCase();
        const validExts = ['jpg', 'jpeg', 'png', 'webp'];
        if (!validExts.includes(ext)) {
            if (window.toast) {
                window.toast.show('Extensão inválida', 'error');
            } else {
                alert('Extensão inválida');
            }
            this.fileInput.value = '';
            return;
        }
        
        this.currentFile = file;
        this.showPreview(file);
        this.showFileInfo(file);
        
        if (this.submitBtn) {
            this.submitBtn.disabled = false;
        }
    }
    
    showPreview(file) {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            if (this.preview) {
                this.preview.src = e.target.result;
                this.preview.classList.remove('hidden');
            }
            if (this.placeholder) {
                this.placeholder.classList.add('hidden');
            }
        };
        
        reader.readAsDataURL(file);
    }
    
    showFileInfo(file) {
        if (this.fileName) {
            this.fileName.textContent = file.name;
        }
        if (this.fileSize) {
            this.fileSize.textContent = this.formatFileSize(file.size);
        }
        if (this.fileInfo) {
            this.fileInfo.classList.remove('hidden');
        }
    }
    
    removeFile() {
        this.reset();
    }
    
    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
    
    async handleUpload() {
        if (!this.currentFile || !this.appointmentId) return;
        
        const formData = new FormData();
        formData.append('photo', this.currentFile);
        
        // Mostrar progress
        if (this.progressContainer) {
            this.progressContainer.classList.remove('hidden');
        }
        if (this.submitBtn) {
            this.submitBtn.disabled = true;
            const btnText = this.submitBtn.querySelector('#upload-btn-text');
            if (btnText) btnText.textContent = 'Enviando...';
        }
        
        try {
            const xhr = new XMLHttpRequest();
            
            // Progress handler
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    this.updateProgress(percentComplete);
                }
            });
            
            // Completion handler
            xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    const response = JSON.parse(xhr.responseText);
                    this.handleSuccess(response);
                } else {
                    this.handleError('Erro ao fazer upload');
                }
            });
            
            // Error handler
            xhr.addEventListener('error', () => {
                this.handleError('Erro de conexão');
            });
            
            // Send request
            xhr.open('POST', `/api/appointments/${this.appointmentId}/upload-photo/`);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('X-CSRFToken', this.getCsrfToken());
            xhr.send(formData);
            
        } catch (error) {
            console.error('Upload error:', error);
            this.handleError('Erro ao fazer upload');
        }
    }
    
    updateProgress(percent) {
        if (this.progressFill) {
            this.progressFill.style.width = percent + '%';
        }
        if (this.progressText) {
            this.progressText.textContent = Math.round(percent) + '%';
        }
    }
    
    handleSuccess(response) {
        if (window.toast) {
            window.toast.show('Foto enviada com sucesso!', 'success');
        } else {
            alert('Foto enviada com sucesso!');
        }
        
        this.close();
        
        // Callback se houver
        if (this.onSuccess && typeof this.onSuccess === 'function') {
            this.onSuccess(response);
        }
        
        // Recarregar página ou atualizar UI
        if (response.reload) {
            setTimeout(() => window.location.reload(), 1000);
        }
    }
    
    handleError(message) {
        if (window.toast) {
            window.toast.show(message, 'error');
        } else {
            alert(message);
        }
        
        // Reset progress
        if (this.progressContainer) {
            this.progressContainer.classList.add('hidden');
        }
        if (this.submitBtn) {
            this.submitBtn.disabled = false;
            const btnText = this.submitBtn.querySelector('#upload-btn-text');
            if (btnText) btnText.textContent = 'Enviar Foto';
        }
    }
    
    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Inicializar
let photoUploadDialog;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        photoUploadDialog = new PhotoUploadDialog();
        window.photoUploadDialog = photoUploadDialog;
    });
} else {
    photoUploadDialog = new PhotoUploadDialog();
    window.photoUploadDialog = photoUploadDialog;
}

// Função helper para abrir dialog
function openPhotoUpload(appointmentId) {
    if (window.photoUploadDialog) {
        window.photoUploadDialog.open(appointmentId);
    }
}

