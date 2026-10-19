"""Tesis-il ve il-il mesafe matrislerini üretir.

Girdi (aynı klasörde): il_koordinatlari.csv, tesisler.csv
Çıktı: mesafe_tesis_il_km.csv (tesis x il), mesafe_il_il_km.csv (il x il)

Yöntem: kuş uçuşu (haversine) mesafe x KARAYOLU_KATSAYISI.
Aynı il içi çok kısa mesafelerin sıfıra düşmemesi için alt sınır uygulanır.
"""
import numpy as np
import pandas as pd

KARAYOLU_KATSAYISI = 1.3   # VARSAYIM: karayolu mesafesi ~ kuş uçuşu x 1.3
ALT_SINIR_KM = 20          # VARSAYIM: en kısa tesis-il / il-il mesafesi (km)
R = 6371.0088              # Dünya yarıçapı (km)


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = (np.sin((lat2 - lat1) / 2) ** 2
         + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)
    return 2 * R * np.arcsin(np.sqrt(a))


def mesafe_matrisi(lat_a, lon_a, lat_b, lon_b):
    d = haversine(lat_a[:, None], lon_a[:, None], lat_b[None, :], lon_b[None, :])
    return np.maximum(d * KARAYOLU_KATSAYISI, ALT_SINIR_KM)


iller = pd.read_csv("il_koordinatlari.csv", encoding="utf-8-sig")
tesis = pd.read_csv("tesisler.csv", encoding="utf-8-sig")

lat_i, lon_i = iller["enlem"].to_numpy(), iller["boylam"].to_numpy()

# tesis x il
m_ti = mesafe_matrisi(tesis["enlem"].to_numpy(), tesis["boylam"].to_numpy(), lat_i, lon_i)
pd.DataFrame(m_ti.round(1), index=tesis["tesis"], columns=iller["il"]).to_csv(
    "mesafe_tesis_il_km.csv", encoding="utf-8-sig")

# il x il (aday lokasyonlar için)
m_ii = mesafe_matrisi(lat_i, lon_i, lat_i, lon_i)
np.fill_diagonal(m_ii, 0.0)
pd.DataFrame(m_ii.round(1), index=iller["il"], columns=iller["il"]).to_csv(
    "mesafe_il_il_km.csv", encoding="utf-8-sig")

print("tamam:", m_ti.shape, m_ii.shape)
