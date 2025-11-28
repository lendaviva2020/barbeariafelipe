/**
 * Gallery Page - Sistema completo com Lightbox
 * Extraído 100% do React Gallery.tsx (447 linhas)
 */

// Gallery Images Data - Usando imagens da pasta gallery
const galleryImages = [
    { id: 1, src: '/static/images/gallery/corte-classico.jpg', alt: 'Corte clássico executivo premium', category: 'cortes', featured: true },
    { id: 2, src: '/static/images/gallery/corte-barba.jpg', alt: 'Transformação completa corte e barba', category: 'antes-depois', featured: true },
    { id: 3, src: '/static/images/gallery/barba-completa.jpg', alt: 'Barba cheia modelada profissionalmente', category: 'barbas', featured: true },
    { id: 4, src: '/static/images/gallery/bigode.jpg', alt: 'Bigode estilizado vintage', category: 'barbas', featured: true },
    { id: 5, src: '/static/images/gallery/barbershop-hero.jpg', alt: 'Interior clássico da barbearia', category: 'ambiente', featured: true }
];

// State
let currentCategory = 'all';
let filteredImages = [...galleryImages];
let currentImageIndex = 0;
let isLightboxOpen = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        hideLoading();
        renderGallery();
        setupFilterButtons();
        setupKeyboardControls();
    }, 800);
});

// Setup filter buttons
function setupFilterButtons() {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const category = btn.dataset.category;
            setCategory(category);
        });
    });
}

// Set category and filter
function setCategory(category) {
    currentCategory = category;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.dataset.category === category) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Filter images
    if (category === 'all') {
        filteredImages = [...galleryImages];
    } else {
        filteredImages = galleryImages.filter(img => img.category === category);
    }
    
    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Re-render
    renderGallery();
}

// Render gallery
function renderGallery() {
    const grid = document.getElementById('galleryGrid');
    const container = document.getElementById('galleryContainer');
    const emptyState = document.getElementById('emptyState');
    const counter = document.getElementById('imageCounter');
    
    // Update counter
    const countText = filteredImages.length === 1 ? 'imagem' : 'imagens';
    const categoryText = currentCategory !== 'all' ? ` em ${getCategoryLabel(currentCategory)}` : '';
    counter.textContent = `${filteredImages.length} ${countText}${categoryText}`;
    
    // Check if empty
    if (filteredImages.length === 0) {
        container.style.display = 'none';
        emptyState.style.display = 'block';
        document.getElementById('emptyMessage').textContent = 
            `Nenhuma imagem encontrada na categoria "${getCategoryLabel(currentCategory)}"`;
        return;
    }
    
    emptyState.style.display = 'none';
    container.style.display = 'block';
    
    // Render images
    grid.innerHTML = filteredImages.map((img, index) => `
        <div class="gallery-item" data-index="${index}" onclick="openLightbox(${index})" style="animation-delay: ${index * 0.05}s;">
            <img src="${img.src}" alt="${img.alt}" loading="lazy" 
                 onerror="this.src='https://via.placeholder.com/400x400/2C1810/C9A961?text=${encodeURIComponent(img.alt.slice(0, 20))}'">
            
            ${img.featured ? `
                <div class="featured-badge">
                    <span>✨</span> Destaque
                </div>
            ` : ''}
            
            <div class="gallery-overlay">
                <div class="gallery-zoom-icon" style="position: absolute; top: 1rem; left: 1rem; color: var(--color-gold); font-size: 2rem;">
                    🔍
                </div>
                <p class="gallery-overlay-title">${img.alt}</p>
                <span class="gallery-overlay-category">${getCategoryLabel(img.category)}</span>
            </div>
        </div>
    `).join('');
}

// Get category label
function getCategoryLabel(category) {
    const labels = {
        'all': 'Todos',
        'cortes': 'Cortes',
        'barbas': 'Barbas',
        'antes-depois': 'Antes/Depois',
        'ambiente': 'Ambiente'
    };
    return labels[category] || category;
}

// Open lightbox
function openLightbox(index) {
    currentImageIndex = index;
    isLightboxOpen = true;
    
    const lightbox = document.getElementById('lightbox');
    lightbox.style.display = 'flex';
    
    updateLightboxImage();
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

// Close lightbox
function closeLightbox() {
    isLightboxOpen = false;
    document.getElementById('lightbox').style.display = 'none';
    document.body.style.overflow = '';
}

// Update lightbox image
function updateLightboxImage() {
    const img = filteredImages[currentImageIndex];
    if (!img) return;
    
    const lightboxImg = document.getElementById('lightboxImage');
    const title = document.getElementById('lightboxTitle');
    const category = document.getElementById('lightboxCategory');
    const counter = document.getElementById('lightboxCounter');
    
    // Show loading
    lightboxImg.classList.add('loading');
    
    // Update content
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    title.textContent = img.alt;
    category.textContent = getCategoryLabel(img.category);
    counter.textContent = `${currentImageIndex + 1} de ${filteredImages.length}`;
    
    // Handle image load
    lightboxImg.onload = () => {
        lightboxImg.classList.remove('loading');
    };
}

// Next image
function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % filteredImages.length;
    updateLightboxImage();
}

// Previous image
function previousImage() {
    currentImageIndex = (currentImageIndex - 1 + filteredImages.length) % filteredImages.length;
    updateLightboxImage();
}

// Share image
async function shareImage() {
    const img = filteredImages[currentImageIndex];
    
    try {
        if (navigator.share) {
            await navigator.share({
                title: 'Barbearia Francisco - Galeria',
                text: img.alt,
                url: window.location.href
            });
        } else {
            await navigator.clipboard.writeText(window.location.href);
            showToast('Link copiado!', 'Link da galeria copiado para a área de transferência', 'success');
        }
    } catch (error) {
        // User cancelled share
        console.log('Share cancelled');
    }
}

// Download image
async function downloadImage() {
    const img = filteredImages[currentImageIndex];
    
    try {
        const response = await fetch(img.src);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `barbearia-francisco-${img.id}.jpg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
        
        showToast('Download iniciado', 'Imagem baixada com sucesso', 'success');
    } catch (error) {
        console.error('Download error:', error);
        showToast('Erro no download', 'Não foi possível baixar a imagem', 'error');
    }
}

// Keyboard controls
function setupKeyboardControls() {
    document.addEventListener('keydown', (e) => {
        if (!isLightboxOpen) return;
        
        switch (e.key) {
            case 'Escape':
                closeLightbox();
                break;
            case 'ArrowLeft':
                previousImage();
                break;
            case 'ArrowRight':
                nextImage();
                break;
        }
    });
}

// Show/Hide loading
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('galleryContainer').style.display = 'block';
}

// Toast notification
function showToast(title, message, type = 'success') {
    if (window.showToast) {
        window.showToast(title, message, type);
    } else {
        alert(`${title}: ${message}`);
    }
}

// Export functions for inline handlers
window.openLightbox = openLightbox;
window.closeLightbox = closeLightbox;
window.nextImage = nextImage;
window.previousImage = previousImage;
window.shareImage = shareImage;
window.downloadImage = downloadImage;

