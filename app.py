import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from pathlib import Path
import tempfile
import socket

config = st.secrets["mysql"]

st.sidebar.markdown("### Database Debug")
st.sidebar.write("Host:", config["host"])
st.sidebar.write("Port:", config["port"])

st.sidebar.markdown("### Database Debug")
st.sidebar.write("Host:", config["host"])
st.sidebar.write("Port:", config["port"])

try:
    test_conn = get_connection()
    test_conn.close()
    st.sidebar.success("MySQL login OK")
except mysql.connector.Error as e:
    st.sidebar.error(f"MySQL failed: errno={e.errno}, sqlstate={e.sqlstate}")
    st.sidebar.error(f"Message: {e.msg}")
except Exception as e:
    st.sidebar.error(f"General error: {type(e).__name__}: {e}")
    

st.set_page_config(
    page_title="OG Urban Kicks Admin Dashboard",
    layout="wide"
)

config = st.secrets["mysql"]
logo_path = Path("assets/og_logo.png")

brand_colors = ["#3B2416", "#6B4423", "#A47551", "#C8A27A", "#E8D5BD"]


def apply_brand_style():
    st.markdown(
        """
        <style>
        /*
        This style keeps OG Urban Kicks brown/cream branding,
        but does NOT force the main Streamlit background.
        So Streamlit Light/Dark mode can work naturally.
        */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Sidebar blends with Streamlit theme */
        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(164, 117, 81, 0.35);
        }

        /* Headings inherit Streamlit light/dark text color */
        h1, h2, h3, h4 {
            color: inherit !important;
            font-weight: 700 !important;
        }

        /* Captions */
        .stCaption, caption {
            opacity: 0.75;
        }

        /* Metric cards with brown boutique details */
        div[data-testid="stMetric"] {
            background: rgba(164, 117, 81, 0.08);
            border: 1px solid rgba(164, 117, 81, 0.45);
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 8px 20px rgba(59, 36, 22, 0.08);
        }

        div[data-testid="stMetricLabel"] {
            color: #A47551 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetricValue"] {
            color: inherit !important;
            font-weight: 700 !important;
        }

        /* Inputs keep brown borders but preserve Streamlit theme background */
        input, textarea {
            border-color: rgba(164, 117, 81, 0.55) !important;
        }

        div[data-baseweb="select"] > div {
            border-color: rgba(164, 117, 81, 0.55) !important;
        }

        div[data-testid="stDateInput"] input {
            border-color: rgba(164, 117, 81, 0.55) !important;
        }

        /* Buttons stay branded */
        .stButton > button,
        button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button {
            background-color: #6B4423 !important;
            color: #FFF8EF !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            background-color: #3B2416 !important;
            color: #FFF8EF !important;
        }

        /* Dataframes */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(164, 117, 81, 0.45);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 8px 20px rgba(59, 36, 22, 0.06);
        }

        /* Plotly chart container */
        .js-plotly-plot {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(164, 117, 81, 0.45);
            box-shadow: 0 8px 20px rgba(59, 36, 22, 0.06);
        }

        /* Divider */
        hr {
            border-color: rgba(164, 117, 81, 0.35);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


apply_brand_style()


def get_connection():
    return mysql.connector.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        ssl_ca=config["ssl_ca"]
    )


@st.cache_data(ttl=300)
def load_data(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def execute_query(query, values=None):
    conn = get_connection()
    cursor = conn.cursor()

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

    st.cache_data.clear()


def add_product_with_inventory(
    product_name,
    category,
    supplier_id,
    cost_price,
    selling_price,
    expiry_date,
    stock_quantity,
    reorder_level
):
    conn = get_connection()
    cursor = conn.cursor()

    insert_product_query = """
    INSERT INTO products
    (product_name, category, supplier_id, cost_price, selling_price, expiry_date)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    cursor.execute(
        insert_product_query,
        (
            product_name,
            category,
            supplier_id,
            cost_price,
            selling_price,
            expiry_date
        )
    )

    new_product_id = cursor.lastrowid

    insert_inventory_query = """
    INSERT INTO inventory
    (product_id, stock_quantity, reorder_level, last_updated)
    VALUES (%s, %s, %s, CURDATE());
    """

    cursor.execute(
        insert_inventory_query,
        (
            new_product_id,
            stock_quantity,
            reorder_level
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    st.cache_data.clear()


def get_sales_data(start_date, end_date):
    query = """
    SELECT 
        s.sale_id,
        s.sale_date,
        st.staff_name,
        s.payment_method,
        s.total_amount,
        SUM(si.profit) AS profit
    FROM sales s
    LEFT JOIN staff st ON s.staff_id = st.staff_id
    LEFT JOIN sale_items si ON s.sale_id = si.sale_id
    WHERE s.sale_date BETWEEN %s AND %s
    GROUP BY s.sale_id, s.sale_date, st.staff_name, s.payment_method, s.total_amount
    ORDER BY s.sale_date;
    """

    df = load_data(query, (start_date, end_date))
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df


def get_inventory_data():
    query = """
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        sp.supplier_name,
        p.cost_price,
        p.selling_price,
        p.expiry_date,
        i.stock_quantity,
        i.reorder_level,
        CASE
            WHEN i.stock_quantity = 0 THEN 'Out of Stock'
            WHEN i.stock_quantity <= i.reorder_level THEN 'Low Stock'
            ELSE 'In Stock'
        END AS stock_status
    FROM products p
    LEFT JOIN suppliers sp ON p.supplier_id = sp.supplier_id
    LEFT JOIN inventory i ON p.product_id = i.product_id
    ORDER BY p.product_name;
    """

    df = load_data(query)
    df["expiry_date"] = pd.to_datetime(df["expiry_date"])
    return df


def get_product_sales_data():
    query = """
    SELECT
        p.product_name,
        p.category,
        SUM(si.quantity) AS quantity_sold,
        SUM(si.total_price) AS total_sales,
        SUM(si.profit) AS total_profit
    FROM sale_items si
    JOIN products p ON si.product_id = p.product_id
    GROUP BY p.product_name, p.category
    ORDER BY total_sales DESC;
    """

    return load_data(query)


def get_expenses_data():
    query = """
    SELECT 
        expense_date,
        expense_type,
        amount,
        note
    FROM expenses
    ORDER BY expense_date DESC;
    """

    df = load_data(query)
    df["expense_date"] = pd.to_datetime(df["expense_date"])
    return df


def get_suppliers_data():
    query = """
    SELECT 
        supplier_id,
        supplier_name
    FROM suppliers
    ORDER BY supplier_name;
    """

    return load_data(query)


def get_date_range():
    query = """
    SELECT 
        MIN(sale_date) AS min_date,
        MAX(sale_date) AS max_date
    FROM sales;
    """

    return load_data(query)


def get_categories():
    query = """
    SELECT DISTINCT category
    FROM products
    WHERE category IS NOT NULL
    ORDER BY category;
    """

    return load_data(query)


def calculate_sales_kpis(sales_df):
    total_sales = sales_df["total_amount"].sum()
    total_profit = sales_df["profit"].sum()
    total_orders = sales_df["sale_id"].nunique()

    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    average_order_value = (total_sales / total_orders) if total_orders > 0 else 0

    return total_sales, total_profit, total_orders, profit_margin, average_order_value


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=None),
        title=dict(font=dict(color=None)),
        xaxis=dict(
            gridcolor="rgba(164, 117, 81, 0.25)",
            zerolinecolor="rgba(164, 117, 81, 0.35)"
        ),
        yaxis=dict(
            gridcolor="rgba(164, 117, 81, 0.25)",
            zerolinecolor="rgba(164, 117, 81, 0.35)"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig


# ---------------- HEADER ----------------

header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    if logo_path.exists():
        st.image(str(logo_path), width=120)
    else:
        st.warning("Logo not found. Put your logo at assets/og_logo.png")

with header_col2:
    st.title("OG Urban Kicks Admin Dashboard")
    st.caption(
        "Business dashboard for tracking footwear sales, inventory, profit, expenses, and product performance."
    )


# ---------------- SIDEBAR ----------------

if logo_path.exists():
    st.sidebar.image(str(logo_path), width=120)
else:
    st.sidebar.warning("Logo missing")

st.sidebar.title("OG Urban Kicks")
st.sidebar.caption("Footwear • Apparel • Accessories")

page = st.sidebar.radio(
    "Go to",
    ["Overview", "Sales", "Inventory", "Products", "Expenses", "Admin Actions"]
)

st.sidebar.divider()

date_range_df = get_date_range()

min_date = pd.to_datetime(date_range_df.loc[0, "min_date"]).date()
max_date = pd.to_datetime(date_range_df.loc[0, "max_date"]).date()

selected_date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
else:
    start_date, end_date = min_date, max_date

categories_df = get_categories()
category_options = ["All"] + categories_df["category"].dropna().tolist()

selected_category = st.sidebar.selectbox("Category", category_options)


# ---------------- OVERVIEW PAGE ----------------

if page == "Overview":
    with st.spinner("Loading overview data..."):
        sales_df = get_sales_data(start_date, end_date)
        inventory_df = get_inventory_data()
        product_sales_df = get_product_sales_data()
        expenses_df = get_expenses_data()

    if selected_category != "All":
        product_sales_df = product_sales_df[product_sales_df["category"] == selected_category]

    total_sales, total_profit, total_orders, profit_margin, average_order_value = calculate_sales_kpis(sales_df)

    total_products = inventory_df["product_id"].nunique()
    low_stock_items = inventory_df[inventory_df["stock_status"] == "Low Stock"].shape[0]
    out_of_stock_items = inventory_df[inventory_df["stock_status"] == "Out of Stock"].shape[0]
    stock_value = (inventory_df["stock_quantity"] * inventory_df["cost_price"]).sum()

    st.subheader("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"₦{total_sales:,.0f}")
    col2.metric("Total Profit", f"₦{total_profit:,.0f}")
    col3.metric("Total Orders", f"{total_orders:,}")
    col4.metric("Profit Margin", f"{profit_margin:.1f}%")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Products", f"{total_products:,}")
    col6.metric("Low Stock", f"{low_stock_items:,}")
    col7.metric("Out of Stock", f"{out_of_stock_items:,}")
    col8.metric("Stock Value", f"₦{stock_value:,.0f}")

    st.divider()

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        sales_trend = sales_df.groupby("sale_date", as_index=False)["total_amount"].sum()

        fig = px.line(
            sales_trend,
            x="sale_date",
            y="total_amount",
            markers=True,
            title="Sales Trend",
            color_discrete_sequence=["#6B4423"]
        )

        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        category_sales = product_sales_df.groupby("category", as_index=False)["total_sales"].sum()

        fig = px.bar(
            category_sales,
            x="category",
            y="total_sales",
            title="Sales by Category",
            color_discrete_sequence=["#A47551"]
        )

        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        payment_data = sales_df.groupby("payment_method", as_index=False)["total_amount"].sum()

        fig = px.pie(
            payment_data,
            names="payment_method",
            values="total_amount",
            title="Payment Method Breakdown",
            color_discrete_sequence=brand_colors
        )

        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with chart_col4:
        stock_status = inventory_df["stock_status"].value_counts().reset_index()
        stock_status.columns = ["stock_status", "count"]

        fig = px.pie(
            stock_status,
            names="stock_status",
            values="count",
            title="Inventory Status",
            color_discrete_sequence=brand_colors
        )

        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Low Stock and Out of Stock Items")

    st.dataframe(
        inventory_df[inventory_df["stock_status"].isin(["Low Stock", "Out of Stock"])],
        use_container_width=True
    )


# ---------------- SALES PAGE ----------------

elif page == "Sales":
    with st.spinner("Loading sales data..."):
        sales_df = get_sales_data(start_date, end_date)

    total_sales, total_profit, total_orders, profit_margin, average_order_value = calculate_sales_kpis(sales_df)

    st.subheader("Sales Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₦{total_sales:,.0f}")
    col2.metric("Average Order Value", f"₦{average_order_value:,.0f}")
    col3.metric("Total Profit", f"₦{total_profit:,.0f}")

    st.divider()

    staff_sales = sales_df.groupby("staff_name", as_index=False)["total_amount"].sum()

    fig = px.bar(
        staff_sales,
        x="staff_name",
        y="total_amount",
        title="Sales by Staff",
        color_discrete_sequence=["#6B4423"]
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sales Records")

    st.dataframe(sales_df, use_container_width=True)


# ---------------- INVENTORY PAGE ----------------

elif page == "Inventory":
    with st.spinner("Loading inventory data..."):
        inventory_df = get_inventory_data()

    total_products = inventory_df["product_id"].nunique()
    low_stock_items = inventory_df[inventory_df["stock_status"] == "Low Stock"].shape[0]
    out_of_stock_items = inventory_df[inventory_df["stock_status"] == "Out of Stock"].shape[0]

    st.subheader("Inventory Management")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", f"{total_products:,}")
    col2.metric("Low Stock Items", f"{low_stock_items:,}")
    col3.metric("Out of Stock Items", f"{out_of_stock_items:,}")

    st.divider()

    status_filter = st.selectbox(
        "Filter by stock status",
        ["All", "In Stock", "Low Stock", "Out of Stock"]
    )

    inventory_view = inventory_df.copy()

    if status_filter != "All":
        inventory_view = inventory_view[inventory_view["stock_status"] == status_filter]

    stock_status = inventory_df["stock_status"].value_counts().reset_index()
    stock_status.columns = ["stock_status", "count"]

    fig = px.bar(
        stock_status,
        x="stock_status",
        y="count",
        title="Inventory Status Count",
        color_discrete_sequence=["#A47551"]
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Inventory Table")

    st.dataframe(inventory_view, use_container_width=True)


# ---------------- PRODUCTS PAGE ----------------

elif page == "Products":
    with st.spinner("Loading product data..."):
        product_sales_df = get_product_sales_data()

    if selected_category != "All":
        product_sales_df = product_sales_df[product_sales_df["category"] == selected_category]

    st.subheader("Product Performance")

    top_products = product_sales_df.sort_values("total_sales", ascending=False).head(10)

    fig = px.bar(
        top_products,
        x="total_sales",
        y="product_name",
        orientation="h",
        title="Top Products by Sales",
        color_discrete_sequence=["#6B4423"]
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        top_products,
        x="total_profit",
        y="product_name",
        orientation="h",
        title="Top Products by Profit",
        color_discrete_sequence=["#A47551"]
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Product Sales Table")

    st.dataframe(product_sales_df, use_container_width=True)


# ---------------- EXPENSES PAGE ----------------

elif page == "Expenses":
    with st.spinner("Loading expenses data..."):
        expenses_df = get_expenses_data()
        sales_df = get_sales_data(start_date, end_date)

    total_sales, total_profit, total_orders, profit_margin, average_order_value = calculate_sales_kpis(sales_df)

    total_expenses = expenses_df["amount"].sum()
    expense_ratio = (total_expenses / total_sales * 100) if total_sales > 0 else 0

    st.subheader("Expenses")

    col1, col2 = st.columns(2)

    col1.metric("Total Expenses", f"₦{total_expenses:,.0f}")
    col2.metric("Expense Ratio", f"{expense_ratio:.1f}%")

    st.divider()

    expense_by_type = expenses_df.groupby("expense_type", as_index=False)["amount"].sum()

    fig = px.bar(
        expense_by_type,
        x="expense_type",
        y="amount",
        title="Expenses by Type",
        color_discrete_sequence=["#6B4423"]
    )

    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Expense Records")

    st.dataframe(expenses_df, use_container_width=True)


# ---------------- ADMIN ACTIONS PAGE ----------------

elif page == "Admin Actions":
    st.subheader("Admin Actions")
    st.caption("Use this page to update the OG Urban Kicks store database.")

    action = st.selectbox(
        "Choose action",
        ["Add Expense", "Update Stock Quantity", "Add New Product"]
    )

    st.divider()

    if action == "Add Expense":
        st.markdown("### Add New Expense")

        with st.form("add_expense_form"):
            expense_date = st.date_input("Expense Date")
            expense_type = st.text_input(
                "Expense Type",
                placeholder="e.g. Delivery, Rent, Electricity, Packaging"
            )
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=100.0
            )
            note = st.text_area(
                "Note",
                placeholder="Optional note about this expense"
            )

            submitted = st.form_submit_button("Add Expense")

            if submitted:
                if expense_type.strip() == "":
                    st.error("Expense type is required.")
                elif amount <= 0:
                    st.error("Amount must be greater than zero.")
                else:
                    query = """
                    INSERT INTO expenses (expense_date, expense_type, amount, note)
                    VALUES (%s, %s, %s, %s);
                    """

                    values = (
                        expense_date,
                        expense_type,
                        amount,
                        note
                    )

                    execute_query(query, values)
                    st.success("Expense added successfully.")
                    st.rerun()

    elif action == "Update Stock Quantity":
        st.markdown("### Update Product Stock")

        inventory_df = get_inventory_data()

        product_options = inventory_df[["product_id", "product_name", "stock_quantity"]].copy()

        product_options["display"] = (
            product_options["product_name"] +
            " | Current Stock: " +
            product_options["stock_quantity"].astype(str)
        )

        selected_product = st.selectbox(
            "Select Product",
            product_options["display"]
        )

        selected_row = product_options[product_options["display"] == selected_product].iloc[0]
        product_id = int(selected_row["product_id"])
        current_stock = int(selected_row["stock_quantity"])

        with st.form("update_stock_form"):
            new_quantity = st.number_input(
                "New Stock Quantity",
                min_value=0,
                value=current_stock,
                step=1
            )

            submitted = st.form_submit_button("Update Stock")

            if submitted:
                query = """
                UPDATE inventory
                SET stock_quantity = %s, last_updated = CURDATE()
                WHERE product_id = %s;
                """

                values = (
                    new_quantity,
                    product_id
                )

                execute_query(query, values)
                st.success("Stock quantity updated successfully.")
                st.rerun()

    elif action == "Add New Product":
        st.markdown("### Add New Product")

        suppliers_df = get_suppliers_data()

        suppliers_df["display"] = (
            suppliers_df["supplier_id"].astype(str) +
            " - " +
            suppliers_df["supplier_name"]
        )

        with st.form("add_product_form"):
            product_name = st.text_input(
                "Product Name",
                placeholder="e.g. Italian Leather Loafers"
            )

            category = st.text_input(
                "Category",
                placeholder="e.g. Sneakers, Loafers, Slides, Belts, Caps"
            )

            selected_supplier = st.selectbox(
                "Supplier",
                suppliers_df["display"]
            )

            cost_price = st.number_input(
                "Cost Price",
                min_value=0.0,
                step=100.0
            )

            selling_price = st.number_input(
                "Selling Price",
                min_value=0.0,
                step=100.0
            )

            expiry_date = st.date_input("Expiry Date")

            stock_quantity = st.number_input(
                "Opening Stock Quantity",
                min_value=0,
                step=1
            )

            reorder_level = st.number_input(
                "Reorder Level",
                min_value=0,
                step=1
            )

            submitted = st.form_submit_button("Add Product")

            if submitted:
                if product_name.strip() == "":
                    st.error("Product name is required.")
                elif category.strip() == "":
                    st.error("Category is required.")
                elif cost_price <= 0:
                    st.error("Cost price must be greater than zero.")
                elif selling_price <= cost_price:
                    st.error("Selling price should be greater than cost price.")
                else:
                    supplier_id = int(selected_supplier.split(" - ")[0])

                    add_product_with_inventory(
                        product_name,
                        category,
                        supplier_id,
                        cost_price,
                        selling_price,
                        expiry_date,
                        stock_quantity,
                        reorder_level
                    )

                    st.success("New product added successfully.")
                    st.rerun()