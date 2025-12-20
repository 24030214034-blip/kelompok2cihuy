import math
import time
import pandas as pd

# ------------------- LINEAR SEARCH -------------------
def LinearSearchFull(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return None

# ------------------- LINEAR SEARCH (untuk Jump Search) -------------------
def LinearSearch(arr, x, loc):
    for i in range(len(arr)):
        if arr[i] == x:
            return i + loc
    return None

# ------------------- JUMP SEARCH -------------------
def JumpSearch(arr, x):
    n = len(arr)
    m = int(math.sqrt(n))
    if m == 0:
        m = 1

    i = 0
    while i < n and arr[min(i + m - 1, n - 1)] < x:
        i += m

    if i >= n:
        return None

    B = arr[i:min(i + m, n)]
    return LinearSearch(B, x, i)

# ------------------- BINARY SEARCH -------------------
def BinarySearch(arr, x):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return None

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
    print("==============================================")
    print(f" {row['BRAND'].upper()} - {row['SERIES'].upper()}")
    print("----------------------------------------------")
    print(f" Size  : {row['SIZE']}")
    print(f" Harga : Rp {row['PRICE']:,.0f}")
    print(f" Stok  : {row['STOK']}")
    print("==============================================\n")

    # MODE 1
def mode_search_key(df, keys):
        brand = input("Masukkan Brand  : ").lower().strip()
        series = input("Masukkan Series : ").lower().strip()
        size = float(input("Masukkan Size   : "))

        search_key = (brand, series, size)

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

        hasil_akhir = hasil_lin if hasil_bin is not None else hasil_bin if hasil_lin is not None else hasil_jump

        print("\n=========== HASIL PENCARIAN ===========")
        if hasil_akhir is not None:
            print_product_card(df, hasil_akhir)
        else:
            print("Data tidak ditemukan.")

        print("=========== WAKTU EKSEKUSI ===========")
        print(f"Linear Search : {waktu_lin} detik")
        print(f"Jump Search   : {waktu_jump} detik")
        print(f"Binary Search : {waktu_bin} detik")

        pass

    # MODE 2
def mode_search_size(df):
       size = float(input("Masukkan Size Sepatu : "))
       
       repeat = 10000
       start = time.perf_counter()
       for _ in range(repeat):
        hasil = df[df['SIZE'] == size].sort_values(by='PRICE')
       waktu = (time.perf_counter() - start) / repeat
       hasil = df[df['SIZE'] == size].sort_values(by='PRICE')

       print("\n=========== HASIL PENCARIAN (SIZE) ===========")

       if hasil.empty:
        print("Tidak ada sepatu dengan size tersebut.")
       else:
        for idx in hasil.index:
            print_product_card(df, idx)

       print("=========== WAKTU EKSEKUSI ===========")
       print(f"Filter + Sort : {waktu} detik")
    

    # MODE 3
def mode_search_price_range(df):
       print("\nPILIH RANGE HARGA")
       print("1. Rp 120.000  - Rp 500.000")
       print("2. Rp 500.001  - Rp 1.000.000")
       print("3. Rp 1.000.001 - Rp 2.700.000")

       pilihan = input("Pilih range (1/2/3): ")

       if pilihan == "1":
         min_harga, max_harga = 120_000, 500_000
       elif pilihan == "2":
         min_harga, max_harga = 500_001, 1_000_000
       elif pilihan == "3":
         min_harga, max_harga = 1_000_001, 2_700_000
       else:
         print("Pilihan range tidak valid.")
         return
    
       repeat = 10000
       start = time.perf_counter()
       for _ in range(repeat):
        hasil = df[(df['PRICE'] >= min_harga) & (df['PRICE'] <= max_harga)]\
                  .sort_values(by='PRICE')
       waktu = (time.perf_counter() - start) / repeat

       hasil = df[(df['PRICE'] >= min_harga) & (df['PRICE'] <= max_harga)]\
                .sort_values(by='PRICE')

       print("\n=========== HASIL PENCARIAN (RANGE HARGA) ===========")
       print(f"Range : Rp {min_harga:,.0f} - Rp {max_harga:,.0f}\n")

       if hasil.empty:
        print("Tidak ada sepatu pada range harga tersebut.")
       else:
        for idx in hasil.index:
            print_product_card(df, idx)

       print("=========== WAKTU EKSEKUSI ===========")
       print(f"Filter + Sort : {waktu} detik")

    # ------------------- MAIN PROGRAM -------------------
if __name__ == "__main__":
    df = load_excel("Data cepatu.xlsx")
    keys = df['Key'].tolist()

    print("\nPILIH MODE PENCARIAN")
    print("1. Brand + Series + Size")
    print("2. Size")
    print("3. Range Harga")

    mode = input("Pilih (1/2/3): ")

    if mode == "1":
       mode_search_key(df, keys)

    elif mode == "2":
       mode_search_size(df)

    elif mode == "3":
       mode_search_price_range(df)

    else:
        print("Pilihan tidak valid.")

    