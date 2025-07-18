# -*- coding: utf-8 -*-
"""CNN_Salinan.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w_VL3_RGfW53KzUS6T36RnMn9BeZ1sxC

# Deploy **Streamlit**
"""

import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

# Styling modern pakai CSS
# Tambahkan custom CSS dengan tema biru klinis kalem dan bentuk dekoratif
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    /* Terapkan ke seluruh halaman */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(to bottom, #eaf4fc, #ffffff);
        color: #003366;
        margin: 0;
        padding: 0;
    }

    /* Container utama */
    .block-container {
        padding: 3rem 6rem;
        background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
        background-repeat: repeat;
        background-size: 400px;
        min-height: 100vh;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem;
        }
    }

    /* Judul dan paragraf */
    h1 {
        color: #005b96;
        text-align: center;
        font-size: 2.5rem;
    }

    p {
        text-align: center;
        font-size: 1.1rem;
    }

    /* Uploader */
    .stFileUploader {
        border: 2px dashed #89c2d9;
        background-color: #f0faff;
        padding: 1em;
        border-radius: 10px;
    }

    /* Tombol */
    .stButton>button {
        background-color: #005b96;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        border: none;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #004b80;
    }
    </style>
""", unsafe_allow_html=True)

# Judul aplikasi
st.set_page_config(page_title="Klasifikasi Cedera Ringan")
st.markdown("<h1>Klasifikasi Cedera Ringan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload gambar cedera untuk mengetahui jenisnya (lecet, memar, atau bengkak)</p>", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("mobilenet_cnn_model.h5")  # ganti path sesuai tempat file .h5 disimpan
    return model

model = load_model()

# Label sesuai urutan folder training
label_map = ['bengkak', 'lecet', 'memar']  # URUTANNYA HARUS BENAR sesuai train_ds.class_names

# Saran penanganan berdasarkan jenis luka
def saran_penanganan(label):
    if label == 'lecet':
        return (
            "🩹 Saran: Bersihkan luka dengan air bersih dan sabun, keringkan, lalu oleskan antiseptik ringan. "
            "Tutup dengan perban steril jika perlu. Hindari menggaruk luka. "
            "Jika luka membengkak atau bernanah, atau tidak sembuh setelah beberapa hari, segera konsultasikan ke dokter."
        )
    elif label == 'memar':
        return (
            "🧊 Saran: Kompres area memar dengan es selama 10–15 menit tiap beberapa jam di hari pertama. "
            "Jaga agar bagian tersebut tidak terbentur lagi. "
            "Jika memar membesar atau sangat nyeri, atau tidak kunjung membaik, segera periksakan diri ke dokter."
        )
    elif label == 'bengkak':
        return (
            "🧊 Saran: Istirahatkan area yang bengkak, kompres dengan es, dan angkat bagian tubuh yang bengkak lebih tinggi dari jantung. "
            "Jika bengkak tidak kunjung reda dalam 1–2 hari atau semakin parah, segera periksakan diri ke dokter."
        )
    else:
        return "Saran tidak tersedia untuk jenis luka ini."

# Upload gambar
uploaded_file = st.file_uploader("Upload gambar cedera (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Baca dan tampilkan gambar
    img = Image.open(uploaded_file)
    st.image(img, caption='Gambar yang diupload', use_container_width=True)

    # Preprocess gambar
    img = img.resize((224, 224))  # harus sama seperti saat training
    img_array = np.array(img) / 255.0
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]  # buang alpha channel kalau ada
    img_array = np.expand_dims(img_array, axis=0)

    # Prediksi
    prediction = model.predict(img_array)
    pred_index = np.argmax(prediction[0])
    confidence = np.max(prediction[0]) * 100
    label = label_map[pred_index]

    # Tampilkan hasil prediksi
    st.success(f"Hasil Prediksi: {label.capitalize()}")
    
    # Tampilkan saran berdasarkan hasil prediksi
    st.info(saran_penanganan(label))
