import json
import datetime as dt

class Kasir:
    def __init__(self):
        self.menu = {}
        file_path = 'menu.json'

        try:
            with open(file_path, 'r') as file:
                # Parse string JSON ke dictionary
                self.menu = json.load(file)
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
            
    def show_menu(self):
        '''Menampilkan menu makanan dan minuman'''
        print()
        print('|'+'='*39+'|')
        print(f"|{'DAFTAR MENU':^39}|")
        print('|'+'='*39+'|')
        print(f"|{'Kode':^7} | {'Menu':^15} | {'Harga':^11}|")
        print('|'+'='*39+'|')
        for item, info in self.menu.items():
            print(f"|{info['kode']:^7} | {item:<15} | Rp{info['harga']:>9,d}|")
        print('|'+'='*39+'|')
        
    def take_order(self):
        '''Fungsi untuk mengambil pesanan dari pelanggan'''
        code = dt.datetime.now().strftime('%Y%m%d%H%M%S')
        name = input('Nama Pelanggan: ')
        orders = []
        total_harga = 0
        print('Masukkan kode menu dan porsi(Cth: 3, 2): ')
        print('(Pilih nomor 0 untuk selesai)')
        while True:
            try:
                order = input('Pesanan: ')
                if order.lower() == '0':
                    print(f"{'Total Harga':28}: Rp {total_harga:,d}")
                    while True:
                        bayar = input(f"{'Masukkan jumlah uang bayar':28}: Rp ")
                        if int(bayar) >= total_harga:
                            break
                        else:
                            print('Uang bayar yang Anda masukkan kurang dari total harga')
                    break
                
                kode_pesanan, porsi = order.split(', ')
                if kode_pesanan in [info['kode'] for info in self.menu.values()]:
                    item_terpilih = next(item for item, info in self.menu.items() if info['kode'] == kode_pesanan)
                    harga_terpilih = self.menu[item_terpilih]['harga']
                    harga = harga_terpilih * int(porsi)
                    total_harga += harga
                    orders.append({'item':item_terpilih, 'porsi':int(porsi), 'harga': harga})
                    print(f'Anda memesan {item_terpilih} x {porsi} dengan harga Rp {harga:,d}.')
                else:
                    print('Kode menu tidak valid.')
            except:
                print('Format input salah')
        return code, name, orders, total_harga, bayar

    def save_order(self, kode_transaksi, nama_pelanggan, orders, total_harga):
        '''Fungsi untuk menyimpan pesanan ke dalam file'''
        order_details = {
            'Kode Transaksi': kode_transaksi,
            'Nama Pelanggan': nama_pelanggan,
            'orders': orders,
            'total_harga': total_harga
        }
        with open('pesanan.txt', 'a') as file:
            file.write(json.dumps(order_details)+'\n')

    def read_orders(self, pay):
        '''Fungsi untuk membaca dan menampilkan pesanan dari file'''
        bayar = int(pay)
        with open('pesanan.txt', 'r') as file:
            lines = file.readlines()
            baris_terakhir = lines[-1]
            order_details = json.loads(baris_terakhir)
            print()
            print('|'+'='*39+'|')
            print(f"|Kode Transaksi: {order_details['Kode Transaksi']:<23}|")
            print('|'+'='*39+'|')
            print(f"|Nama Pelanggan: {order_details['Nama Pelanggan']:<23}|")
            print('|'+'='*39+'|')
            print(f"|Tanggal: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<30}|")
            print('|'+'='*39+'|')
            print(f"|{'Detail Pesanan':^39}|")
            print('|'+'='*39+'|')
            print(f"|{'Menu':^15} | {'Porsi':^5} | {'Harga':^13}|")
            print('|'+'='*39+'|')
            for order in order_details['orders']:
                print(f"|{order['item']:<15} | {order['porsi']:^5} | Rp {order['harga']:>10,d}|")
                print('|'+'='*39+'|')
            print(f"|Total Harga {'Rp':>16} {order_details['total_harga']:>10,d}|")
            print('|'+'-'*39+'|')
            print(f"|Uang Bayar {'Rp':>17} {bayar:>10,d}|")
            print('|'+'-'*39+'|')
            print(f"|Kembalian {'Rp':>18} {bayar - order_details['total_harga']:>10,d}|")
            print('|'+'='*39+'|')
            print(f"|{'Terima Kasih':^39}|")
            print('|'+'='*39+'|')

# Membuat instance dari kelas Kasir
kasir = Kasir()

# Penggunaan fungsi
kasir.show_menu()
kode_transaksi, nama_pelanggan, orders, total_harga, bayar = kasir.take_order()
kasir.save_order(kode_transaksi, nama_pelanggan, orders, total_harga)
kasir.read_orders(bayar)
