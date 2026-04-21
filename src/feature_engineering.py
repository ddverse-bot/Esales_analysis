import pandas as pd
import os


def feature_engineering():

    print("Starting feature engineering...")

    DATA_PATH = "data/processed/esales_clean.csv"

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded:", df.shape)

    # ---------------------------------------------------
    # Freight to price ratio
    # ---------------------------------------------------
    df["freight_price_ratio"] = df["freight_value"] / (df["price"] + 1)

    # ---------------------------------------------------
    #  Slow approval flag
    # ---------------------------------------------------
    df["slow_approval"] = (df["approval_delay_hours"] > 24).astype(int)

    # ---------------------------------------------------
    # State delay rate
    # (requires customer_state column)
    # ---------------------------------------------------
    if "customer_state" in df.columns:
        state_delay = df.groupby("customer_state")["delivery_delay"].mean()
        df["state_delay_rate"] = df["customer_state"].map(state_delay)

    # ---------------------------------------------------
    #  Category delay rate
    # (requires product_category column)
    # ---------------------------------------------------
    if "product_category_name_english" in df.columns:
        cat_delay = df.groupby("product_category_name_english")["delivery_delay"].mean()
        df["category_delay_rate"] = df["product_category_name_english"].map(cat_delay)

    # ---------------------------------------------------
    # Save dataset
    # ---------------------------------------------------
    df.to_csv(DATA_PATH, index=False)

    print("Feature engineering completed")

    new_features = [
        "state_delay_rate",
        "category_delay_rate",
        "freight_price_ratio",
        "slow_approval"
    ]

    print("\nNew Features Added:")
    print(new_features)

    print("\nUpdated Shape:", df.shape)


if __name__ == "__main__":
    feature_engineering()