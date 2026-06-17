# OG Urban Kicks Admin Dashboard

A cloud-based admin dashboard built for **OG Urban Kicks**, a premium men’s footwear, apparel, and accessories brand.

The dashboard helps business owners and managers track sales, inventory, products, expenses, profit, stock levels, and overall store performance from one clean interface.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Live Demo](#live-demo)
* [Screenshots](#screenshots)
* [Key Features](#key-features)
* [Dashboard Pages](#dashboard-pages)
* [Tech Stack](#tech-stack)
* [Project Architecture](#project-architecture)
* [Database Structure](#database-structure)
* [Project Folder Structure](#project-folder-structure)
* [Local Setup](#local-setup)
* [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
* [Environment Variables and Secrets](#environment-variables-and-secrets)
* [Security Notes](#security-notes)
* [Business Value](#business-value)
* [Skills Demonstrated](#skills-demonstrated)
* [Future Improvements](#future-improvements)
* [Project Status](#project-status)
* [Author](#author)

---

## Project Overview

**OG Urban Kicks Admin Dashboard** is a business intelligence and admin management dashboard designed for a fashion retail business.

The project uses a cloud-hosted **Aiven MySQL database** as the backend data source and a **Streamlit web application** as the dashboard interface.

The dashboard allows users to monitor important business metrics such as:

* Total sales
* Total profit
* Total orders
* Profit margin
* Product performance
* Inventory status
* Low-stock products
* Out-of-stock products
* Expenses
* Stock value

This project was built as a professional portfolio project to demonstrate database integration, business analytics, dashboard development, cloud deployment, and secure secret management.

---

## Live Demo

**Live Dashboard:** Add your Streamlit Cloud link here
**GitHub Repository:** Add your GitHub repository link here

Example:

```text
Live Dashboard: https://your-app-name.streamlit.app
GitHub Repository: https://github.com/Kennedy-og/og-urban-kicks-dashboard
```

---

## Screenshots

Add screenshots of your dashboard here.

Example:

```markdown
![Dashboard Overview](assets/dashboard-overview.png)
![Inventory Page](assets/inventory-page.png)
![Admin Actions](assets/admin-actions.png)
```

---

## Key Features

### Business KPIs

The dashboard displays major business performance indicators including:

* Total sales
* Total profit
* Total orders
* Profit margin
* Average order value
* Total products
* Stock value
* Low-stock items
* Out-of-stock items
* Total expenses
* Expense ratio

---

### Sales Analysis

The sales page allows users to analyze store sales performance.

Features include:

* Sales summary
* Sales by staff
* Sales records table
* Date range filtering
* Sales performance chart

---

### Inventory Management

The inventory page helps track product stock levels.

Features include:

* Total product count
* Low-stock count
* Out-of-stock count
* Inventory status filter
* Inventory status chart
* Full inventory table

---

### Product Performance

The product page shows how each product is performing.

Features include:

* Top products by sales
* Top products by profit
* Product sales table
* Category filter

---

### Expense Tracking

The expenses page helps track business costs.

Features include:

* Total expenses
* Expense ratio
* Expenses by type
* Expense records table

---

### Admin Actions

The admin page allows users to update the database directly from the dashboard.

Current admin actions include:

* Add new expense
* Update product stock quantity
* Add new product

---

## Dashboard Pages

The dashboard contains six main pages:

| Page          | Purpose                                       |
| ------------- | --------------------------------------------- |
| Overview      | Shows major business KPIs and summary charts  |
| Sales         | Tracks sales performance and staff sales      |
| Inventory     | Monitors stock levels and inventory status    |
| Products      | Analyzes product sales and profit             |
| Expenses      | Tracks business expenses                      |
| Admin Actions | Allows admin users to update database records |

---

## Tech Stack

| Technology             | Purpose                               |
| ---------------------- | ------------------------------------- |
| Python                 | Main programming language             |
| Streamlit              | Web dashboard interface               |
| MySQL                  | Relational database                   |
| Aiven MySQL            | Cloud database hosting                |
| Pandas                 | Data loading and analysis             |
| Plotly                 | Interactive charts and visualizations |
| mysql-connector-python | MySQL database connection             |
| Git                    | Version control                       |
| GitHub                 | Code hosting                          |
| Streamlit Cloud        | Web app deployment                    |

---

## Project Architecture

```text
Aiven MySQL Database
        ↓
Python MySQL Connection
        ↓
Pandas Data Processing
        ↓
Plotly Charts
        ↓
Streamlit Dashboard
        ↓
Streamlit Cloud Deployment
```

The dashboard connects securely to the cloud database, runs SQL queries, processes the returned data with Pandas, and displays the insights using Streamlit and Plotly.

---

## Database Structure

The project uses the following database tables:

| Table      | Description                                                                  |
| ---------- | ---------------------------------------------------------------------------- |
| suppliers  | Stores supplier information                                                  |
| staff      | Stores staff information                                                     |
| products   | Stores product details such as name, category, cost price, and selling price |
| inventory  | Stores stock quantity, reorder level, and stock update information           |
| sales      | Stores sales transaction records                                             |
| sale_items | Stores products sold within each sale                                        |
| expenses   | Stores business expense records                                              |

---

## Project Folder Structure

```text
og-urban-kicks-dashboard/
│
├── assets/
│   └── og_logo.png
│
├── app.py
├── db_setup.py
├── test_connection.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

> Note: `.streamlit/secrets.toml` and `ca.pem` should not be pushed to GitHub.

---

## Local Setup

Follow the steps below to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Kennedy-og/og-urban-kicks-dashboard.git
```

```bash
cd og-urban-kicks-dashboard
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create Streamlit Secrets

Create a folder named:

```text
.streamlit
```

Inside it, create a file named:

```text
secrets.toml
```

Add your local database credentials:

```toml
[mysql]
host = "your-aiven-host"
port = 10491
user = "avnadmin"
password = "your-database-password"
database = "defaultdb"
ssl_ca = "ca.pem"
```

---

### 5. Add Aiven SSL Certificate Locally

Download the Aiven CA certificate and save it in the project root folder as:

```text
ca.pem
```

Your local project should look like this:

```text
og-urban-kicks-dashboard/
├── app.py
├── ca.pem
├── db_setup.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```

---

### 6. Test Database Connection

Run:

```bash
python test_connection.py
```

If the connection is successful, you should see a message showing that Python connected to MySQL.

---

### 7. Run Database Setup

Run:

```bash
python db_setup.py
```

This creates the database tables and inserts sample OG Urban Kicks data.

---

### 8. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser.

---

## Streamlit Cloud Deployment

The project is deployed using **Streamlit Cloud**.

Deployment steps:

1. Push the project to GitHub.
2. Go to Streamlit Cloud.
3. Create a new app.
4. Select the GitHub repository.
5. Select the main branch.
6. Set the main file path as:

```text
app.py
```

7. Add database secrets in Streamlit Cloud.
8. Deploy the app.

---

## Environment Variables and Secrets

For Streamlit Cloud, do not use:

```toml
ssl_ca = "ca.pem"
```

because the `ca.pem` file is not pushed to GitHub.

Instead, paste the full certificate inside Streamlit Cloud Secrets:

```toml
[mysql]
host = "your-aiven-host"
port = 10491
user = "avnadmin"
password = '''your-database-password'''
database = "defaultdb"
ssl_ca = """
-----BEGIN CERTIFICATE-----
PASTE_FULL_AIVEN_CA_CERTIFICATE_HERE
-----END CERTIFICATE-----
"""
```

The app is designed to support both:

* Local SSL file path: `ssl_ca = "ca.pem"`
* Streamlit Cloud certificate text using triple quotes

---

## Security Notes

The following files must not be pushed to GitHub:

```text
.streamlit/secrets.toml
ca.pem
.env
```

These files may contain sensitive information such as:

* Database password
* SSL certificate
* Private connection details

They should be added to `.gitignore`.

Recommended `.gitignore`:

```text
.streamlit/secrets.toml
ca.pem
.env
__pycache__/
*.pyc
venv/
.venv/
```

If a password is accidentally committed, reset the password immediately and remove it from Git history before pushing again.

---

## Business Value

This dashboard provides real business value for a retail fashion brand by helping the owner:

* Track sales performance
* Monitor profit
* Identify top-selling products
* Detect low-stock products early
* Track business expenses
* Understand product performance
* Make better business decisions using data
* Manage store data from one central dashboard

---

## Skills Demonstrated

This project demonstrates the following technical and business skills:

* Python programming
* SQL database design
* MySQL database management
* Cloud database connection
* Streamlit app development
* Data analysis with Pandas
* Interactive visualization with Plotly
* Dashboard UI design
* Business intelligence reporting
* Git and GitHub workflow
* Streamlit Cloud deployment
* Secure secret management
* CRUD-style admin actions
* Retail analytics

---

## Future Improvements

Possible future improvements include:

* Add record new sale feature
* Add staff management page
* Add supplier management page
* Add product edit and delete feature
* Add authentication and login system
* Add role-based admin access
* Add downloadable PDF/CSV reports
* Add customer records
* Add monthly sales forecasting
* Add profit prediction model
* Add AI-powered sales recommendations
* Add mobile-responsive improvements

---

## Project Status

The project is currently a working deployed prototype.

Current completed milestones:

* Cloud MySQL database setup
* Secure Streamlit connection to Aiven MySQL
* Streamlit Cloud deployment
* Dashboard pages
* KPIs and charts
* Inventory tracking
* Expense tracking
* Admin update actions
* GitHub version control

---

## Author

**Kennedy OG**

Python Developer | Data Analytics | Business Intelligence | Dashboard Development

---
