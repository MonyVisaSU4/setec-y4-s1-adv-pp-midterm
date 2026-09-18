# Loan Management System (Loan-MGM)

A full-stack, enterprise-grade Financial Loan Management System built with **Python**, **Flask**, and **SQLAlchemy**. This platform provides role-based access control (RBAC) for **Administrators** and **Borrowers/Customers**, automated background loan status auditing via **APScheduler**, automated repayment amortization scheduling, and dynamic real-time reporting.

---

## Table of Contents

1. [System Architecture & Overview](#system-architecture--overview)
2. [Technology Stack & Where It Is Used](#technology-stack--where-it-is-used)
3. [Key Modules & Implementation Details](#key-modules--implementation-details)
4. [Database Schema & Data Models](#database-schema--data-models)
5. [Loan Calculation & Amortization Formula](#loan-calculation--amortization-formula)
6. [Automated Background Schedulers](#automated-background-schedulers)
7. [API & Route Directory](#api--route-directory)
8. [Project Directory Structure](#project-directory-structure)
9. [Installation & Setup Guide](#installation--setup-guide)
10. [Default Credentials & Usage](#default-credentials--usage)
11. [Bug Fixes & Code Audit Log](#bug-fixes--code-audit-log)

---

## System Architecture & Overview

The Loan Management System is organized as a modular Flask MVC application using Blueprints, declarative SQLAlchemy 2.0 ORM mappings, secure session management, and scheduled background workers.

```
graph TD
    Client[Web Browser / Client] -->|HTTP Requests| FlaskApp[Flask Application (app.py)]
    FlaskApp -->|Auth & Session| FlaskLogin[Flask-Login & Werkzeug Security]
    FlaskApp -->|Admin Blueprint| AdminRoutes[routes/admin.py]
    FlaskApp -->|Customer Blueprint| CustomerRoutes[routes/customer.py]
    AdminRoutes -->|Role Guard| Decorators[decorators.py (@admin_required)]
    FlaskApp -->|Scheduled Jobs (24h)| APScheduler[APScheduler Worker]
    APScheduler -->|Audit & Update Overdue| DB[(Database / SQLite / MySQL / PostgreSQL)]
    AdminRoutes -->|CRUD & Aggregations| Models[models/ - User, CustomerProfile, Loan, RepaymentSchedule]
    CustomerRoutes -->|Portfolio & Schedules| Models
    Models -->|SQLAlchemy 2.0 ORM| DB
```

---

## Technology Stack & Where It Is Used

Here is the breakdown of technologies, frameworks, and libraries implemented across the project:

| Technology / Library | Version | Purpose | Implementation Location |
| :--- | :--- | :--- | :--- |
| **Python** | `3.11+` | Core programming language | Entire Backend |
| **Flask** | `3.1.3` | Web Framework & Blueprint Routing | [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py), [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py), [`routes/customer.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/customer.py) |
| **Flask-SQLAlchemy** | `3.1.1` | ORM Integration with Flask | [`extension.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/extension.py), [`models/`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models) |
| **SQLAlchemy** | `2.0.51` | Database Mappings (`Mapped`, `mapped_column`, `relationship`, `select`, `func`, `and_`) | [`models/user.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/user.py), [`models/loan.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/loan.py), [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py) |
| **Flask-Login** | `0.6.3` | User Authentication, Session State & `@login_required` | [`login_manager.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/login_manager.py), [`models/user.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/user.py), [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py) |
| **Werkzeug Security** | `3.1.8` | Password hashing & verification (`generate_password_hash`, `check_password_hash`) | [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py), [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py), [`models/user.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/user.py) |
| **APScheduler** | `3.11.3` | Background periodic automation scheduler (`BackgroundScheduler`) | [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py) |
| **python-dateutil** | `2.9.0` | Calendar-accurate date arithmetic (`relativedelta`) | [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py), [`routes/customer.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/customer.py) |
| **Flask-Migrate** | `4.1.0` | Alembic-backed database schema migrations | [`extension.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/extension.py), [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py) |
| **python-dotenv** | `1.2.2` | Loading environment variables from `.env` file | [`config.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/config.py) |
| **Jinja2 & HTML5** | `3.1.6` | Dynamic server-side templating with template inheritance | [`templates/`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/templates) |
| **Bootstrap & CoreUI / CSS / JS** | Asset bundle | Admin layout, responsive tables, modal components & AJAX handlers | [`static/assets/`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/static/assets), [`templates/partials/`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/templates/partials) |
| **Database Drivers** | Multi-DB | `sqlite3`, `mysqlclient`, `PyMySQL`, `psycopg2-binary` support | Configured via `DATABASE_URL` in [`.env`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/.env) |

---

## Key Modules & Implementation Details

### 1. Role-Based Authentication & Access Control
- **Location**: [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py), [`decorators.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/decorators.py), [`login_manager.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/login_manager.py)
- **Implementation**:
  - `User.role` uses `StrEnum` (`Role.ADMIN = "admin"`, `Role.CUSTOMER = "customer"`).
  - Custom decorator [`@admin_required`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/decorators.py) inspects `current_user.role` and redirects non-admin users to the root login view.
  - Root route [`/`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py) intelligently routes authenticated users to their corresponding dashboard (`admin.dashboard` or `customer.dashboard`).

### 2. Admin Borrower Management (CRUD)
- **Location**: [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py)
- **Features**:
  - **Listing & Filter**: Joins `CustomerProfile` with `User` table; includes an async JSON endpoint (`/admin/borrower/filter`) for dynamic table updates.
  - **Add Borrower**: Atomic transaction creating both `User` (with hashed password) and `CustomerProfile` records with `db.session.flush()` and `db.session.commit()`.
  - **Safe Deletion**: Validates if the customer has existing loans before permitting deletion, preventing orphaned loan records and raising integrity warnings.

### 3. Automated Loan Issuance & Repayment Scheduling
- **Location**: [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py)
- **Features**:
  - Validates active loan limits per borrower.
  - Calculates flat interest and equal monthly installment payments.
  - Automatically generates `N` monthly `RepaymentSchedule` entries across the loan tenure using `dateutil.relativedelta(months=i + 1)`.

### 4. Installment Repayment & Collection Modal
- **Location**: [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py), [`templates/partials/modals/repay.html`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/templates/partials/modals/repay.html)
- **Features**:
  - Fetches repayment details asynchronously via GET.
  - Submits collected payment via POST, updating `amount_paid`, `paid_date`, and marking status as `PAID`.

### 5. Financial Audit & Reporting Dashboard
- **Location**: [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py)
- **Features**:
  - Real-time aggregations via SQL functions (`func.count`, `func.sum`).
  - Tracks Total Disbursed Principal, Expected Interest, Total Collected Repayments, Active Loans, and Overdue Installments.
  - Dynamic date-range and loan status filtering (`/admin/report/filter`).

### 6. Customer Portal & Self-Service
- **Location**: [`routes/customer.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/customer.py)
- **Features**:
  - Personalized Dashboard showing active loan balance, next installment due date, and payment history.
  - Loan portfolio list and detailed loan schedule timeline with status badges (Pending, Paid, Overdue).
  - Customer profile view.

---

## Database Schema & Data Models

The data layer uses SQLAlchemy 2.0 type annotations with cascade relationships.

```mermaid
erDiagram
    users ||--o| customer_profiles : "1 to 1 (user_id)"
    customer_profiles ||--o{ loans : "1 to Many (customer_id)"
    loans ||--o{ repayment_schedule : "1 to Many (loan_id)"

    users {
        int user_id PK
        string email UK
        string password_hash
        enum role "admin | customer"
        datetime created_at
        boolean is_active
    }

    customer_profiles {
        int customer_id PK
        int user_id FK
        string phone
        string address
        string national_id
        datetime created_at
    }

    loans {
        int loan_id PK
        int customer_id FK
        float amount
        float interest_rate
        int tenure_month
        date start_date
        enum status "active | closed"
        float total_payable
        datetime created_at
    }

    repayment_schedule {
        int id PK
        int loan_id FK
        date due_date
        float amount_due
        float amount_paid
        enum status "pending | paid | overdue"
        date paid_date
    }
```

### Model Files:
1. **[`models/user.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/user.py)**: Encapsulates user credentials, password hashing, and role definition with helper methods `set_password()`, `get_password()`, `check_password()`, and `to_dict()`.
2. **[`models/customer_profile.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/customer_profile.py)**: Stores personal identifiers (`phone`, `address`, `national_id`) with cascade relation.
3. **[`models/loan.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/loan.py)**: Encapsulates principal, interest rate, term duration, and status.
4. **[`models/repayment_schedule.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/repayment_schedule.py)**: Uses `@property status` and `_status` backing column to calculate overdue status if `due_date < today`.

---

## Loan Calculation & Amortization Formula

The system uses flat annual rate interest calculation implemented in [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py):

$$\text{Tenure (Years)} = \frac{\text{Tenure (Months)}}{12}$$

$$\text{Total Interest} = \text{Principal Amount} \times \left(\frac{\text{Annual Interest Rate}}{100}\right) \times \text{Tenure (Years)}$$

$$\text{Total Payable} = \text{Principal Amount} + \text{Total Interest}$$

$$\text{Monthly Installment Due} = \frac{\text{Total Payable}}{\text{Tenure (Months)}}$$

---

## Automated Background Schedulers

Configured using **APScheduler** in [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py):

1. **Overdue Status Auditor (`sync_status_overdue`)**:
   - Runs every 24 hours (`interval`, `hours=24`).
   - Scans all non-paid installments where `due_date < date.today()` and updates their status to `Status_Repay.OVERDUE`.
2. **Loan Closure Auditor (`sync_closed_status`)**:
   - Runs every 24 hours (`interval`, `hours=24`).
   - Checks active loans; if every installment schedule is marked as `PAID`, the loan status is automatically transitioned to `Status_Loan.CLOSED`.

---

## API & Route Directory

### Authentication Routes ([`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py))
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET`, `POST` | `/` | Login page & role-based dashboard redirection | Public |
| `GET` | `/logout` | Clears user session, calls `logout_user()`, and redirects to root | Authenticated |

### Admin Endpoints ([`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py))
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/admin/dashboard` | Main admin analytics & overdue installment tracker | Admin |
| `GET` | `/admin/borrower` | List all registered borrowers | Admin |
| `GET` | `/admin/borrower/filter` | AJAX search and filter borrower records | Admin |
| `GET`, `POST` | `/admin/borrower/add` | Register new borrower user and customer profile | Admin |
| `GET` | `/admin/borrower/view/<id>` | View customer profile and associated loan history | Admin |
| `GET`, `POST` | `/admin/borrower/update/<id>` | Update borrower details and password | Admin |
| `GET`, `POST` | `/admin/borrower/delete/<id>` | Safe delete borrower (if no active loans) | Admin |
| `GET` | `/admin/loan` | Overview of all loan agreements | Admin |
| `GET` | `/admin/loan/filter` | AJAX filter loans by status and start/end dates | Admin |
| `GET`, `POST` | `/admin/loan/add` | Issue a new loan and generate monthly schedules | Admin |
| `GET` | `/admin/loan/view/<id>` | View loan details and installment payment ledger | Admin |
| `GET`, `POST` | `/admin/loan/repay/<id>` | AJAX modal endpoint to process installment payment | Admin |
| `GET` | `/admin/report` | Financial audit report and metric aggregations | Admin |
| `GET` | `/admin/report/filter` | AJAX filter audit records by date range and status | Admin |

### Customer Endpoints ([`routes/customer.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/customer.py))
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/customer/dashboard` | Customer loan balance, next installment, and status | Customer |
| `GET` | `/customer/loan` | List of loans taken by the logged-in customer | Customer |
| `GET` | `/customer/loan/schedule/<id>`| Detailed repayment schedule and payment timeline | Customer |
| `GET` | `/customer/profile` | View profile details | Customer |

---

## Project Directory Structure

```
setec-y4-s1-adv-pp-midterm/
├── app.py                      # Application entry point, Blueprints & APScheduler setup
├── config.py                   # Configuration & .env environment parser
├── decorators.py               # Security & RBAC decorators (@admin_required)
├── extension.py                # SQLAlchemy & Flask-Migrate instance definitions
├── login_manager.py            # Flask-Login user_loader configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (DB URL, Secret Key)
├── models/                     # Declarative SQLAlchemy ORM Data Models
│   ├── __init__.py             # Exports User, CustomerProfile, Loan, RepaymentSchedule
│   ├── user.py                 # User authentication model & Role enum
│   ├── customer_profile.py     # Customer demographic profile model
│   ├── loan.py                 # Loan entity model & Status enum
│   └── repayment_schedule.py   # Repayment schedule model with dynamic overdue property
├── routes/                     # Blueprint Route Handlers
│   ├── admin.py                # Admin management, loan creation, audits, repay APIs
│   └── customer.py             # Customer portal, schedule timeline & profile APIs
├── templates/                  # Jinja2 HTML Templates
│   ├── layouts/
│   │   └── base.html           # Base layout template
│   ├── partials/               # Reusable template components
│   │   ├── navbar.html         # Top navigation header
│   │   ├── sidebar-left.html   # Role-aware sidebar navigation
│   │   ├── style-shop.html     # Stylesheet links
│   │   ├── jsshop.html         # Core JavaScript scripts
│   │   └── modals/
│   │       └── repay.html      # Modal dialog for processing repayments
│   ├── auth/
│   │   └── login.html          # Authentication login screen
│   ├── admin/
│   │   ├── dashboard.html      # Admin dashboard with summary cards & overdue table
│   │   ├── report.html         # Financial audit report
│   │   ├── borrower/           # Borrower CRUD templates (add, edit, list, view)
│   │   └── loan/               # Loan CRUD templates (add, list, view)
│   └── customer/
│       ├── dashboard.html      # Customer overview dashboard
│       ├── loan.html           # Customer loans list
│       ├── profile.html        # Customer profile page
│       └── schedule.html       # Installments timeline and agreement breakdown
└── static/
    └── assets/                 # CSS, SCSS, JavaScript, Images, and Vendor libraries
```

---

## Installation & Setup Guide

### 1. Prerequisites
- **Python 3.10+**
- **pip** and **virtualenv**

### 2. Required Packages (`requirements.txt`)
All necessary dependencies are pinned and provided in `requirements.txt`:
```txt
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.0
Flask-Login>=0.6.3
Flask-Migrate>=4.0.0
SQLAlchemy>=2.0.0
APScheduler>=3.10.0
python-dateutil>=2.8.2
python-dotenv>=1.0.0
Werkzeug>=3.0.0
```

### 3. Clone and Setup Environment
```bash
# Navigate to project directory
cd setec-y4-s1-adv-pp-midterm

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (CMD):
.venv\Scripts\activate.bat
# On Linux/macOS:
source .venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your_super_secret_session_key
DATABASE_URL=sqlite:///loan_management.db
FLASK_ENV=development
FLASK_APP=app.py
```
*(Supports PostgreSQL: `postgresql://user:pass@localhost:5432/loan_db` or MySQL: `mysql+pymysql://user:pass@localhost:3306/loan_db`)*

### 5. Run the Application
```bash
flask run
# or
python app.py
```
Open your browser at `http://127.0.0.1:5000/`.

---

## Default Credentials & Usage

### 1. Administrator Access
- Create an initial administrator record directly in the `users` table or database seed with `role = 'admin'`.
- Access all administrative panels: Borrowers, Loans, Repayments, and Reports.

### 2. Borrower / Customer Access
- Administrators can register new borrowers from `/admin/borrower/add`.
- Borrowers log in at `/` using their assigned email and password to track installments and loan statuses.

---

## Bug Fixes & Code Audit Log

Here is a summary of all identified bugs, their root causes, and how they were resolved:

| # | File | Bug Description & Root Cause | Resolution / Fix |
|---|------|------------------------------|------------------|
| 1 | [`app.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/app.py) | **Incomplete Logout**: `/logout` only called `session.clear()`, leaving Flask-Login's `current_user` and authentication cookie state unclean. | Imported and called `logout_user()` alongside `session.clear()`. |
| 2 | [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py) | **Tautology in Loan Creation**: `findLoan = Loan.query.filter(loans.customer_id == Loan.customer_id)` compared `Loan.customer_id == Loan.customer_id` (always `True` for all rows), blocking ANY customer from taking a loan if any loan existed in the system. | Changed filter to `Loan.customer_id == borrower_choose` and `Loan.status == Status_Loan.ACTIVE`. |
| 3 | [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py) | **Unscoped Loan Collection Query in `view_loan`**: `get_total_collect` executed an unaggregated query across all repayment schedules without filtering by the loan ID. | Computed `sum(r.amount_paid for r in repayment_schedule)` specifically for the selected loan. |
| 4 | [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py) | **Broken Deletion Response in `delete_borrower`**: Returned `render_template("admin/borrower/edit.html")` without context variables when a borrower had loans, breaking AJAX/SweetAlert handlers. | Returned clean JSON responses (`{"message": "..."}`) with appropriate status messages. |
| 5 | [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py) | **Incorrect Matching Count in `report`**: `matching_loan` counted `CustomerProfile.customer_id` (total borrowers) rather than matching loan records. | Updated `matching_loan` to count audited matching loan records (`len(audited_loan_records)`). |
| 6 | [`routes/admin.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/admin.py) | **Redundant SQL Joins**: `statement.join(CustomerProfile, User.user_id == CustomerProfile.user_id)` joined `CustomerProfile` with itself. | Corrected join clause to `.join(User, CustomerProfile.user_id == User.user_id)`. |
| 7 | [`routes/customer.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/customer.py) | **AttributeError Crashes on Missing Profiles/Loans**: Direct chaining `.first().customer_id` and `.first().amount_due` threw fatal errors when records were absent. | Added safe guards, `None` checks, and default empty states. |
| 8 | [`routes/customer.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/customer.py) | **Invalid Column Filter on Property**: `filter(RepaymentSchedule.status == Status.PENDING)` queried `@property status` instead of the mapped column `_status`, and queried all customers' loans globally. | Filtered by customer loan IDs (`loan_id.in_(...)`) and mapped column `_status != Status_Repay.PAID`. |
| 9 | [`routes/customer.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/routes/customer.py) | **IndexError & Inaccurate Tenure in `schedule`**: `relativedelta(repays[0].due_date, loan.start_date).months` crashed if `repays` was empty and returned `1` instead of total tenure. | Used `loan_record.tenure_month` directly. |
| 10 | [`templates/admin/borrower/edit.html`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/templates/admin/borrower/edit.html) | **Inverted Flash Message Tuple**: `{% for message, category in messages %}` inverted `(category, message)`. | Corrected to `{% for category, message in messages %}`. |
| 11 | [`templates/admin/borrower/view.html`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/templates/admin/borrower/view.html) | **Missing Fallbacks & Broken Loan Actions**: Table rows lacked null checks on dates, and action button routes were broken or misaligned. | Added fallback formatting, safe filters, and validated link attributes. |
| 12 | [`templates/customer/dashboard.html`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/templates/customer/dashboard.html) | **Broken Links & Formatter**: Hardcoded `id=id` in loan portfolio loop and uncaught `.strftime()` on `None`. | Linked `id=l.loan_id` and conditionally formatted `due_date`. |
| 13 | [`models/user.py`](file:///d:/Year4%20Semmester1/ADV%20PP/Midterm/setec-y4-s1-adv-pp-midterm/models/user.py) | **Encapsulation & Security**: Password hashing logic and model attributes exposed without getters/setters and serialization safety. | Added `set_password()`, `get_password()`, `check_password()`, and secure `to_dict()` excluding sensitive fields. |
