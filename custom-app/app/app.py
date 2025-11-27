import streamlit as st
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

# Load secrets from the configuration file
with open("/etc/dataos/config/secret.conf") as file:
    secret_json = json.load(file)

# Extracting API details from the loaded config
url = secret_json['API_URL']
api_key = secret_json['API_KEY']
payload = secret_json['PAYLOAD']

# Set up Streamlit title
st.title("🔗 Product Affinity Analysis")

# API request headers
api_url = url
headers = {
    'apikey': api_key,  # API Key
    'Content-Type': 'application/json'
}

# Load data once and store it in session state
@st.cache_data(show_spinner=True)
def load_all_data():
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                return data["data"]
            else:
                st.error("❌ 'data' not found in the response.")
                return []
        else:
            st.error(f"❌ Error fetching data: {response.status_code} {response.text}")
            return []
    except Exception as e:
        st.error(f"❌ Exception: {str(e)}")
        return []

if "fetched_data" not in st.session_state:
    st.session_state.fetched_data = load_all_data()

# Prevent tab switching by storing active tab
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "API-Fetched Data"

# Create three tabs: All Data, Customer Insights, and Dashboards
tab1, tab2, tab3 = st.tabs(["API-Fetched Data", "Customer Insights", "Product Affinity Dashboard"])

# Tab 1: Show all data in tabular format
with tab1:
    st.session_state.active_tab = "API-Fetched Data"
    st.write("### 📊 API-Fetched Data")
    
    if st.session_state.fetched_data:
        st.table(st.session_state.fetched_data)
    else:
        st.warning("⚠ No data available. Please check the API or try again later.")

# Tab 2: Customer-specific data with visual representation
with tab2:
    st.session_state.active_tab = "Customer Insights"

    customer_id = st.text_input("Enter Customer ID to search:", key="customer_search")


    if customer_id:
        try:
            customer_id = int(customer_id)
            # Filter data based on entered customer_id
            matched_data = [
                record for record in st.session_state.fetched_data 
                if record.get("customer.customer_id") == customer_id
            ]

            if matched_data:
                # Extract selected fields for the matched customer ID
                customer_info = matched_data[0]  # Get first matched record

                # Business-Friendly Display
                st.write(f"## 🧑 Customer Overview: {customer_info['customer.customer_id']}")

                col1, col2, col3 = st.columns(3)

                col1.metric("💰 Income", f"${customer_info['customer.income']:,.2f}")
                col2.metric("📆 Birth Year", customer_info["customer.birth_year"])
                col3.metric("🏡 Marital Status", customer_info["customer.marital_status"])

                st.subheader("📊 Purchase Insights")

                col4, col5, col6 = st.columns(3)
                col4.metric("🛍️ Purchase Frequency", customer_info["purchase.purchase_frequency"])
                col5.metric("💳 Average Spend", f"${customer_info['purchase.average_spend']:,.2f}")
                col6.metric("⚡ Churn Probability", customer_info['purchase.churn_probability'], help="Churn Probability Indicator")

                st.subheader("🌍 Customer Segments & Location")
                st.markdown(f"""
                    - **Customer Segment:** {customer_info['customer.customer_segments']}
                    - **Country:** {customer_info['purchase.country_name']}
                """)

            else:
                st.error(f"❌ Given customer ID '{customer_id}' is not found in the data.")
        except ValueError:
            st.error("❌ Please enter a valid numeric customer ID.")

