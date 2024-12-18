import argparse
import subprocess
import platform
import re
import sys

def extract_ips(output):
    """Extract IP addresses from traceroute output."""
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")  # IPv4 regex
    return ip_pattern.findall(output)

def run_traceroute(target, progressive=False):
    """Run traceroute and display only the list of IPs."""
    if platform.system() == "Windows":
        traceroute_cmd = ["tracert", target]
    else:
        traceroute_cmd = ["traceroute", target]

    try:
        with subprocess.Popen(traceroute_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1) as process:
            collected_ips = []
            for line in process.stdout:
                ips = extract_ips(line)
                if progressive and ips:
                    for ip in ips:
                        print(ip)  # Print progressively
                collected_ips.extend(ips)
            process.wait()
            if process.returncode != 0:
                print(f"Error: {process.stderr.read().strip()}", file=sys.stderr)
            elif not progressive:
                # Print the final list if not progressive
                print("\n".join(collected_ips))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Traceroute Script")
    parser.add_argument("target", help="Target URL or IP address for traceroute")
    parser.add_argument("-p", "--progressive", action="store_true", help="Progressive output")
    args = parser.parse_args()

    run_traceroute(args.target, args.progressive)

if __name__ == "__main__":
    main()
