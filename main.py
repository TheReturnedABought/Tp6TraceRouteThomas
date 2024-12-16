import argparse
import subprocess
import platform
import sys

def run_traceroute(target, progressive=False):
    """Run traceroute (tracert on Windows) and display output."""
    if platform.system() == "Windows":
        traceroute_cmd = ["tracert", target]
    else:
        traceroute_cmd = ["traceroute", target]

    print(f"Executing: {' '.join(traceroute_cmd)}")  # Debugging
    try:
        with subprocess.Popen(traceroute_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1) as process:
            print("Command started. Output:")
            for line in process.stdout:
                if progressive:  # Progressive output
                    print(line.strip())
            process.wait()
            if process.returncode != 0:
                print(f"Error: {process.stderr.read().strip()}", file=sys.stderr)
            else:
                print("Traceroute completed successfully.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Traceroute Script")
    parser.add_argument("target", help="Target URL or IP address for traceroute")
    parser.add_argument("-p", "--progressive", action="store_true", help="Progressive output")
    args = parser.parse_args()

    print(f"Target: {args.target}, Progressive: {args.progressive}")  # Debugging
    run_traceroute(args.target, args.progressive)

if __name__ == "__main__":
    main()
