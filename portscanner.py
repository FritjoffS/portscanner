import socket
import sys
from datetime import datetime
import threading
from queue import Queue
import argparse
import os

# Banner grabbing function
def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return None

# Port scanning function
def scan_port(ip, port, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            banner = grab_banner(ip, port)
            print(f"Port {port:5d}: Open   - Service: {service}   - Banner: {banner}")
            results.append((port, "Open", service, banner))
        else:
            print(f"Port {port:5d}: Closed")
        sock.close()
    except Exception as e:
        print(f"Port {port:5d}: Error   - {str(e)}")

# Worker thread function
def worker(ip, port_queue, results):
    while not port_queue.empty():
        port = port_queue.get()
        print(f"Scanning port {port}...")
        scan_port(ip, port, results)
        port_queue.task_done()

# Main scanning function
def scan_ports(ip, start_port, end_port, num_threads):
    print(f"Scanning target {ip}")
    print(f"Time started: {datetime.now()}\n")

    port_queue = Queue()
    results = []

    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(ip, port_queue, results))
        thread.start()
        threads.append(thread)

    port_queue.join()

    for thread in threads:
        thread.join()

    results.sort()

    print(f"\nTime finished: {datetime.now()}")
    print("Port scanning complete\n")

    return results

# Function to log results to a file
def log_results(ip, start_port, end_port, results, output_file):
    with open(output_file, 'w') as f:
        f.write(f"Scan results for {ip} (Ports {start_port}-{end_port})\n")
        f.write(f"Time started: {datetime.now()}\n\n")
        for port, status, service, banner in results:
            if status == "Open":
                f.write(f"Port {port:5d}: {status}   - Service: {service}   - Banner: {banner}\n")
        f.write(f"\nTime finished: {datetime.now()}\n")

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Start port")
    parser.add_argument("end_port", type=int, help="End port")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-o", "--output", help="Output file to save results")

    args = parser.parse_args()

    results = scan_ports(args.ip, args.start_port, args.end_port, args.threads)

    if args.output:
        log_results(args.ip, args.start_port, args.end_port, results, args.output)
        print(f"Results saved to {args.output}")
    else:
        for port, status, service, banner in results:
            if status == "Open":
                print(f"Port {port:5d}: {status}   - Service: {service}   - Banner: {banner}")