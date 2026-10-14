# DDoS Attack Tool
https://i.imgur.com/hiuKB8Z.jpeg
## 🚀 Quick Start

### Local Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/ddos-tool.git
cd ddos-tool

# Run the tool
python main.py
```

### GitHub Codespaces
1. Click "Code" → "Codespaces" → "Create Codespace"
2. Wait for setup to complete
3. Run: `python main.py`

### Docker
```bash
# Build and run
docker-compose up

# Or use Docker directly
docker build -t ddos-tool .
docker run --privileged --network host -it ddos-tool
```

### GitHub Actions
1. Go to "Actions" tab
2. Select "DDoS Tool Runner"
3. Click "Run workflow"
4. Enter parameters:
   - Attack type (tcp/udp/http/https/dns/icmp/syn/slowloris)
   - Target IP
   - Port (default: 80)
   - Threads (default: 100)
   - Duration (default: 60)

## 🎯 Features

- **Multi-layer attacks**: Layer 3 (ICMP), Layer 4 (TCP, UDP, SYN), Layer 7 (HTTP, HTTPS, DNS, Slowloris)
- **Multi-target mode**: Attack multiple targets simultaneously
- **Advanced optimizations**:
  - Multiple sockets per thread
  - TCP_NODELAY for reduced latency
  - Custom socket buffer sizes
  - Multiprocessing support
  - Async I/O mode
  - Random payloads and ports
- **Attack presets**: Low, Medium, High, Extreme, Insane
- **Attack modes**: Burst, Sustained, Adaptive
- **Attack history**: View recent attacks
- **Configurable settings**: Fine-tune every parameter

## ⚙️ Settings

Access settings via menu option [10]:
- Sockets per thread (1-20)
- Random payload
- Random ports
- Connection pooling
- Log enabled
- Multiprocessing
- Max processes (1-8)
- Async mode
- TCP_NODELAY
- Socket buffer size (1KB-1MB)

## 📊 Performance

| Preset | Threads | Sockets/Thread | Total Connections |
|--------|---------|----------------|-------------------|
| Low    | 50      | 5              | 250               |
| Medium | 100     | 5              | 500               |
| High   | 500     | 5              | 2,500             |
| Extreme| 1000    | 5              | 5,000             |
| Insane | 2000    | 5              | 10,000            |

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Use only on networks you own or have explicit permission to test. Unauthorized use is illegal and may result in severe legal consequences.

## 🔧 Requirements

- Python 3.7+
- No external dependencies (uses only standard library)
- For ICMP attacks: Administrator/root privileges
- For multiprocessing: Multiple CPU cores recommended

## 📝 License

MIT License - Use at your own risk
