import argparse
import subprocess
import sys
from pathlib import Path

def run_generate_data(args):
    """Run the synthetic data generation script."""
    script = Path(__file__).parent.parent / "scripts" / "generate_data.py"
    subprocess.run([sys.executable, str(script), "--output-dir", args.output_dir], check=True)

def run_pipeline(args):
    """Execute the full pipeline sequentially."""
    orchestrator = Path(__file__).parent.parent / "pipeline" / "main_orchestrator.py"
    output_file = Path(args.output_dir) / "cleaned_orbit_data.csv"
    cmd = [sys.executable, str(orchestrator), "--input", args.input, "--output", str(output_file)]
    if args.config:
        cmd.extend(["--config", args.config])
    subprocess.run(cmd, check=True)

def run_visualize(args):
    """Launch the visualization script."""
    viz = Path(__file__).parent.parent / "pipeline" / "visualize_results.py"
    subprocess.run([sys.executable, str(viz), "--input", args.input], check=True)

def main():
    parser = argparse.ArgumentParser(prog="cosmic-sanitizer", description="CLI for Cosmic Telemetry Sanitizer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate-data", help="Generate synthetic telemetry data")
    gen_parser.add_argument("--output-dir", default="data/raw_telemetry", help="Directory to store generated data")
    gen_parser.set_defaults(func=run_generate_data)

    pipe_parser = subparsers.add_parser("run-pipeline", help="Run the full sanitization pipeline")
    pipe_parser.add_argument("--input", required=True, help="Path to raw telemetry CSV")
    pipe_parser.add_argument("--output-dir", default="data/sanitized_telemetry", help="Directory for processed data")
    pipe_parser.add_argument("--config", default="config/settings.json", help="Path to config JSON")
    pipe_parser.set_defaults(func=run_pipeline)

    viz_parser = subparsers.add_parser("visualize", help="Visualize pipeline results")
    viz_parser.add_argument("--input", required=True, help="Path to processed telemetry CSV")
    viz_parser.set_defaults(func=run_visualize)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
