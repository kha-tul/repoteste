import streamlit as st

def cards(title, total_sessions):
    # Displaying the metric in a card-like style with an icon and a red horizontal line
    st.markdown(
        """
        <style>
        .metric-card {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 8px 12px rgba(0,0,0,0.3);
            text-align: center;
            font-size: 14px;
            position: relative;
            overflow: hidden;
            height: 50%;
            width: 98%;
        }
        .metric-card::before {
            content: '';
            position: absolute;
            height: 100%;
            width: 5px;
            background-color: red;
            top: 0;
            left: 0;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="metric-card">
            <div>{title}</div>
            <div class="metric-value">{total_sessions}</div>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )