import pandas as pd


def load_data():
    """
    Load raw Olist datasets
    """

    orders = pd.read_csv("data/raw/archive/olist_orders_dataset.csv")
    items = pd.read_csv("data/raw/archive/olist_order_items_dataset.csv")
    payments = pd.read_csv("data/raw/archive/olist_order_payments_dataset.csv")
    products = pd.read_csv("data/raw/archive/olist_products_dataset.csv")
    customers = pd.read_csv("data/raw/archive/olist_customers_dataset.csv")
    categories = pd.read_csv("data/raw/archive/product_category_name_translation.csv")

    return orders, items, payments, products, customers, categories


def preprocess_data():

    print("Loading datasets...")

    orders, items, payments, products, customers, categories = load_data()

    print("Merging product categories...")

    products_en = products.merge(
        categories,
        on="product_category_name",
        how="left"
    )

    print("Joining all datasets...")

    df = (
        orders
        .merge(customers, on="customer_id", how="left")
        .merge(items, on="order_id", how="left")
        .merge(products_en, on="product_id", how="left")
        .merge(payments, on="order_id", how="left")
    )

    print("Converting date columns...")

    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for c in date_cols:
        df[c] = pd.to_datetime(df[c])

    print("Creating target variable (delivery delay)...")

    df["delivery_delay"] = (
        df["order_delivered_customer_date"] >
        df["order_estimated_delivery_date"]
    ).astype(int)

    df = df.dropna(subset=[
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ])

    print("Handling missing numeric values...")

    num_cols = [
        "product_weight_g",
        "product_length_cm",
        "product_width_cm"
    ]

    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    print("Creating time features...")

    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour
    df["purchase_dayofweek"] = df["order_purchase_timestamp"].dt.dayofweek

    print("Creating delivery features...")

    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"] -
        df["order_purchase_timestamp"]
    ).dt.days

    df["order_total"] = df.groupby("order_id")["payment_value"].transform("sum")

    df["items_per_order"] = df.groupby("order_id")["order_item_id"].transform("count")

    df["approval_delay_hours"] = (
        df["order_approved_at"] -
        df["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600

    print("Selecting ML features...")

    features = [
        "price",
        "freight_value",
        "product_weight_g",
        "product_length_cm",
        "product_width_cm",
        "purchase_hour",
        "purchase_dayofweek",
        "estimated_delivery_days",
        "payment_installments",
        "approval_delay_hours",
        "order_total",
        "items_per_order"
    ]

    target = "delivery_delay"

    df_model = df[features + [target]]

    print("Cleaning dataset...")

    df_model = df_model.drop_duplicates()
    df_model = df_model[df_model["price"] > 0]
    df_model = df_model[df_model["freight_value"] >= 0]
    df_model = df_model.dropna()

    print("Final dataset shape:", df_model.shape)

    print("Saving processed dataset...")

    df_model.to_csv(
        "data/processed/esales_clean.csv",
        index=False
    )

    print("Data preprocessing completed!")
    print("Saved to: data/processed/esales_clean.csv")


if __name__ == "__main__":
    preprocess_data()