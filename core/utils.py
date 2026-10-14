import time
import threading
import multiprocessing

class AttackStats:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.packet_count = 0
        self.rps_samples = []
        self.max_rps = 0
        self.min_rps = float('inf')
        self.lock = threading.Lock()
        self.rps_window = []  # Moving average window
        self.window_size = 5  # Keep last 5 RPS values

    def start(self):
        self.start_time = time.time()
        self.rps_samples = []
        self.max_rps = 0
        self.min_rps = float('inf')
        self.rps_window = []

    def stop(self):
        self.end_time = time.time()

    def add_packet(self):
        self.packet_count += 1

    def update_rps(self, rps):
        with self.lock:
            self.rps_samples.append(rps)
            self.rps_window.append(rps)
            if len(self.rps_window) > self.window_size:
                self.rps_window.pop(0)
            if rps > self.max_rps:
                self.max_rps = rps
            if rps < self.min_rps:
                self.min_rps = rps

    def get_smoothed_rps(self):
        with self.lock:
            if not self.rps_window:
                return 0
            return sum(self.rps_window) / len(self.rps_window)

    def get_stats(self):
        if not self.end_time or not self.start_time:
            return None

        duration = self.end_time - self.start_time
        avg_rps = sum(self.rps_samples) / len(self.rps_samples) if self.rps_samples else 0
        if self.min_rps == float('inf'):
            self.min_rps = 0

        return {
            'duration': duration,
            'total_packets': self.packet_count,
            'avg_rps': avg_rps,
            'max_rps': self.max_rps,
            'min_rps': self.min_rps,
            'avg_pps': self.packet_count / duration if duration > 0 else 0
        }

    def print_stats(self):
        stats = self.get_stats()
        if not stats:
            return

        print("\n  ATTACK STATISTICS")
        print(f"  Duration:           {stats['duration']:.2f} seconds")
        print(f"  Total Packets:      {stats['total_packets']:,}")
        print(f"  Average RPS:        {stats['avg_rps']:.0f}")
        print(f"  Maximum RPS:        {stats['max_rps']:.0f}")
        print(f"  Minimum RPS:        {stats['min_rps']:.0f}")
        print(f"  Average PPS:        {stats['avg_pps']:.0f}")

class AttackAnimation:
    def __init__(self):
        self.frames = [
            "[⠋] Attacking...",
            "[⠙] Attacking...",
            "[⠹] Attacking...",
            "[⠸] Attacking...",
            "[⠼] Attacking...",
            "[⠴] Attacking...",
            "[⠦] Attacking...",
            "[⠧] Attacking...",
            "[⠇] Attacking...",
            "[⠏] Attacking..."
        ]
        self.current_frame = 0

    def get_frame(self):
        frame = self.frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        return frame

    def print_attack_status(self, target, packets, rps, elapsed, status="ATTACKING"):
        frame = self.get_frame()
        print(f"\r{frame} Target: {target} | Status: {status} | Packets: {packets:,} | RPS: {rps:.0f} | Time: {elapsed:.1f}s", end="", flush=True)

    def print_target_status(self, target, status, latency):
        print(f"\n  TARGET STATUS")
        print(f"  Target: {target}")
        print(f"  Status: {status}")
        print(f"  Latency: {latency}\n")

    def print_progress_bar(self, current, total, width=40):
        progress = current / total if total > 0 else 0
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        percent = progress * 100
        return f"[{bar}] {percent:.1f}%"
