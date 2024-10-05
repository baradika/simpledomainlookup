import whois
import socket
import requests
from datetime import datetime

def domain_lookup(domain):
    try:
        result = whois.whois(domain)
        return result
    except Exception as e:
        print(f"Terjadi kesalahan saat mencari informasi domain: {e}")
        return None

def get_ip_address(domain):
    try:
        # Menghapus protokol dari domain jika ada
        if domain.startswith("http://"):
            domain = domain[7:]
        elif domain.startswith("https://"):
            domain = domain[8:]
        
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "Tidak dapat menemukan alamat IP."

def get_ip_location(ip_address):
    try:
        # Menggunakan API ip-api.com untuk mendapatkan lokasi IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        location_data = response.json()
        
        if location_data['status'] == 'success':
            return {
                "country": location_data.get("country", "Tidak diketahui"),
                "region": location_data.get("regionName", "Tidak diketahui"),
                "city": location_data.get("city", "Tidak diketahui"),
                "zip": location_data.get("zip", "Tidak diketahui"),
                "lat": location_data.get("lat", "Tidak diketahui"),
                "lon": location_data.get("lon", "Tidak diketahui")
            }
        else:
            return "Tidak dapat menemukan lokasi untuk IP ini."
    except Exception as e:
        return f"Kesalahan dalam mendapatkan lokasi: {e}"

def format_date(date):
    if isinstance(date, list):
        # Jika tanggal merupakan list, ambil tanggal pertama
        date = date[0] if date else None
    if date:
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")  # Format ISO
    return "Tidak ada informasi tanggal."

def display_info(info, ip_address, ip_location):
    if info:
        print("\nInformasi Domain:")
        print(f"Domain Name: {info.domain or 'Tidak ada'}")
        print(f"Registry Domain ID: {info.registry_domain_id or 'Tidak ada'}")
        print(f"Registrar WHOIS Server: {info.whois_server or 'Tidak ada'}")
        print(f"Registrar URL: {info.registrar_url or 'Tidak ada'}")
        print(f"Updated Date: {format_date(info.updated_date)}")
        print(f"Creation Date: {format_date(info.creation_date)}")
        print(f"Registrar Registration Expiration Date: {format_date(info.expiration_date)}")
        print(f"Registrar: {info.registrar or 'Tidak ada'}")
        print(f"Domain Status: {', '.join(info.status) if info.status else 'Tidak ada'}")
        print(f"Registrant Name: {info.name or 'Tidak ada'}")
        print(f"Registrant Organization: {info.org or 'Tidak ada'}")
        print(f"Registrant City: {info.city or 'Tidak ada'}")
        print(f"Registrant Country: {info.country or 'Tidak ada'}")
        print(f"Registrant Email: {', '.join(info.emails) if info.emails else 'Tidak ada'}")
        
        # Menampilkan informasi admin jika ada
        if info.admin:
            print(f"\nAdmin Name: {info.admin or 'Tidak ada'}")
            print(f"Admin Organization: {info.admin_org or 'Tidak ada'}")
        
        # Menampilkan informasi tech jika ada
        if info.tech:
            print(f"\nTech Name: {info.tech or 'Tidak ada'}")
            print(f"Tech Organization: {info.tech_org or 'Tidak ada'}")
        
        print(f"\nName Server: {', '.join(info.name_servers) if info.name_servers else 'Tidak ada'}")
        
        # Menampilkan informasi lokasi IP
        if isinstance(ip_location, dict):
            print(f"\nIP Address: {ip_address}")
            print(f"IP Location: {ip_location['city']}, {ip_location['region']}, {ip_location['country']} (ZIP: {ip_location['zip']})")
            print(f"Latitude: {ip_location['lat']}, Longitude: {ip_location['lon']}")
        else:
            print(ip_location)
    else:
        print("Informasi tidak tersedia.")

if __name__ == "__main__":
    while True:
        domain = input("Masukkan nama domain (atau ketik 'exit' untuk keluar): ")
        if domain.lower() == 'exit':
            print("Terima kasih telah menggunakan tools ini.")
            break
        # Memanggil fungsi untuk melakukan pencarian informasi domain dan IP address
        info = domain_lookup(domain)
        ip_address = get_ip_address(domain)
        ip_location = get_ip_location(ip_address)
        display_info(info, ip_address, ip_location)
