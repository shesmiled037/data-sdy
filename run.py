import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# Load .env
load_dotenv()
WP_API_URL = os.getenv("WP_API_URL")
WP_USER = os.getenv("WP_USER")
WP_PASS = os.getenv("WP_PASS")

def ambil_tabel_sdy():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = "http://206.189.86.19/data-keluaran-sydney/"

            # Tambahkan retry maksimal 3x
            for attempt in range(3):
                try:
                    print(f"🌐 Akses ke {url} (percobaan {attempt + 1})")
                    page.goto(url, timeout=90000, wait_until="load")
                    page.wait_for_selector("table.baru", timeout=10000)
                    break  # sukses, keluar dari loop
                except Exception as e:
                    print(f"🔁 Gagal buka halaman (percobaan {attempt + 1}): {e}")
                    if attempt == 2:
                        raise  # kalau 3x gagal, lempar error

            html = page.content()
            browser.close()

            soup = BeautifulSoup(html, "html.parser")
            tabel_list = soup.find_all("table", class_="baru")

            if not tabel_list:
                print("❌ Tidak ada tabel ditemukan.")
                return None

            hasil = []

            for table in tabel_list:
                heading = table.find_previous(["h2", "h3", "h4"])
                if heading:
                    hasil.append(f"<{heading.name}>{heading.text.strip()}</{heading.name}>")

                # Ubah warna lama ke warna baru
                table_html = str(table).replace("#68a225", "#29bfe5").replace("#265c00", "#30257d")
                hasil.append(table_html)

            print(f"✅ Ditemukan {len(tabel_list)} tabel + judul.")
            return "\n".join(hasil)

    except Exception as e:
        print(f"❌ Error ambil data: {e}")
        return None


def gabungkan_ke_template(tabel_html):
    try:
        bagian_atas = """
<article id="post-4775" class="single-view post-4775 post type-post status-publish format-standard hentry category-data-sydney tag-data-sdy tag-data-sydney tag-keluaran-sydney tag-paito-sidney tag-pengeluaran-sydney" itemprop="blogPost" itemscope="" itemtype="http://schema.org/BlogPosting">
<header class="entry-header cf">
<h1 class="entry-title" itemprop="headline"><a href="./">Data Keluaran Sydney 2025</a></h1>
</header>
<div class="entry-byline cf">	
</div>
<div class="entry-content cf" itemprop="text">
<p><strong>Data Keluaran Sydney 2025, Data Sydney 2024, Angka Pengeluaran Sdy terlengkap</strong></p>
<p>Rekap <a href="./"><span style="text-decoration: underline;"><strong>p</strong><strong>engeluaran togel sydney</strong></span></a> hari ini, angka keluaran togel sdy tercepat, hasil result sidney 1st, tabel nomor angka keluar sydney terbaru, data sydney 2025 lengkap yang bersumber dari situs resminya.</p>
<p><strong>Data Sydney</strong> menayangkan nomor pengeluaran sydney 2018 sampai 2025, rekap pengeluaran sdy hari ini, paito sydneypools terlengkap dan terbaru. Dengan menggunakan data togel sdy ini mempermudah dalam pencarian angka tarikan paito.</p>
<div id="attachment_4528" style="width: 854px" class="wp-caption aligncenter"><p id="caption-attachment-4528" class="wp-caption-text">Data Keluaran Sydney 2025, Data sidney Pools terbaru</p></div>
<table>
<tbody>
<tr>
<td>Keluaran togel sydney hari ini keluar pada pukul 13.50 WIB, Data togel sdy ini di update setelah hasil result sidney 1st prize terakhir tampil.</td>
</tr>
</tbody>
</table>
"""

        bagian_bawah = """
<p><strong>Data Pengeluaran sdy</strong> terbaru, Hasil keluaran atau Result Sydney tercepat akan langsung keluar di halaman ini dengan cepat tepat dan akurat. Data <span style="text-decoration: underline;"><a href="./"><strong>keluaran sydney 2025</strong></a></span> yang memberikan data pengeluaran togel sydney 2018 sampai dengan sekarang.</p>
<blockquote><p>Kamu juga mungkin membutuhkan <a href="https://result.gbg-coc.org/data-pengeluaran-hongkong/"><span style="text-decoration: underline;"><strong>Data Keluaran Hongkong 2025</strong></span></a></p></blockquote>
<p>Hasil rekap togel sidney kami tampilkan Data angka keluaran sydney 2024, yang bisa anda pergunakan untuk melihat <a href="http://95.111.203.17/"><span style="text-decoration: underline;"><strong>Data sdy</strong></span></a> di tahun 2025 ini dan merumus angka jitu setiap harinya.</p>
<h3>Data Sdy Pools 2025</h3>
<p>Angka Keluar togel SDY / sydney hari ini pukul 13.50 WIB setiap hari, Untuk pemutaran bola jatuh sdy live draw di mulai pada jam 13.40 sampai dengan selesai prize 1 st.</p>
<p>Sekian informasi <span style="text-decoration: underline;"><strong>Data Keluaran sydney 2025</strong></span> yang kami tampilkan di atas semoga dapat bermanfaat serta bisa berguna buat sobat togeler semua. Dalam mempermudah dalam mencari angka tarikan paito terbaik butuh usaha yang baik juga. Pengeluaran sydney tercepat, <em><strong>Data sydney 2025</strong></em>, hasil result togel sydney hari ini terlengkap dan akurat.</p>
<h4>Incoming search terms:</h4><ul><li>data sdy 2023</li><li>data sydney</li><li>pengeluaran sidney</li><li>pengeluaran cambodia</li><li>togel sydney</li><li>Data sdy 2024</li><li>Kluaran makau 2023</li><li>Data sydney 2023</li><li>https://datamacau help/data-keluaran-sydney/</li><li>data sdy 2022</li></ul>
</div>
<footer class="entry-footer cf">	
</footer>
</article>
"""

        hasil_html = bagian_atas + tabel_html + bagian_bawah

        with open("result_sdy.html", "w", encoding="utf-8") as f:
            f.write(hasil_html)

        print("✅ result_sdy.html berhasil dibuat.")
        return hasil_html
    except Exception as e:
        print(f"❌ Error saat gabung template: {e}")
        return None

def post_ke_wordpress(html_content):
    if not WP_API_URL or not WP_USER or not WP_PASS:
        print("❌ Data .env tidak lengkap.")
        return

    headers = {"Content-Type": "application/json"}
    data = {
        "title": "",
        "content": html_content,
        "status": "publish"
    }

    try:
        r = requests.post(WP_API_URL, json=data, auth=(WP_USER, WP_PASS), headers=headers)
        if r.status_code in [200, 201]:
            print("✅ Berhasil posting ke WordPress.")
            print(f"🔗 Link: {r.json().get('link')}")
        else:
            print(f"❌ Gagal post: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Error saat post ke WordPress: {e}")

if __name__ == "__main__":
    tabel_html = ambil_tabel_sdy()
    if tabel_html:
        full_html = gabungkan_ke_template(tabel_html)
        if full_html:
            post_ke_wordpress(full_html)
