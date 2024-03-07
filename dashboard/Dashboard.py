import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import streamlit as st

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('day_df_clean.csv')  
    data['dteday'] = pd.to_datetime(data['dteday'])  
    return data

data = load_data()

# Judul dashboard
st.title('Dashboard Penyewaan Sepeda')

# Tampilkan filter rentang waktu
min_date = data['dteday'].min()
max_date = data['dteday'].max()
default_date = min_date + (max_date - min_date) // 2
start_date = st.date_input('Pilih Tanggal Awal', default_date, min_date, max_date)
end_date = st.date_input('Pilih Tanggal Akhir', max_date, min_date, max_date)

# Konversi nilai dari date_input menjadi objek datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan rentang waktu
filtered_data = data[(data['dteday'] >= start_date) & (data['dteday'] <= end_date)]

# Tampilkan filter pemilihan musim (opsional)
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
selected_seasons = st.multiselect('Pilih Musim (Opsional)', seasons)

# Filter data berdasarkan musim yang dipilih (jika ada)
if selected_seasons:
    filtered_data = filtered_data[filtered_data['season'].isin(selected_seasons)]

# Tampilkan data yang difilter
st.write('Data Penyewaan Sepeda untuk Rentang Waktu', start_date, 'sampai', end_date)
st.write(filtered_data)

# Visualisasi sederhana
st.write('Grafik Jumlah Penyewaan Sepeda per Hari:')
daily_rentals = filtered_data.groupby('dteday')['cnt'].sum()
st.line_chart(daily_rentals)
