// Layout builder for Loan Management System

(function () {
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

    // 2. Perform DOM modifications once DOM is ready
    document.addEventListener("DOMContentLoaded", () => {
        const session = window.auth ? window.auth.getSession() : null;
        if (!session) return; // Not logged in, auth.js handles redirect

        const currentFile = window.location.pathname.split("/").slice(-1)[0] || "index.html";

        // ── SIDEBAR ──────────────────────────────────────────────────────────────
        const sidebarEl = document.getElementById("sidebar");
        if (sidebarEl) {
            let displayName = "Admin";
            let displayRole = "Administrator";
            let profilePic = "assets/images/faces/face1.jpg";

            if (session.role === "customer") {
                displayRole = "Borrower";
                profilePic = "assets/images/faces/face2.jpg";
                if (window.db) {
                    const profile = window.db.getCustomerById(session.customerProfileId);
                    if (profile) {
                        displayName = profile.name;
                        const num = parseInt(profile.id.replace(/\D/g, "")) || 2;
                        profilePic = `assets/images/faces/face${(num % 10) + 2}.jpg`;
                    }
                }
            }

            // Menu items per role
            let menuItems = [];
            if (session.role === "admin") {
                menuItems = [
                    {name: "Dashboard", href: "admin_dashboard.html", icon: "mdi mdi-speedometer"},
                    {name: "Borrowers", href: "admin_customers.html", icon: "mdi mdi-account-multiple"},
                    {name: "Loans", href: "admin_loans.html", icon: "mdi mdi-cash-multiple"},
                    {name: "Reports", href: "admin_reports.html", icon: "mdi mdi-file-document"}
                ];
            } else {
                menuItems = [
                    {name: "Dashboard", href: "customer_dashboard.html", icon: "mdi mdi-speedometer"},
                    {name: "My Profile", href: "customer_profile.html", icon: "mdi mdi-account"},
                    {name: "My Loans", href: "customer_loans.html", icon: "mdi mdi-cash-multiple"}
                ];
            }

            // Build nav <li> items
            let navItemsHtml = "";

            // Profile item
            navItemsHtml += `
        <li class="nav-item nav-profile">
          <a href="#" class="nav-link">
            <div class="nav-profile-image">
              <img src="${profilePic}" alt="profile" style="width:44px;height:44px;object-fit:cover;border-radius:50%">
              <span class="login-status online"></span>
            </div>
            <div class="nav-profile-text d-flex flex-column">
              <span class="font-weight-bold mb-2">${displayName}</span>
              <span class="text-secondary text-small">${displayRole}</span>
            </div>
            <i class="mdi mdi-bookmark-check text-success nav-profile-badge"></i>
          </a>
        </li>
      `;

            // Menu links — icon LEFT, title RIGHT (standard Bootstrap Admin order)
            menuItems.forEach(item => {
                const isActive = item.href === currentFile ? "active" : "";
                navItemsHtml += `
          <li class="nav-item ${isActive}">
            <a class="nav-link" href="${item.href}">
              <i class="${item.icon} menu-icon"></i>
              <span class="menu-title">${item.name}</span>
            </a>
          </li>
        `;
            });

            // Logout
            navItemsHtml += `
        <li class="nav-item sidebar-actions">
          <span class="nav-link">
            <button class="btn btn-block btn-gradient-danger btn-sm" onclick="auth.logout()">
              <i class="mdi mdi-logout mr-2"></i>Logout
            </button>
          </span>
        </li>
      `;

            // Full sidebar HTML — brand wrapper + nav
            sidebarEl.innerHTML = `
        <div class="sidebar-brand-wrapper d-none d-lg-flex align-items-center justify-content-center fixed-top">
          <a class="sidebar-brand brand-logo" href="${session.role === 'admin' ? 'admin_dashboard.html' : 'customer_dashboard.html'}" style="text-decoration:none;">
            <span class="text-primary font-weight-bold" style="font-size:1.6rem;">
              <i class="mdi mdi-bank mr-1"></i>LMS
            </span>
          </a>
          <a class="sidebar-brand brand-logo-mini" href="${session.role === 'admin' ? 'admin_dashboard.html' : 'customer_dashboard.html'}" style="text-decoration:none;">
            <span class="text-primary font-weight-bold" style="font-size:1.3rem;">L</span>
          </a>
        </div>
        <ul class="nav">
          ${navItemsHtml}
        </ul>
      `;
        }

        // ── NAVBAR ───────────────────────────────────────────────────────────────
        const navbarEl = document.getElementById("navbar");
        if (navbarEl) {
            let displayName = "Admin User";
            let profilePic = "assets/images/faces/face1.jpg";

            if (session.role === "customer") {
                profilePic = "assets/images/faces/face2.jpg";
                if (window.db) {
                    const profile = window.db.getCustomerById(session.customerProfileId);
                    if (profile) {
                        displayName = profile.name;
                        const num = parseInt(profile.id.replace(/\D/g, "")) || 2;
                        profilePic = `assets/images/faces/face${(num % 10) + 2}.jpg`;
                    }
                }
            }

            const accountHref = session.role === "admin" ? "admin_dashboard.html" : "customer_profile.html";

            navbarEl.innerHTML = `
        <div class="navbar-brand-wrapper d-flex d-lg-none align-items-center justify-content-center">
          <a class="navbar-brand brand-logo-mini" href="${accountHref}" style="text-decoration:none;font-size:1.3rem;font-weight:700;" class="text-primary">
            <i class="mdi mdi-bank mr-1 text-primary"></i>
            <span class="text-primary">LMS</span>
          </a>
        </div>
        <div class="navbar-menu-wrapper d-flex align-items-stretch">
          <button class="navbar-toggler navbar-toggler align-self-center" type="button" data-toggle="minimize">
            <span class="mdi mdi-menu"></span>
          </button>
          <ul class="navbar-nav navbar-nav-right">
            <li class="nav-item nav-profile dropdown">
              <a class="nav-link dropdown-toggle" id="profileDropdown" href="#" data-toggle="dropdown" aria-expanded="false">
                <div class="nav-profile-img">
                  <img src="${profilePic}" alt="image" style="width:32px;height:32px;object-fit:cover;border-radius:50%">
                  <span class="availability-status online"></span>
                </div>
                <div class="nav-profile-text">
                  <p class="mb-1 text-black font-weight-semibold">${displayName}</p>
                  <p class="text-small text-muted mb-0">${session.role === "admin" ? "Administrator" : "Borrower"}</p>
                </div>
              </a>
              <div class="dropdown-menu navbar-dropdown" aria-labelledby="profileDropdown">
                <a class="dropdown-item" href="${accountHref}">
                  <i class="mdi mdi-account-circle mr-2 text-primary"></i> My Account
                </a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="javascript:void(0)" onclick="auth.logout()">
                  <i class="mdi mdi-logout mr-2 text-danger"></i> Sign Out
                </a>
              </div>
            </li>
            <li class="nav-item d-none d-lg-block full-screen-link">
              <a class="nav-link" id="fullscreen-button" title="Toggle Fullscreen" style="cursor:pointer;">
                <i class="mdi mdi-fullscreen" id="fullscreen-icon"></i>
              </a>
            </li>
          </ul>
          <button class="navbar-toggler navbar-toggler-right d-lg-none align-self-center" type="button" data-toggle="offcanvas">
            <span class="mdi mdi-menu"></span>
          </button>
        </div>
      `;
        }

        // ── FOOTER ───────────────────────────────────────────────────────────────
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

        // 3. Load theme JS scripts in order
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
            });
    });
})();
