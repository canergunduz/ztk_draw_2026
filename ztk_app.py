import streamlit as st
import random
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="Kura Simülatörü", page_icon="🏆", layout="wide")

# Takımlar
seeded = ["Galatasaray", "Samsunspor", "Konyaspor", "Beşiktaş"]
unseeded = ["Trabzonspor", "Alanyaspor", "Gençlerbirliği", "Fenerbahçe"]

# Session State (Oturum Hafızası) Başlatma
if 'draw_count' not in st.session_state:
    st.session_state.draw_count = 0

if 'history' not in st.session_state:
    # Seri başı takımların her bir seri başı olmayan takımla eşleşme sayısını tutan sözlük
    st.session_state.history = {s: {u: 0 for u in unseeded} for s in seeded}

if 'last_draw' not in st.session_state:
    st.session_state.last_draw = []

# Kura Çekme Fonksiyonu
def draw_lots():
    current_unseeded = unseeded.copy()
    
    while True:
        random.shuffle(current_unseeded)
        pairs = list(zip(seeded, current_unseeded))
        
        # Kısıtlamaları kontrol et
        if ("Galatasaray", "Alanyaspor") in pairs or ("Beşiktaş", "Fenerbahçe") in pairs:
            continue # Kısıtlama ihlal edildi, tekrar karıştır
        
        break # Geçerli kura bulundu, döngüden çık
        
    # Geçerli kurayı hafızaya kaydet
    st.session_state.last_draw = pairs
    st.session_state.draw_count += 1
    
    for s, u in pairs:
        st.session_state.history[s][u] += 1

# Hafızayı Sıfırlama Fonksiyonu
def reset_history():
    st.session_state.draw_count = 0
    st.session_state.history = {s: {u: 0 for u in unseeded} for s in seeded}
    st.session_state.last_draw = []

# --- ARAYÜZ ---
st.title("🏆 Türkiye Kupası Çeyrek Final Kura Simülatörü")
st.markdown("Seri başı ve seri başı olmayan takımlar arasındaki eşleşmeleri simüle edin. **Galatasaray-Alanyaspor** ve **Beşiktaş-Fenerbahçe** eşleşemez.")

# Butonlar (3 Kolon halinde güncelledik)
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🎲 1 Kura Çek", use_container_width=True):
        draw_lots()
        
with col_btn2:
    if st.button("🚀 100 Kez Simüle Et", use_container_width=True):
        # draw_lots fonksiyonunu 100 kere çalıştırıyoruz
        for _ in range(100):
            draw_lots()
            
with col_btn3:
    if st.button("🗑️ İstatistikleri Sıfırla", use_container_width=True):
        reset_history()

st.divider()

# Sonuç Ekranı (İki Kolon: Son Kura ve İstatistikler)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Son Kura Sonucu")
    if st.session_state.last_draw:
        for s, u in st.session_state.last_draw:
            st.success(f"**{s}** ⚔️ **{u}**")
    else:
        st.info("Henüz kura çekilmedi.")

with col2:
    st.subheader(f"📊 Eşleşme İstatistikleri (Toplam Kura: {st.session_state.draw_count})")
    
    if st.session_state.draw_count > 0:
        # Veriyi Pandas DataFrame'e çevirip yüzde hesabı yapalım
        df = pd.DataFrame(st.session_state.history).T # Satırlar seri başı olsun diye devriğini (.T) alıyoruz
        
        # Yüzdelik dilime çevirme (% formatı)
        df_pct = (df / st.session_state.draw_count) * 100
        
        # Ekranda güzel görünmesi için formatlama
        st.dataframe(
            df_pct.style.format("{:.1f}%").background_gradient(cmap="Blues"),
            use_container_width=True
        )
    else:
         st.info("İstatistikleri görmek için kura çekiniz.")