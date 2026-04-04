import argparse
from pathlib import Path

from .utils import get_servers_path, get_export_path, get_timestamp
from .table import Editor
from .nbt import NBT

def main():
    parser = argparse.ArgumentParser(
        prog="mcservers",
        description="Simple servers.dat editor"
    )

    parser.add_argument(
        "--path",
        default=str(get_servers_path()),
        help="Specify the servers.dat path"
    )

    parser.add_argument(
        "--export",
        nargs="?",
        const=str(get_export_path()),
        help="Specify the export text file"
    )

    args = parser.parse_args()
    path = Path(args.path).resolve()

    if path.is_dir():
        path = path / "servers.dat"

    path.parent.mkdir(parents=True, exist_ok=True)

    nbt = NBT(path)
    nbt.load()

    if args.export is not None:
        export_path = Path(args.export).resolve()
        export_path.parent.mkdir(parents=True, exist_ok=True)

        if export_path.is_dir():
            timestamp = get_timestamp()
            export_path = export_path / f"servers_{timestamp}.txt"

        nbt.export(export_path)
        print(f"Exported to {export_path}")
        return

    app = Editor(nbt)
    app.run()

if __name__ == "__main__":
    main()