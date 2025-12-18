import math #untuk menghitung akar n pd jump search
import time #untuk waktu 
import pandas as pd

# ------------------- LINEAR SEARCH -------------------
def LinearSearchFull(arr, x): # arr untuk daftar data, x data yg mau di cari
    n = len(arr) # panjang data dari arr
    for i in range(len(arr)): #looping dari data awal smpe akhir
        if arr[i] == x: #elemen = data yang dicari
            return i #mengembalikan posisi index saat data sdh ditemukan
    return None #data tidak ditemukan


# ------------------- LINEAR SEARCH (untuk Jump Search) -------------------
def LinearSearch(arr, x, loc): # loc = posisi awal block dlm array
    n = len(arr) #panjang array
    for i in range(n):
        if arr[i] == x: 
            return i + loc #indeks sebenarnya dalam array utama
    return None

# ------------------- JUMP SEARCH -------------------
def JumpSearch(arr, x): # arr = daftar data, x = data yg di cari
    n = len(arr) 
    m = int(math.sqrt(n)) #penghitungan banyak block
    if m == 0: #ketika data kosong
        m = 1 #block dibuat sebanyak 1

    i = 0 
    while i < n and arr[min(i + m - 1, n - 1)] < x: #mengecek elemen terakhir block , jika < maka lanjut ke block selanjutnya
        #print(f"Processing Block = {arr[i:min(i+m, n)]}")
        i += m #lanjut ke block berikutnya

    if i >= n: #data tidak ditemukan setelah melewati semua block
        return None

    B = arr[i : min(i + m, n)] #block dmn tempat data ditemukan
    #print(f"[Processing Block = {B}]")

    return LinearSearch(B, x, i)


# ------------------- BINARY SEARCH -------------------
def BinarySearch(arr, x): 
    low, high = 0, len(arr) - 1 #penentuan index terakhir

    while low <= high:
        mid = (low + high) // 2 #penentuan nilai tengah

        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    return None #data tdk ditemukan


# ------------------- LOAD EXCEL -------------------
def load_excel(namafile):
    df = pd.read_excel(namafile)

    df['BRAND'] = df['BRAND'].astype(str).str.lower().str.strip()
    df['SERIES'] = df['SERIES'].astype(str).str.lower().str.strip()
    df['SIZE'] = pd.to_numeric(df['SIZE'], errors='coerce')

    df = df.dropna(subset=['SIZE'])

    df['Key'] = list(zip(df['BRAND'], df['SERIES'], df['SIZE']))

    df = df.sort_values(by=['BRAND', 'SERIES', 'SIZE']).reset_index(drop=True)

    return df


# ------------------- PRODUCT CARD -------------------
def print_product_card(df, index):
    row = df.iloc[index]
    print("\n==============================================")
    print(f" {row['BRAND'].upper()} - {row['SERIES'].upper()}")
    print("----------------------------------------------")
    print(f" Size  : {row['SIZE']}")
    print(f" Harga : Rp {row['PRICE']:,.0f}")
    print(f" Stok  : {row['STOK']}")
    print("==============================================\n")


# ------------------- MAIN PROGRAM -------------------
if __name__ == "__main__":
    df = load_excel("Data cepatu.xlsx")
    keys = df['Key'].tolist()

    #print("Jumlah Data :", len(keys))

    brand = input("Masukkan Brand  : ").lower().strip()
    series = input("Masukkan Series : ").lower().strip()
    size = float(input("Masukkan Size   : "))

    search_key = (brand, series, size)

#------------------BENCHMARK WAKTU-----------------------
    repeat = 10000
    start = time.perf_counter()
    for _ in range(repeat):
        hasil_lin = LinearSearchFull(keys, search_key)
    waktu_lin = (time.perf_counter() - start) / repeat

    start = time.perf_counter()
    for _ in range(repeat):
        hasil_jump = JumpSearch(keys, search_key)
    waktu_jump = (time.perf_counter() - start) / repeat

    start = time.perf_counter()
    for _ in range(repeat): 
        hasil_bin = BinarySearch(keys, search_key)
    waktu_bin = (time.perf_counter() - start) / repeat


    hasil_akhir = hasil_lin or hasil_bin or hasil_jump

    print("\n=========== HASIL PENCARIAN ===========")

    if hasil_akhir is not None:
        print_product_card(df, hasil_akhir)
    else:
        print("Data tidak ditemukan.")

    print("=========== WAKTU EKSEKUSI ===========")
    print(f"Linear Search : {int(waktu_lin * 1_000_000)} mikrodetik")
    print(f"Jump Search   : {int(waktu_jump * 1_000_000)} mikrodetik")
    print(f"Binary Search : {int(waktu_bin * 1_000_000)} mikrodetik")