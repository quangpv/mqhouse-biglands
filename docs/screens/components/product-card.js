function formatCommission(value) {
    if (!value || value <= 0) return '';
    if (value >= 1000000000) return (value / 1000000000).toFixed(1).replace(/\.0$/, '') + ' tỷ';
    if (value >= 1000000) return (value / 1000000).toFixed(0) + 'tr';
    if (value >= 1000) return (value / 1000).toFixed(0) + 'k';
    return String(value);
}

function getStatusBadge(status) {
    var colorMap = {
        draft: 'bg-slate-400/90',
        post_pending: 'bg-blue-500/90',
        edit_pending: 'bg-blue-500/90',
        deposit_pending: 'bg-amber-500/90',
        soldout_pending: 'bg-orange-500/90',
        complete_pending: 'bg-indigo-500/90',
        cancel_pending: 'bg-red-400/90',
        available: 'bg-success/90',
        deposited: 'bg-warning/90',
        soldout: 'bg-red-600/90',
        expired: 'bg-slate-500/95',
        completed: 'bg-slate-500/95',
    };
    var dotStatuses = { available: true, deposited: true, soldout: true };
    var bgClass = colorMap[status] || 'bg-slate-500/95';
    var label = (typeof STATUS_LABELS !== 'undefined' && STATUS_LABELS[status]) || status;
    var dot = dotStatuses[status] ? '<span class="h-1.5 w-1.5 bg-white rounded-full"></span>' : '';
    return '<span class="px-2.5 py-1 text-[11px] font-semibold ' + bgClass + ' text-white rounded-[8px] uppercase tracking-wider flex items-center gap-1 shadow-sm">' + dot + label + '</span>';
}

