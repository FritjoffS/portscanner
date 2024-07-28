import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
import socket
from datetime import datetime
import threading
from queue import Queue

class ScannerThread(QThread):
    update_progress = pyqtSignal(int)
    update_result = pyqtSignal(str)
    scan_complete = pyqtSignal(list)

    def __init__(self, ip, start_port, end_port, num_threads):
        QThread.__init__(self)
        self.ip = ip
        self.start_port = start_port
        self.end_port = end_port
        self.num_threads = num_threads

    def run(self):
        results = self.scan_ports(self.ip, self.start_port, self.end_port, self.num_threads)
        self.scan_complete.emit(results)

    def grab_banner(self, ip, port):
        try:
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode().strip()
            return banner
        except:
            return None

    def scan_port(self, ip, port, results):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                banner = self.grab_banner(ip, port)
                result_str = f"Port {port:5d}: Open   - Service: {service}   - Banner: {banner}"
                self.update_result.emit(result_str)
                results.append((port, "Open", service, banner))
            else:
                self.update_result.emit(f"Port {port:5d}: Closed")
            sock.close()
        except Exception as e:
            self.update_result.emit(f"Port {port:5d}: Error   - {str(e)}")

    def worker(self, ip, port_queue, results):
        while not port_queue.empty():
            port = port_queue.get()
            self.scan_port(ip, port, results)
            self.update_progress.emit(port)
            port_queue.task_done()

    def scan_ports(self, ip, start_port, end_port, num_threads):
        port_queue = Queue()
        results = []

        for port in range(start_port, end_port + 1):
            port_queue.put(port)

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker, args=(ip, port_queue, results))
            thread.start()
            threads.append(thread)

        port_queue.join()

        for thread in threads:
            thread.join()

        results.sort()
        return results

class PortScannerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Port Scanner')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Input fields
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('IP:'))
        self.ip_input = QLineEdit()
        input_layout.addWidget(self.ip_input)
        input_layout.addWidget(QLabel('Start Port:'))
        self.start_port_input = QLineEdit()
        input_layout.addWidget(self.start_port_input)
        input_layout.addWidget(QLabel('End Port:'))
        self.end_port_input = QLineEdit()
        input_layout.addWidget(self.end_port_input)
        input_layout.addWidget(QLabel('Threads:'))
        self.threads_input = QLineEdit()
        self.threads_input.setText('10')
        input_layout.addWidget(self.threads_input)
        layout.addLayout(input_layout)

        # Scan button
        self.scan_button = QPushButton('Start Scan')
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

        # Save button
        self.save_button = QPushButton('Save Results')
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)

        central_widget.setLayout(layout)

    def start_scan(self):
        ip = self.ip_input.text()
        start_port = int(self.start_port_input.text())
        end_port = int(self.end_port_input.text())
        num_threads = int(self.threads_input.text())

        self.results_display.clear()
        self.progress_bar.setRange(start_port, end_port)
        self.progress_bar.setValue(start_port)

        self.scanner_thread = ScannerThread(ip, start_port, end_port, num_threads)
        self.scanner_thread.update_progress.connect(self.update_progress)
        self.scanner_thread.update_result.connect(self.update_result)
        self.scanner_thread.scan_complete.connect(self.scan_complete)
        self.scanner_thread.start()

        self.scan_button.setEnabled(False)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_result(self, result):
        self.results_display.append(result)

    def scan_complete(self, results):
        self.results_display.append("\nScan complete!")
        self.scan_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.full_results = results

    def save_results(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'w') as f:
                f.write(f"Scan results\n")
                f.write(f"Time: {datetime.now()}\n\n")
                for port, status, service, banner in self.full_results:
                    if status == "Open":
                        f.write(f"Port {port:5d}: {status}   - Service: {service}   - Banner: {banner}\n")
            self.results_display.append(f"\nResults saved to {filename}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PortScannerGUI()
    ex.show()
    sys.exit(app.exec_())
