# 🚀 E-Sales AI: Real-Time Delivery Intelligence System
     An AI-powered dashboard for predicting delivery delays and analyzing e-commerce logistics in real time.

## 📌 Introduction
    Modern e-commerce platforms operate under tight delivery constraints where delays directly impact customer satisfaction, retention, and operational costs. Anticipating such delays before they occur enables proactive decision-making in logistics and supply chain management.
    The E-Sales Project is a machine learning–driven system designed to predict delivery delays and provide real-time analytical insights through an interactive dashboard. It combines predictive modeling, feature engineering, and live visualization to simulate a production-grade decision-support tool.

## 🎯 Objectives
    The primary goals of this project are:
      -Predict the probability of delivery delays using structured order data
      -Provide a real-time monitoring system for predictions
      -Enable interactive exploration of delivery patterns and risk factors
      -Demonstrate an end-to-end ML pipeline from data to deployment
      
## 🧠 System Architecture
     The system is composed of three core components:

    1. Data Processing Layer
        -Cleaned and structured e-commerce dataset
        -Feature engineering to capture logistics complexity
        -Derived features such as:
             (i)   Freight-to-price ratio
             (ii)  Approval delay indicators
             (iii) Order-level aggregations
     2. Machine Learning Layer
         Supervised classification model trained to predict delivery delays
         Outputs a probability score representing risk
         Uses engineered features capturing:
                (i) Product characteristics
                (ii) Order behavior
                (iii) Payment and approval delays
                (iv) Temporal signals
     3. Visualization & Interaction Layer
          Built using Streamlit
          Provides:
            -Real-time predictions
            -Charts
            -Interactive filters and analytics
            -Session-based logging system

## ⚙️ Key Features
    1. AI- Based Prediction Delay:
              Predicts delivery delay probability using 14 input features
              Provides interpretable risk output (High / Low)
              Designed for real-time inference
    2. Real-Time Prediction Logging
              Every prediction is stored in session state
              Enables continuous monitoring of system behavior
              Supports dynamic recalculation of metrics
    3. Analytics Dashboard
          Includes:
           -Risk distribution visualization
           -Time-based risk trends
           -Aggregate statistics (mean risk, counts)

## 📈 Feature Engineering
      The model leverages 14 carefully designed features:
      Raw Features
          price
          freight_value
          product_weight_g
          product_length_cm
          product_width_cm
          purchase_hour
          purchase_dayofweek
          estimated_delivery_days
          payment_installments
          approval_delay_hours
          order_total
          items_per_order
      Engineered Features
         freight_price_ratio → captures shipping cost intensity
         slow_approval → binary indicator for delayed payment approval

      These features collectively encode logistical complexity, temporal behavior, and operational inefficiencies.

## Model details:
      - Model Type: Ensemble model of Random forest and XGBoost
      - Task: Binary Classification (delay/ no delay)
      - Risk Percentage
## Evaluation Metrics:
## 📊 Real-Time System Behaviour
       Unlike static dashboards, this system supports:
         - Immediate UI updates after each prediction
         - Dynamic chart re-rendering using session state
         - Continuous accumulation of prediction logs
    This mimics a live monitoring environment similar to production analytics systems.    
