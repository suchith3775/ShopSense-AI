import streamlit as st
from datetime import date
import pandas as pd

st.set_page_config(page_title="ShopSense AI", page_icon="🛍️", layout="wide")

# Beginner-friendly prototype: data lives in Streamlit session memory.
# It resets when the app session restarts. Do not use real customer data yet.

def money(value):
    return f"₹{value:,.2f}"

if "products" not in st.session_state:
    st.session_state.products = [
        {"name": "Milk packet", "price": 28.0, "stock": 20, "low_stock": 5},
        {"name": "Bread", "price": 35.0, "stock": 12, "low_stock": 4},
        {"name": "Eggs (piece)", "price": 7.0, "stock": 30, "low_stock": 10},
    ]
if "sales" not in st.session_state:
    st.session_state.sales = []
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if "credits" not in st.session_state:
    st.session_state.credits = []

st.title("🛍️ ShopSense AI")
st.caption("Simple shop management prototype • Version 0.1")
st.info("Demo mode: data is temporary and resets when the app session restarts. Use sample data only.")

pages = ["Dashboard", "Inventory", "Record a sale", "Expenses", "Digital Khata"]
page = st.sidebar.radio("Go to", pages)
st.sidebar.caption("Built for a small-shop pilot")

products = st.session_state.products

if page == "Dashboard":
    today_sales = sum(x["total"] for x in st.session_state.sales if x["date"] == str(date.today()))
    today_expenses = sum(x["amount"] for x in st.session_state.expenses if x["date"] == str(date.today()))
    today_cost = sum(x["cost"] for x in st.session_state.sales if x["date"] == str(date.today()))
    estimated_profit = today_sales - today_cost - today_expenses
    low_items = [p for p in products if p["stock"] <= p["low_stock"]]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Today's sales", money(today_sales))
    c2.metric("Today's expenses", money(today_expenses))
    c3.metric("Estimated profit*", money(estimated_profit))
    c4.metric("Products", len(products))

    st.subheader("⚠️ Low-stock alerts")
    if low_items:
        for p in low_items:
            st.warning(f'{p["name"]}: only {p["stock"]} left (alert at {p["low_stock"]})')
    else:
        st.success("No low-stock items right now.")

    st.subheader("Recent sales")
    if st.session_state.sales:
        st.dataframe(pd.DataFrame(st.session_state.sales).tail(10), use_container_width=True, hide_index=True)
    else:
        st.write("No sales recorded yet. Go to **Record a sale** to try it.")

    st.caption("*Estimated profit here = sales revenue − estimated product cost − expenses. This demo does not yet track supplier purchase costs, taxes, returns, or credit accounting in full.")

elif page == "Inventory":
    st.subheader("Inventory")
    if products:
        st.dataframe(pd.DataFrame(products), use_container_width=True, hide_index=True)
    else:
        st.write("No products yet.")

    st.subheader("Add a product")
    with st.form("add_product", clear_on_submit=True):
        name = st.text_input("Product name")
        price = st.number_input("Selling price (₹)", min_value=0.0, value=10.0, step=1.0)
        stock = st.number_input("Opening stock", min_value=0, value=0, step=1)
        threshold = st.number_input("Low-stock alert when stock is at or below", min_value=0, value=5, step=1)
        submitted = st.form_submit_button("Add product")
        if submitted:
            if not name.strip():
                st.error("Enter a product name.")
            elif any(p["name"].lower() == name.strip().lower() for p in products):
                st.error("That product already exists. Use a unique name for this prototype.")
            else:
                products.append({"name": name.strip(), "price": float(price), "stock": int(stock), "low_stock": int(threshold)})
                st.success(f"Added {name.strip()}.")
                st.rerun()

    st.subheader("Adjust stock")
    names = [p["name"] for p in products]
    if names:
        selected = st.selectbox("Choose product", names, key="stock_product")
        adjustment = st.number_input("Change in stock (+ to add, − to remove)", value=0, step=1)
        if st.button("Update stock"):
            product = next(p for p in products if p["name"] == selected)
            if product["stock"] + int(adjustment) < 0:
                st.error("Stock cannot go below zero.")
            else:
                product["stock"] += int(adjustment)
                st.success(f'Updated {selected}: {product["stock"]} in stock.')
                st.rerun()

