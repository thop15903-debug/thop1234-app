import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Cấu hình trang Streamlit
st.set_page_config(page_title="Ứng dụng Streamlit Mẫu", layout="wide")

# Tiêu đề ứng dụng
st.title("📊 Báo Cáo Phân Tích Dữ Liệu Tương Tác")

# --- SIDEBAR: CHỌN THAM SỐ ---
st.sidebar.header("⚙️ Cài đặt Tham số")
khu_vuc = st.sidebar.multiselect(
    "Chọn Khu Vực:",
    options=["Miền Bắc", "Miền Trung", "Miền Nam"],
    default=["Miền Bắc", "Miền Trung", "Miền Nam"]
)

so_luong_mau = st.sidebar.slider("Số lượng bản ghi:", min_value=10, max_value=200, value=50)

# --- TẠO DỮ LIỆU MẪU ---
np.random.seed(42)
dates = pd.date_range(start="2026-01-01", periods=so_luong_mau)
data = pd.DataFrame({
    "Ngày": dates,
    "Khu Vực": np.random.choice(["Miền Bắc", "Miền Trung", "Miền Nam"], size=so_luong_mau),
    "Doanh Thu": np.random.randint(100, 1000, size=so_luong_mau),
    "Lợi Nhuận": np.random.randint(20, 300, size=so_luong_mau)
})

# Lọc dữ liệu theo Sidebar
filtered_data = data[data["Khu Vực"].isin(khu_vuc)]

# --- HIỂN THỊ CHỈ SỐ TỔNG QUAN ---
col1, col2, col3 = st.columns(3)
col1.metric("Tổng Doanh Thu", f"{filtered_data['Doanh Thu'].sum():,} VNĐ")
col2.metric("Tổng Lợi Nhuận", f"{filtered_data['Lợi Nhuận'].sum():,} VNĐ")
col3.metric("Số Lượng Giao Dịch", len(filtered_data))

# --- BIỂU ĐỒ DỮ LIỆU ---
st.subheader("📈 Biểu đồ Doanh thu theo Thời gian")
fig = px.line(filtered_data, x="Ngày", y="Doanh Thu", color="Khu Vực", title="Xu hướng Doanh Thu")
st.plotly_chart(fig, use_container_width=True)

# --- BẢNG DỮ LIỆU & NÚT XUẤT BÁO CÁO ---
st.subheader("📋 Bảng Dữ Liệu Chi Tiết")
st.dataframe(filtered_data, use_container_width=True)

# Nút xuất file CSV
csv_data = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Tải Báo Cáo (CSV)",
    data=csv_data,
    file_name="bao_cao_doanh_thu.csv",
    mime="text/csv"
)
