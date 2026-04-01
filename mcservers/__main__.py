from nbt.nbt import NBTFile
import argparse
from pathlib import Path
from rich import print
from rich.table import Table
from .utils import get_servers_path

def list_servers(path): # https://github.com/twoolie/NBT/issues/80
    with open(path, "rb") as f:
        nbtfile = NBTFile(buffer=f)
        servers = nbtfile["servers"]

        table = Table()

        table.add_column("#", style="dim")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("IP Address", style="magenta")
        table.add_column("Icon", style="yellow")
        table.add_column("Textures", style="yellow")

        for i, server in enumerate(servers, start=1): # https://minecraft.fandom.com/wiki/Servers.dat_format
            table.add_row(
                str(i),
                str(server["name"]),
                str(server["ip"]),
                "Yes" if server.get("icon") else "No",
                "Yes" if server.get("acceptTextures") else "No"
            )

        print(table)

def main():
    parser = argparse.ArgumentParser(
        prog="mcservers",
        description="Simple servers.dat reader"
    )

    parser.add_argument(
        "--path",
        default=str(get_servers_path()),
        help="Specify the servers.dat path"
    )

    args = parser.parse_args()
    path = Path(args.path).resolve()

    list_servers(path)

if __name__ == "__main__":
    main()