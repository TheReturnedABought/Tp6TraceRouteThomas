import argparse
import subprocess
import sys
import platform

def run_traceroute(target, progressive=False):
    """Run traceroute (tracert on Windows) and display output."""
    # Detect operating system and set the appropriate command
    if platform.system() == "Windows":
        traceroute_cmd = ["tracert", target]
    else:
        traceroute_cmd = ["traceroute", target]

    # Run the command
    process = subprocess.Popen(traceroute_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output_lines = []
    try:
        for line in process.stdout:
            if progressive:  # Display output progressively
                print(line.strip())
            output_lines.append(line.strip())

        process.wait()
        if process.returncode != 0:
            print(f"Error running traceroute: {process.stderr.read().strip()}", file=sys.stderr)

    except KeyboardInterrupt:
        print("Traceroute interrupted by user.", file=sys.stderr)
        process.terminate()

    return output_lines

def save_to_file(output, filename):
    """Save output to a file."""
    try:
        with open(filename, "w") as file:
            for line in output:
                file.write(line + "\n")
        print(f"Traceroute output saved to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Traceroute script with options for progressive display and output file.")
    parser.add_argument("target", help="URL or IP address to traceroute.")
    parser.add_argument("-p", "--progressive", action="store_true", help="Display traceroute output progressively.")
    parser.add_argument("-o", "--output-file", help="File to save the traceroute output.")
    
    args = parser.parse_args()

    # Run traceroute
    print(f"Running traceroute for: {args.target}")
    output = run_traceroute(args.target, progressive=args.progressive)

    # Save to file if option is provided
    if args.output_file:
        save_to_file(output, args.output_file)

if __name__ == "__main__":
    main()
