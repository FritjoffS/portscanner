# Port Scanner

A simple and efficient multi-threaded port scanner written in Python. This script allows you to scan a range of ports on a specified IP address to identify open ports, the services running on them, and any banners they may provide.

## Features

- Multi-threaded scanning for faster results.
- Banner grabbing to identify services running on open ports.
- Detailed output during the scanning process.
- Option to log results to a file, including only open ports.
- Command-line interface for easy usage.

## Requirements

- Python 3.x
- `socket` and `threading` libraries (included in the Python standard library)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/port-scanner.git
   cd port-scanner

2. Ensure you have Python 3 installed. You can check your Python version with:

    ```bash
    python --version
    ```
### Usage
To run the port scanner, use the following command:
```bash
python portscanner.py <ip_address> <start_port> <end_port> [-t THREADS] [-o OUTPUT]
```

#### Arguments
```
<ip_address>: The target IP address to scan.
<start_port>: The starting port number for the scan.
<end_port>: The ending port number for the scan.
-t THREADS (optional): The number of threads to use for scanning (default is 10).
-o OUTPUT (optional): The output file to save results. Only open ports will be logged.
```
#### Example

To scan ports 20 to 1024 on the IP address 192.168.1.1 using 50 threads and save the results to scan_results.txt, run:
```bash
python portscanner.py 192.168.1.1 20 1024 -t 50 -o scan_results.txt
```
#### Output

<p>The script will print the scanning progress to the console and save the results of open ports to the specified output file.</p>

<p>The results include:</p>
<ul>
<li>Port number
<li>Status (Open/Closed)
<li>Service running on the port
<li>Banner information (if available)
</ul>

### Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

<ul>
<li> Fork the repository.
<li> Create a new branch (git checkout -b feature-branch).
<li> Make your changes and commit them (git commit -m 'Add new feature').
<li> Push to the branch (git push origin feature-branch).
<li> Open a pull request.
</ul>

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

Use this tool responsibly. Ensure you have permission to scan the target IP address and be aware of the legal implications of port scanning.