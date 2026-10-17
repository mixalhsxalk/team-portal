document.addEventListener('DOMContentLoaded', function() {

    // ── 1. Active nav highlight ──────────────────────────
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');

    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (!href) return;

        if (href === '/' && currentPath === '/') {
            item.classList.add('active');
        } else if (href !== '/' && currentPath.startsWith(href)) {
            item.classList.add('active');
        }
    });

    // ── 2. Auto-dismiss non-error alerts ────────────────
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');

    alerts.forEach(alertEl => {
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined') {
                new bootstrap.Alert(alertEl).close();
            } else {
                alertEl.classList.remove('show');
                setTimeout(() => alertEl.remove(), 150);
            }
        }, 4500);
    });

});