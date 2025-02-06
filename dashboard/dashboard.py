import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
file_path = "merged_data.csv"
df = pd.read_csv(file_path)

# Konversi kolom tanggal
df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping bulan
bulan_mapping = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
}
df['bulan'] = df['mnth'].map(bulan_mapping)

# Judul Dashboard
st.title("Dashboard Peminjaman Sepeda")

# Sidebar untuk filter
time_filter = st.sidebar.selectbox("Pilih Filter Waktu", ["Harian", "Bulanan", "Jam"])

# Analisis peminjaman sepeda di pagi hari
st.sidebar.markdown("# Analisis peminjaman sepeda")

if time_filter == "Harian":
    # 1. VISUALISASI PENGGUNAAN SEPEDA PER HARI
    st.subheader("Tren Penggunaan Sepeda per Hari")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=df["dteday"], y=df["cnt_day"], color="purple", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Peminjaman Sepeda")
    ax.set_title("Tren Penggunaan Sepeda per Hari")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    # Analisis peminjaman sepeda di pagi hari
    st.subheader("Peminjaman Sepeda di Pagi Hari")
    morning_rentals = df[(df["hr"] >= 6) & (df["hr"] <= 9)]
    weekend_morning_avg = morning_rentals[morning_rentals["is_weekend"] == 1]["cnt_hour"].mean()
    weekday_morning_avg = morning_rentals[morning_rentals["is_weekend"] == 0]["cnt_hour"].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=["Hari Biasa", "Akhir Pekan"], y=[weekday_morning_avg, weekend_morning_avg], palette=["green", "yellow"], ax=ax)
    ax.set_ylabel("Rata-rata Peminjaman Sepeda di Pagi Hari")
    ax.set_title("Perbandingan Peminjaman Sepeda di Pagi Hari (Weekday vs Weekend)")
    st.pyplot(fig)

elif time_filter == "Bulanan":
    st.subheader("Peminjaman Sepeda per Bulan")
    monthly_rentals = df.groupby('bulan')["cnt_day"].sum().reset_index()
    order_bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    monthly_rentals['bulan'] = pd.Categorical(monthly_rentals['bulan'], categories=order_bulan, ordered=True)
    monthly_rentals = monthly_rentals.sort_values('bulan')
    fig, ax = plt.subplots()
    sns.barplot(data=monthly_rentals, x='bulan', y='cnt_day', palette='coolwarm', ax=ax)
    ax.set_title("Tren Peminjaman Sepeda per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_xticklabels(order_bulan, rotation=45)
    st.pyplot(fig)

elif time_filter == "Jam":
    st.subheader("Peminjaman Sepeda per Jam dalam Sehari")
    hourly_counts = df.groupby("hr")["cnt_hour"].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette="Blues_r", ax=ax)
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Peminjaman Sepeda")
    ax.set_title("Rata-rata Peminjaman Sepeda per Jam dalam Sehari")
    ax.set_xticks(range(0, 24))
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)
