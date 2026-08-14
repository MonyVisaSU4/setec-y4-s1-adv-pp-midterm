# Loan Management System

A comprehensive web application for managing loans, borrowers, and repayment schedules. Built with Python and Flask, this system provides dual-role access for administrators and customers to manage loans efficiently.

## Overview

The Loan Management System is a full-featured financial management application that enables:

- **Admin Dashboard**: Comprehensive oversight of all loans, borrowers, and financial metrics
- **Customer Portal**: Customers can view their loan portfolio and repayment schedules
- **Loan Management**: Create, update, and track loans with automated repayment scheduling
- **Repayment Tracking**: Monitor payment status and overdue installments
- **User Authentication**: Secure login system with role-based access control

## Key Features

### Admin Features
- Dashboard with key financial metrics (total borrowers, active loans, disbursed amounts, collected amounts)
- Manage borrowers and their profiles
- Create and manage loans
- Track repayment schedules and overdue payments
- Generate reports and audit logs
- View borrower information and loan history

### Customer Features
- Personal dashboard with loan portfolio overview
- View active loans and their details
- Access repayment schedules
- Track payment history and remaining balance
- View upcoming due installments
- Update profile information

### Core Functionality
- **User Management**: Multi-role authentication (Admin & Customer)
- **Loan Processing**: Complete loan lifecycle management
- **Repayment Scheduling**: Automatic calculation of EMI and repayment schedules
- **Financial Tracking**: Monitor disbursements, collections, and outstanding amounts

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Authentication**: Flask-Login for session management
- **Frontend**: Jinja2 templating with Bootstrap
- **Additional Libraries**: SQLAlchemy, python-dotenv, Werkzeug

## Project Structure

```
loan-mgm/
├── app.py                          # Main Flask application entry point
├── config.py                       # Configuration management
├── decorators.py                   # Custom decorators for authorization
├── extension.py                    # Flask extensions initialization
├── login_manager.py                # Login manager configuration
├── requirements.txt                # Project dependencies
├── models/                         # Database models
│   ├── user.py                    # User model with roles (Admin/Customer)
│   ├── customer_profile.py        # Customer profile information
│   ├── loan.py                    # Loan details and status tracking
│   └── repayment_schedule.py      # Repayment schedule and payment status
├── routes/                        # Application routes/blueprints
│   ├── admin.py                   # Admin-specific routes and logic
│   └── customer.py                # Customer-specific routes and logic
├── templates/                     # HTML templates
│   ├── auth/                      # Login page templates
│   ├── admin/                     # Admin dashboard and management pages
│   ├── customer/                  # Customer portal pages
│   ├── layouts/                   # Base layout templates
│   └── partials/                  # Reusable template components
└── static/                        # Static assets
    ├── assets/
    │   ├── css/                   # Stylesheets and SCSS
    │   ├── js/                    # JavaScript functionality
    │   └── images/                # Image resources
    └── vendors/                   # Third-party libraries
```

## Database Models

### User Model
- `user_id`: Primary key
- `email`: Unique user email
- `password_hash`: Encrypted password
- `role`: Admin or Customer
- `created_at`: Account creation timestamp
- `is_active`: Account status for login control

### CustomerProfile Model
- `customer_id`: Primary key
- `user_id`: Foreign key to User
- `phone`: Contact number
- `address`: Customer address
- `national_id`: Government ID
- `created_at`: Profile creation timestamp

### Loan Model
- `loan_id`: Primary key
- `customer_id`: Foreign key to CustomerProfile
- `amount`: Principal loan amount
- `interest_rate`: Annual interest rate
- `tenure_month`: Loan duration in months
- `start_date`: Loan commencement date
- `status`: Active or Closed
- `total_payable`: Total amount due (principal + interest)
- `created_at`: Loan creation timestamp

### RepaymentSchedule Model
- Tracks individual installment payments
- Manages payment status (Pending, Paid, Overdue)
- Records amount due and amount paid
- Stores due dates for each installment

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.8 or higher
- Git
- pip (Python package manager)

## Getting Started

Follow these steps to set up and run the project locally on your machine.

### 1. Clone the Repository

```bash
git clone -b "impl-ui/visa" <repository-url>
cd loan-mgm
```

### 2. Set Up the Virtual Environment

Create a fresh virtual environment to manage dependencies locally.

```bash
python -m venv .venv
```

On Windows:
```bash
.venv\Scripts\activate
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Ensure your virtual environment is active, then install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///loan_management.db
FLASK_ENV=development
FLASK_APP=app.py
```

**Note**: The `.env` file should not be committed to version control as it contains sensitive information.

### 5. Initialize the Database

The database tables are automatically created when the application starts. However, you may want to seed initial admin data for testing.

### 6. Run the Application

Start the Flask development server:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`

## Usage

### Admin Access
1. Navigate to the login page
2. Use admin credentials
3. Access the admin dashboard to manage all system data

### Customer Access
1. Login with customer credentials
2. View personal loan portfolio
3. Access repayment schedules and payment history

## Key Endpoints

### Authentication
- `GET/POST /` - Login page

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET/POST /admin/borrower/*` - Manage borrowers
- `GET/POST /admin/loan/*` - Manage loans
- `GET /admin/report` - Financial reports

### Customer Routes
- `GET /customer/dashboard` - Customer dashboard
- `GET /customer/loan` - View loans
- `GET /customer/schedule` - View repayment schedules
- `GET /customer/profile` - Manage profile

## Additional Features

- **Responsive Design**: Mobile-friendly interface for all devices
- **Interactive Charts**: Visual representation of financial data using Chart.js
- **Data Validation**: Server-side and client-side validation
- **Security**: Password hashing, CSRF protection, and role-based access control
- **Audit Logging**: Track system activities and changes

## Development Notes

- The application uses SQLAlchemy for ORM with support for multiple database engines
- Custom decorators enforce role-based access control
- Flask blueprints organize routes by functionality
- Jinja2 templating enables dynamic content rendering
- SCSS/CSS provides a professional and consistent UI

## Troubleshooting

### Database Issues
- Ensure the database path in `.env` is correct
- Check that you have write permissions to the database directory
- For fresh database setup, delete the existing database file and restart the app

### Login Issues
- Verify credentials are correct
- Check that the user account is marked as active (is_active=True)
- Ensure SECRET_KEY is properly set in .env

## Future Enhancements

- Email notifications for payment reminders
- SMS notifications for important updates
- Advanced reporting and analytics
- Loan application workflow automation
- Mobile app integration
- Payment gateway integration

## Support

For issues or questions, please refer to the documentation or contact the development team.