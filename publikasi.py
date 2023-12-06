from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Fungsi untuk mengeklik tombol "Tampilkan Lainnya"
def click_show_more(driver):
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "gsc_bpf_more"))
        )
        show_more_button.click()
    except Exception as e:
        print("Tidak bisa menemukan tombol atau terjadi kesalahan:", str(e))

# Inisialisasi WebDriver (pastikan sudah mengunduh driver sesuai browser yang akan digunakan)
driver = webdriver.Chrome()  # Ganti dengan browser yang ingin kamu gunakan (Chrome, Firefox, dll.)

url = "https://scholar.google.co.id/citations?hl=id&user=_GaUEDgAAAAJ&view_op=list_works&sortby=pubdate"
driver.get(url)

# Melakukan beberapa kali klik "Tampilkan lainnya" untuk memuat semua data
for i in range(5):  # Ubah angka sesuai kebutuhan untuk memuat lebih banyak data
    click_show_more(driver)

# Mengambil HTML setelah semua data dimuat
page_source = driver.page_source

# Menutup WebDriver
driver.quit()

# Menggunakan BeautifulSoup untuk mengekstrak data penelitian
soup = BeautifulSoup(page_source, 'html.parser')

# Proses ekstraksi data penelitian yang diurutkan berdasarkan tahun
publication_details = soup.find_all("tr", {"class": "gsc_a_tr"})

# Menyiapkan teks output dengan pembatas antar tahun
output_text = "<ol>\n"
current_year = None

for pub in publication_details:
    title = pub.find("a", {"class": "gsc_a_at"}).text
    authors = pub.find("div", {"class": "gs_gray"}).text
    year = pub.find("span", {"class": "gsc_a_h"}).text

    link = pub.find("a", {"class": "gsc_a_at"})['href']
    full_link = f"https://scholar.google.com{link}"

    # Memeriksa apakah tahun publikasi telah berubah
    if year != current_year:
        # Jika tahun berbeda, tambahkan pembatas untuk tahun baru
        current_year = year
        output_text += f'  <li style="text-align:center;"><strong>Tahun {current_year}</strong></li>\n'

    publication_text = (
        f'<li style="text-align: justify;"><strong><a class="gsc_a_at" href="{full_link}" target="_blank" rel="noopener">{title}</a></strong>, ({authors}), {year}</li>\n'
    )
    output_text += publication_text

output_text += "</ol>"

# Simpan output ke dalam file .txt
with open("output_publications.txt", "w", encoding="utf-8") as file:
    file.write(output_text)

print("Data berhasil disimpan dalam file output_publications.txt")