function formatDateVietnamese(dateString) {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    return date.toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

class ProductCard extends HTMLElement {
    constructor() {
        super();
        this._product = null;
        this._listenersAttached = false;
    }

    set product(val) {
        this._product = val;
        if (this.isConnected) this.render();
    }

    get product() {
        return this._product;
    }

    connectedCallback() {
        this._attachGlobalListeners();
        if (this._product) this.render();
    }

    disconnectedCallback() {
        this._removeGlobalListeners();
    }

    _attachGlobalListeners() {
        if (this._listenersAttached) return;
        this._listenersAttached = true;

        this._onWindowClick = (e) => {
            const menu = this.querySelector('[data-card-menu]');
            if (menu && !menu.classList.contains('hidden') && !this.contains(e.target)) {
                menu.classList.add('hidden');
            }
        };

        this._onMenuOpened = (e) => {
            if (e.target !== this) {
                const menu = this.querySelector('[data-card-menu]');
                if (menu) menu.classList.add('hidden');
            }
        };

        window.addEventListener('click', this._onWindowClick);
        window.addEventListener('product-card:menu-opened', this._onMenuOpened);
    }

    _removeGlobalListeners() {
        if (this._onWindowClick) window.removeEventListener('click', this._onWindowClick);
        if (this._onMenuOpened) window.removeEventListener('product-card:menu-opened', this._onMenuOpened);
        this._listenersAttached = false;
    }

    render() {
        const prod = this._product;
        if (!prod) return;

        const statusBadge = getStatusBadge(prod.status);
        const pinButtonClass = prod.isPinned ? 'text-warning fill-warning' : 'text-textSecondary hover:text-warning';

        this.innerHTML = `
                    <div class="bg-surface border border-border rounded-[16px] overflow-hidden shadow-soft flex flex-col h-full group hover:shadow-md transition-all duration-150 relative cursor-pointer">
                    <div class="relative h-[200px] overflow-hidden">
                        <img src="${prod.thumbnail}" alt="${prod.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        <div class="absolute top-3 left-3 flex flex-wrap gap-1.5 max-w-[80%]">
                            <span class="px-2.5 py-1 text-[11px] font-semibold ${prod.transactionType === 'Bán' ? 'bg-primary' : 'bg-success'} text-white rounded-[8px] uppercase tracking-wider">${prod.transactionType}</span>
                            ${prod.isHot ? '<span class="px-2.5 py-1 text-[11px] font-semibold bg-red-600 text-white rounded-[8px] uppercase tracking-wider">Hot 🔥</span>' : ''}
                        </div>
                        <div class="absolute top-3 right-3 flex gap-1.5">
                            <button data-pin-btn class="bg-white/90 hover:bg-white p-1.5 rounded-full shadow-soft transition-all" title="Ghim sản phẩm">
                                <i data-lucide="pin" class="h-3.5 w-3.5 ${pinButtonClass}"></i>
                            </button>
                            <button data-menu-btn class="bg-white/90 hover:bg-white p-1.5 rounded-full shadow-soft transition-all" title="Thao tác">
                                <i data-lucide="more-vertical" class="h-3.5 w-3.5 text-textSecondary"></i>
                            </button>
                        </div>
                        <div class="absolute bottom-3 right-3 flex items-center gap-1.5">
                            ${statusBadge}
                        </div>
                        <div class="absolute bottom-3 left-3 flex items-center gap-1.5">
                            ${prod.commission ? `
                            <span class="flex items-center gap-1 px-2 py-1 text-[11px] font-semibold bg-blue-600/90 text-white rounded-[8px] shadow-sm">
                                <i data-lucide="circle-dollar-sign" class="h-3.5 w-3.5"></i>
                                ${formatCommission(prod.commission)}
                            </span>` : ''}
                        </div>
                    </div>
                    <div data-card-menu class="hidden absolute top-12 right-3 w-44 bg-white border border-border rounded-[12px] shadow-soft z-50 py-1">
                ${prod.isHot ? `
                <button data-action="unhot" class="w-full flex items-center gap-2 px-3 py-2 text-[13px] text-textPrimary hover:bg-slate-50 transition-all text-left">
                    <i data-lucide="flame" class="h-3.5 w-3.5 text-orange-500"></i><span>Bỏ Hàng Hot</span>
                </button>` : `
                <button data-action="hot" class="w-full flex items-center gap-2 px-3 py-2 text-[13px] text-textPrimary hover:bg-slate-50 transition-all text-left">
                    <i data-lucide="flame" class="h-3.5 w-3.5 text-orange-500"></i><span>Đẩy lên Hot</span>
                </button>`}
                        <button data-action="edit" class="w-full flex items-center gap-2 px-3 py-2 text-[13px] text-textPrimary hover:bg-slate-50 transition-all text-left">
                            <i data-lucide="pencil" class="h-3.5 w-3.5"></i><span>Chỉnh sửa</span>
                        </button>
                        <button data-action="approve" class="w-full flex items-center gap-2 px-3 py-2 text-[13px] text-textPrimary hover:bg-slate-50 transition-all text-left">
                            <i data-lucide="check-circle" class="h-3.5 w-3.5 text-success"></i><span>Duyệt</span>
                        </button>
                        <button data-action="reject" class="w-full flex items-center gap-2 px-3 py-2 text-[13px] text-textPrimary hover:bg-slate-50 transition-all text-left">
                            <i data-lucide="x-circle" class="h-3.5 w-3.5 text-error"></i><span>Từ chối</span>
                        </button>
                        <div class="h-px bg-border my-1 mx-2"></div>
                        <button data-action="delete" class="w-full flex items-center gap-2 px-3 py-2 text-[13px] text-error hover:bg-red-50 transition-all text-left">
                            <i data-lucide="trash-2" class="h-3.5 w-3.5"></i><span>Xóa</span>
                        </button>
                    </div>

                    <div class="p-4 flex-1 flex flex-col justify-between space-y-2">
                        <div class="space-y-2">
                            <div class="flex items-center justify-between">
                                <span class="text-[12px] font-medium text-textSecondary uppercase tracking-wide">${prod.propertyType}</span>
                                <span class="text-[11px] font-semibold text-slate-400">#${prod.id}</span>
                            </div>
                            <h3 class="text-[16px] font-semibold text-textPrimary leading-snug line-clamp-2 hover:text-primary transition-all duration-150">
                                <a href="#">${prod.title}</a>
                            </h3>
                            <p class="text-[12px] text-textSecondary flex items-center gap-1">
                                <i data-lucide="map-pin" class="h-4 w-4 shrink-0 text-slate-400 mt-0.5"></i>
                                <span class="line-clamp-2">${prod.address}</span>
                            </p>
                        </div>

                        <div class="grid grid-cols-3 gap-2 bg-slate-50 p-2.5 rounded-[12px] text-center text-textPrimary">
                            <div>
                                <span class="text-[10px] text-textSecondary block">P. Ngủ</span>
                                <span class="text-[13px] font-semibold">${prod.roomCount || '-'} PN</span>
                            </div>
                            <div>
                                <span class="text-[10px] text-textSecondary block">Nhà VS</span>
                                <span class="text-[13px] font-semibold">${prod.wcCount || '-'} WC</span>
                            </div>
                            <div>
                                <span class="text-[10px] text-textSecondary block font-medium text-textSecondary">Số tầng</span>
                                <span class="text-[13px] font-semibold">${prod.floorCount || '-'} T</span>
                            </div>
                        </div>

                        ${prod.highlightBadges && prod.highlightBadges.length > 0 ? `
                        <div class="flex flex-wrap gap-1">
                            ${prod.highlightBadges.map(b => `<span class="px-2 py-0.5 bg-slate-100 text-textSecondary text-[11px] rounded-[6px] font-medium">${b}</span>`).join('')}
                        </div>
                        ` : ''}

                        <div class="grid grid-cols-2 gap-3 pt-3 border-t border-border">
                            <div>
                                <span class="text-[10px] text-textSecondary block font-medium">Giá</span>
                                <span class="text-[18px] font-bold text-error">${prod.transferPrice}</span>
                                <span class="text-[11px] text-textSecondary block mt-0.5">${prod.unitPrice}tr/m²</span>
                            </div>
                            <div class="border-l border-border pl-3">
                                <span class="text-[10px] text-textSecondary block font-medium">Diện tích</span>
                                <span class="text-[18px] font-bold text-textPrimary">${prod.landArea} m²</span>
                                <span class="text-[11px] text-textSecondary block mt-0.5">${prod.width}m × ${prod.length}m</span>
                            </div>
                        </div>

                        <div class="flex items-center justify-between pt-3 border-t border-slate-100">
                            <div class="flex items-center gap-2">
                                <img src="${prod.postedUser.avatar}" alt="${prod.postedUser.name}" class="h-6 w-6 rounded-full object-cover ring-1 ring-border">
                                <span class="text-[12px] font-semibold text-textPrimary">${prod.postedUser.name}</span>
                            </div>
                            <span class="text-[11px] font-medium text-textPrimary">${formatDateVietnamese(prod.postedDate)}</span>
                        </div>
                    </div>
                </div>
        `;

        this._bindEvents();
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    _bindEvents() {
        const prod = this._product;
        if (!prod) return;

        const card = this.querySelector('.bg-surface');
        if (card) {
            card.addEventListener('click', (e) => {
                if (e.target.closest('button') || e.target.closest('a')) return;
                this.dispatchEvent(new CustomEvent('product-card:select', {
                    bubbles: true,
                    detail: { id: prod.id }
                }));
            });
        }

        const pinBtn = this.querySelector('[data-pin-btn]');
        if (pinBtn) {
            pinBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.dispatchEvent(new CustomEvent('product-card:pin', {
                    bubbles: true,
                    detail: { id: prod.id }
                }));
            });
        }

        const menuBtn = this.querySelector('[data-menu-btn]');
        if (menuBtn) {
            menuBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this._toggleMenu();
            });
        }

        this.querySelectorAll('[data-action]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const menu = this.querySelector('[data-card-menu]');
                if (menu) menu.classList.add('hidden');
                this.dispatchEvent(new CustomEvent('product-card:action', {
                    bubbles: true,
                    detail: { id: prod.id, action: btn.dataset.action }
                }));
            });
        });

        const menu = this.querySelector('[data-card-menu]');
        if (menu) {
            menu.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
    }

    _toggleMenu() {
        const menu = this.querySelector('[data-card-menu]');
        if (!menu) return;

        document.querySelectorAll('product-card [data-card-menu]').forEach(m => {
            if (m !== menu) m.classList.add('hidden');
        });

        menu.classList.toggle('hidden');

        if (!menu.classList.contains('hidden')) {
            this.dispatchEvent(new CustomEvent('product-card:menu-opened', {
                bubbles: true
            }));
        }
    }
}

customElements.define('product-card', ProductCard);