with tab3:
    st.session_state.active_tab = "Product Affinity Dashboard"
    st.write("### 📊 Product Affinity Dashboard: KPIs and Charts")

    # Layout for KPIs in a single row (3 columns for 3 KPIs)
    col1, col2, col3 = st.columns(3)

    # KPI 1: Total Customers
    with col1:
        total_customers = sum(
            record['customer.total_customers'] for record in st.session_state.fetched_data
            if record.get('customer.total_customers') is not None
        )
        st.metric("📈 Total Customers", total_customers, help="The total number of unique customers.")

    # KPI 2: Total Revenue (In Million)
    with col2:
        total_revenue = sum(
            record['purchase.average_spend'] for record in st.session_state.fetched_data
            if record.get('purchase.average_spend') is not None
        )  # Convert to millions
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}M", help="Revenue generated across all purchases (in millions).")

    # KPI 3: Top Cross-Sell Opportunity Score
    with col3:
        cross_sell_scores = [
            float(record['purchase.cross_sell_opportunity_score']) for record in st.session_state.fetched_data
            if record.get('purchase.cross_sell_opportunity_score') is not None
        ]
        max_cross_sell = max(cross_sell_scores, default=0) if cross_sell_scores else 0
        st.metric("🔗 Top Cross-Sell Opportunity", f"{max_cross_sell:,.2f}", help="Top cross-sell opportunity score, indicating potential sales growth.")

    # Layout for charts in a 2x2 grid
    chart_col1, chart_col2 = st.columns(2)

    # Chart 1: Customer Segments Distribution (Pie Chart)
    with chart_col1:
        customer_segments = [
            record['customer.customer_segments'] for record in st.session_state.fetched_data
            if record.get('customer.customer_segments') is not None
        ]
        
        segment_counts = dict(Counter(customer_segments))
        
        labels = list(segment_counts.keys())
        values = list(segment_counts.values())

        fig, ax = plt.subplots(figsize=(4, 4))  # Larger pie chart for better clarity
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.write("📊 Customer Segments Distribution")
        st.pyplot(fig)

    # Chart 2: Average Spend Per Product Category (Bar Chart)
    with chart_col2:
        valid_data = [
            (record['product.product_category'], record['purchase.average_spend'])
            for record in st.session_state.fetched_data
            if record.get('purchase.average_spend') is not None and not pd.isna(record.get('purchase.average_spend'))
        ]
        
        df = pd.DataFrame(valid_data, columns=['product_category', 'average_spend'])
        
        avg_spend_per_category = df.groupby('product_category')['average_spend'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(avg_spend_per_category['product_category'], avg_spend_per_category['average_spend'], color='skyblue')

        ax.set_title("💸 Average Spend Per Product Category", fontsize=16, fontweight='bold')
        ax.set_xlabel("Product Category", fontsize=12)
        ax.set_ylabel("Average Spend ($)", fontsize=12)
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability

        ax.set_yticks([0, 5, 10, 20, 25, 30, 35, 40])
        
        st.pyplot(fig)

    # Layout for charts in a 2x2 grid (continued)
    chart_col3, chart_col4 = st.columns(2)

    # Chart 3: Price vs. Cross-Sell Opportunity Score (Area Chart)
    with chart_col3:
        price_vs_cross_sell = [
            (record['product.price'], record['purchase.cross_sell_opportunity_score'])
            for record in st.session_state.fetched_data
            if record.get('product.price') is not None and record.get('purchase.cross_sell_opportunity_score') is not None
        ]

        price, cross_sell = zip(*price_vs_cross_sell)

        sorted_data = sorted(zip(price, cross_sell))
        sorted_price, sorted_cross_sell = zip(*sorted_data)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(sorted_price, sorted_cross_sell, color="skyblue", alpha=0.4)

        ax.set_title("💰 Price vs. Cross-Sell Opportunity", fontsize=16, fontweight='bold')
        ax.set_xlabel("Product Price ($)", fontsize=12)
        ax.set_ylabel("Cross-Sell Opportunity Score", fontsize=12)

        st.pyplot(fig)

    # Chart 4: Purchase Frequency Over Country (Bar Chart)
    with chart_col4:
        country_frequency = [
            (item['purchase.country_name'], item['purchase.purchase_frequency'])
            for item in st.session_state.fetched_data
            if item.get('purchase.country_name') is not None and item.get('purchase.purchase_frequency') is not None
        ]

        frequency_by_country = {}
        for country, frequency in country_frequency:
            frequency_by_country[country] = frequency_by_country.get(country, 0) + frequency

        countries = list(frequency_by_country.keys())
        frequencies = list(frequency_by_country.values())

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(countries, frequencies, color='lightcoral')

        ax.set_title("🌍 Purchase Frequency by Country", fontsize=16, fontweight='bold')
        ax.set_xlabel("Country", fontsize=12)
        ax.set_ylabel("Total Purchase Frequency", fontsize=12)
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability

        st.pyplot(fig)
