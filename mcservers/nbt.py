import configparser

import nbtlib
from nbtlib.tag import List, Compound, String, Byte

class NBT:
    def __init__(self, path):
        self.path = path

    def load(self):
        try:
            self.nbtfile = nbtlib.load(self.path, byteorder="big", gzipped=False)
        except FileNotFoundError:
            self.nbtfile = nbtlib.File({"servers": List[Compound]([])}, byteorder="big", gzipped=False)

    @property
    def servers(self):
        return self.nbtfile["servers"]

    @property
    def rows(self):
        return [
            [
                server.get("name", ""),
                server.get("ip", ""),
                server.get("icon", "") or "",
                server["acceptTextures"] if "acceptTextures" in server else None
            ]
            for server in self.servers
        ]

    def save(self, rows):
        new_servers_list = List[Compound]() # https://minecraft.fandom.com/wiki/Servers.dat_format

        for name, ip, icon, textures in rows:
            name = str(name or "").strip()
            ip = str(ip or "").strip()

            if not name and not ip:
                continue

            server = Compound({
                "name": String(name),
                "ip": String(ip)
            })

            icon = str(icon or "").strip()

            if icon:
                server["icon"] = String(icon)

            if textures in (0, 1):
                server["acceptTextures"] = Byte(textures)

            new_servers_list.append(server)

        self.nbtfile["servers"] = new_servers_list
        self.nbtfile.save(filename=self.path, gzipped=False)

    def export(self, export_path):
        if not self.servers:
            raise ValueError("Empty servers list")

        config = configparser.ConfigParser()
        config.optionxform = str

        for i, (name, ip, icon, textures) in enumerate(self.rows, start=1):
            section_name = f"server_{i}"

            config[section_name] = {
                "name": str(name),
                "ip": str(ip)
            }

            if icon:
                config[section_name]["icon"] = str(icon)

            if textures in (0, 1):
                config[section_name]["acceptTextures"] = str(int(textures))

        with open(export_path, "w", encoding="utf-8") as f:
            config.write(f)