elif page == "Record a sale":
    st.subheader("Record a sale")
    names = [p["name"] for p in products]
    if not names:
        st.warning("Add a product in Inventory first.")
    else:
        with st.form("record_sale", clear_on_submit=True):
            selected = st.selectbox("Product", names)
            quantity = st.number_input("Quantity sold", min_value=1, value=1, step=1)
            payment = st.selectbox("Payment method", ["Cash", "UPI", "Credit"])
            customer = st.text_input("Customer name (required for credit; use a nickname in this demo)")
            submitted = st.form_submit_button("Save sale")
            if submitted:
                product = next(p for p in products if p["name"] == selected)
                if quantity > product["stock"]:
                    st.error(f'Only {product["stock"]} available.')
                elif payment == "Credit" and not customer.strip():
                    st.error("Enter a customer name for a credit sale.")
                else:
                    total = product["price"] * int(quantity)
                    # Cost is unknown in v0.1, so it is left at zero and profit is only a rough estimate.
                    st.session_state.sales.append({
                        "date": str(date.today()), "product": selected, "quantity": int(quantity),
                        "unit_price": product["price"], "total": total, "payment": payment,
                        "customer": customer.strip() if payment == "Credit" else "",
                        "cost": 0.0
                    })
                    product["stock"] -= int(quantity)
                    if payment == "Credit":
                        st.session_state.credits.append({
                            "date": str(date.today()), "customer": customer.strip(),
                            "description": f"{quantity} × {selected}", "amount": total, "paid": 0.0
                        })
                    st.success(f"Sale saved: {quantity} × {selected} = {money(total)}")
                    st.rerun()

    st.subheader("Sales history")
    if st.session_state.sales:
        st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True, hide_index=True)
        csv = pd.DataFrame(st.session_state.sales).to_csv(index=False).encode("utf-8")
        st.download_button("Download sales CSV", csv, "shopsense_sales.csv", "text/csv")
    else:
        st.write("No sales recorded yet.")

elif page == "Expenses":
    st.subheader("Record an expense")
    with st.form("add_expense", clear_on_submit=True):
        description = st.text_input("Expense description (e.g., delivery, electricity)")
        amount = st.number_input("Amount (₹)", min_value=0.0, value=0.0, step=10.0)
        submitted = st.form_submit_button("Save expense")
        if submitted:
            if not description.strip():
                st.error("Enter an expense description.")
            elif amount <= 0:
                st.error("Enter an amount greater than zero.")
            else:
                st.session_state.expenses.append({
                    "date": str(date.today()), "description": description.strip(), "amount": float(amount)
                })
                st.success("Expense saved.")
                st.rerun()

    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True, hide_index=True)
        csv = pd.DataFrame(st.session_state.expenses).to_csv(index=False).encode("utf-8")
        st.download_button("Download expenses CSV", csv, "shopsense_expenses.csv", "text/csv")
    else:
        st.write("No expenses recorded yet.")

elif page == "Digital Khata":
    st.subheader("Digital Khata — customer credit")
    st.caption("Use fake names and sample amounts only. This is a demo, not a reliable accounting system.")
    if st.session_state.credits:
        credits_df = pd.DataFrame(st.session_state.credits)
        credits_df["balance"] = credits_df["amount"] - credits_df["paid"]
        st.dataframe(credits_df, use_container_width=True, hide_index=True)
        st.metric("Total outstanding credit", money(credits_df["balance"].sum()))
    else:
        st.write("No credit entries yet. Record a sale and choose **Credit** to add one.")

    st.subheader("Record a repayment")
    customers = sorted(set(x["customer"] for x in st.session_state.credits))
    if customers:
        with st.form("repayment", clear_on_submit=True):
            customer = st.selectbox("Customer", customers)
            outstanding = sum(x["amount"] - x["paid"] for x in st.session_state.credits if x["customer"] == customer)
            st.write(f"Outstanding for this customer: **{money(outstanding)}**")
            amount = st.number_input("Repayment amount (₹)", min_value=0.0, value=0.0, step=10.0)
            submitted = st.form_submit_button("Save repayment")
            if submitted:
                if amount <= 0:
                    st.error("Enter an amount greater than zero.")
                elif amount > outstanding:
                    st.error("Repayment cannot exceed the outstanding balance.")
                else:
                    remaining = amount
                    for entry in st.session_state.credits:
                        if entry["customer"] == customer and remaining > 0:
                            due = entry["amount"] - entry["paid"]
                            applied = min(due, remaining)
                            entry["paid"] += applied
                            remaining -= applied
                    st.success("Repayment recorded.")
                    st.rerun()
    else:
        st.write("No customer credit balances to repay yet.")

st.sidebar.divider()
st.sidebar.caption("Prototype only • Not ready for real financial records")
