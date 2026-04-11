import argparse
import base64
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path


API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"


def normalize_command(command: str, use_designation: bool) -> str:
    command = command.strip()

    if command.startswith("'") and command.endswith("'"):
        return command

    if use_designation:
        return f"'DES={command};'"

    return f"'{command};'"


def build_url(command: str, start_time: str, stop_time: str, use_designation: bool) -> str:
    params = {
        "format": "json",
        "EPHEM_TYPE": "SPK",
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "COMMAND": normalize_command(command, use_designation),
        "START_TIME": start_time,
        "STOP_TIME": stop_time,
    }
    return f"{API_URL}?{urllib.parse.urlencode(params)}"


def download_spk(command: str, output_path: Path, start_time: str, stop_time: str, use_designation: bool) -> None:
    url = build_url(command, start_time, stop_time, use_designation)

    with urllib.request.urlopen(url) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if "spk" not in payload or not payload["spk"]:
        print("Horizons did not return SPK data.", file=sys.stderr)
        if "result" in payload:
            print(payload["result"], file=sys.stderr)
        raise SystemExit(1)

    spk_bytes = base64.b64decode(payload["spk"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(spk_bytes)

    print(f"Saved {output_path} ({len(spk_bytes)} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a small-body SPK from JPL Horizons.")
    parser.add_argument("command", help="Horizons small-body selector, e.g. 136472 or 2005 FY9")
    parser.add_argument("output", help="Output .bsp path")
    parser.add_argument("--start", default="1900-01-01", help="SPK start time")
    parser.add_argument("--stop", default="2150-01-01", help="SPK stop time")
    parser.add_argument(
        "--designation",
        action="store_true",
        help="Treat command as a designation, e.g. 2005 FY9",
    )
    args = parser.parse_args()

    download_spk(args.command, Path(args.output), args.start, args.stop, args.designation)


if __name__ == "__main__":
    main()
