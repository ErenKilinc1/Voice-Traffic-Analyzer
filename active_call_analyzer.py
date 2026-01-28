from netmiko import ConnectHandler
import re
from datetime import datetime

# Cihaz Bilgileri
cisco_cube = {
    'device_type': 'cisco_ios',
    'host': '10.5.95.4',
    'username': 'abdullah.kilinc',
    'password': 'dynmox-X',
}

def voice_traffic_analyzer():
    try:
        call_count = 0

        with ConnectHandler(**cisco_cube) as net_connect:

            output_compact = net_connect.send_command("show call active voice compact")
            output_brief = net_connect.send_command("show call active voice brief")

            call_info_map = {}
            for line in output_brief.splitlines():
                if "99" in line:
                    cid_match = re.search(r'(99\d{6})', line)
                    if cid_match:
                        cid = int(cid_match.group(1))

                        time_match = re.search(r'(\d{2}:\d{2}:\d{2})', line)
                        time_str = time_match.group(1) if time_match else "00:00:00"

                        status = "CONNECTING" if "+-1" in line or "connecting" in line.lower() else "ACTIVE"

                        call_info_map[cid] = {
                            'time': time_str,
                            'status': status
                        }

            print(f"\n--- {cisco_cube['host']} Gerçek Zamanlı Aktif Çağrı Raporu ---")
            header = f"{'TARİH / SAAT':<20} | {'DURUM':<12} | {'ARAYAN (DAHİLİ)':<20} | {'ARANAN CEP'}"
            print(header)
            print("-" * len(header))

            call_data = {}
            lines = output_compact.splitlines()

            for line in lines:
                parts = line.split()
                if len(parts) > 6 and parts[0].startswith('99'):
                    cid = int(parts[0])
                    peer_match = re.search(r'P(\d+)', line)
                    peer_no = peer_match.group(1) if peer_match else "N/A"

                    # Brief haritasından bilgileri al
                    info = call_info_map.get(cid, {'time': "00:00:00", 'status': "ACTIVE"})

                    call_data[cid] = {
                        'number': peer_no,
                        'time': info['time'],
                        'status': info['status']
                    }

            # 3. Akıllı Eşleştirme (Atlama yapan ID'leri yakalayan mantık)
            processed = set()
            sorted_ids = sorted(call_data.keys())
            date_today = datetime.now().strftime("%d.%m.%Y")

            for i in range(len(sorted_ids)):
                cid = sorted_ids[i]
                if cid in processed:
                    continue

                # Sadece n+1 değil, bir sonraki uygun ID'ye bak (atlamaları tolere et)
                if i + 1 < len(sorted_ids):
                    next_id = sorted_ids[i + 1]

                    # Eğer iki bacak arasındaki ID farkı makul ise (max 5) eşleştir
                    if next_id - cid <= 5:
                        c1 = call_data[cid]
                        c2 = call_data[next_id]

                        # Cep numarası filtresi
                        is_c1_mobile = c1['number'].startswith(('05', '5')) and len(c1['number']) >= 10
                        is_c2_mobile = c2['number'].startswith(('05', '5')) and len(c2['number']) >= 10

                        if is_c1_mobile or is_c2_mobile:
                            # Hangi tarafın cep hangisinin dahili olduğunu ayır
                            if is_c2_mobile:
                                caller = c1['number']
                                callee = c2['number']
                            else:
                                caller = c2['number']
                                callee = c1['number']

                            router_time = c1['time']
                            full_timestamp = f"{date_today} {router_time}"

                            # İki bacaktan biri bile CONNECTING ise durum CONNECTING yansır
                            final_status = "CONNECTING" if c1['status'] == "CONNECTING" or c2[
                                'status'] == "CONNECTING" else "ACTIVE"

                            print(f"{full_timestamp:<20} | {final_status:<12} | {caller:<20} | {callee}")
                            call_count += 1

                        processed.add(cid)
                        processed.add(next_id)

            # Rapor Sonu Özeti
            print("-" * len(header))
            print(f"TOPLAM AKTİF CEP ARAMASI: {call_count}")
            print("-" * len(header))

    except Exception as e:
        print(f"Hata oluştu: {e}")


if __name__ == "__main__":
    voice_traffic_analyzer()