// 1. Inject Stylesheets immediately into <head>
const stylesheets = [
    "assets/vendors/mdi/css/materialdesignicons.min.css",
    "assets/vendors/css/vendor.bundle.base.css",
    "assets/vendors/font-awesome/css/font-awesome.min.css",
    "assets/css/style.css"
];

stylesheets.forEach(href => {
    if (!document.querySelector(`link[href="${href}"]`)) {
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = href;
        document.head.appendChild(link);
    }
});

// Inject style fixes
const styleFix = document.createElement("style");
styleFix.textContent = `
    .sidebar .nav .nav-item .nav-link .menu-title {
      font-size: 0.9375rem;
    }
    .badge-pending { background-color: #ffc107; color: #111; }
    .badge-active  { background-color: #007bff; color: #fff; }
    .badge-closed  { background-color: #28a745; color: #fff; }
    .badge-overdue { background-color: #dc3545; color: #fff; }
    .badge-paid    { background-color: #28a745; color: #fff; }
    .table-overdue-row { background-color: rgba(220, 53, 69, 0.15) !important; }
  `;
document.head.appendChild(styleFix);

const footerEl = document.getElementById("footer");
if (footerEl) {
    const year = new Date().getFullYear();
    footerEl.innerHTML = `
        <div class="container-fluid clearfix">
          <span class="text-muted d-block text-center text-sm-left d-sm-inline-block">Copyright &copy; LMS ${year}</span>
          <span class="float-none float-sm-right d-block mt-1 mt-sm-0 text-center">Premium Loan Management System</span>
        </div>
      `;
}

function loadScript(src) {
    return new Promise((resolve, reject) => {
        // Avoid loading duplicates
        if (document.querySelector(`script[src="${src}"]`)) {
            resolve();
            return;
        }
        const s = document.createElement("script");
        s.src = src;
        s.onload = resolve;
        s.onerror = reject;
        document.body.appendChild(s);
    });
}

loadScript("assets/vendors/js/vendor.bundle.base.js")
    .then(() => loadScript("assets/js/off-canvas.js"))
    .then(() => loadScript("assets/js/misc.js"))
    .then(() => loadScript("assets/js/settings.js"))
    .then(() => loadScript("assets/js/todolist.js"))
    .then(() => {
        window.dispatchEvent(new Event("lms-scripts-loaded"));
    })
    .catch(err => {
        console.error("Error loading theme scripts:", err);
        // Fire event anyway so page content still loads
        window.dispatchEvent(new Event("lms-scripts-loaded"));
    })