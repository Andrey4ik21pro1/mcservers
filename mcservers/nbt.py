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
                str(server.get("name", "")),
                str(server.get("ip", "")),
                str(server.get("icon") or ""),
                int(server["acceptTextures"]) if "acceptTextures" in server else None
            ]
            for server in self.servers
        ]

    def save(self, rows):
        new_servers_list = List[Compound]() # https://minecraft.fandom.com/wiki/Servers.dat_format

        for row in rows:
            name = str(row[0] or "").strip()
            ip = str(row[1] or "").strip()

            if not name and not ip:
                continue

            server = Compound({
                "name": String(name),
                "ip": String(ip)
            })

            icon = str(row[2] or "").strip()
            if icon:
                server["icon"] = String(icon)

            if row[3] in (0, 1):
                server["acceptTextures"] = Byte(int(row[3]))

            new_servers_list.append(server)

        self.nbtfile["servers"] = new_servers_list
        self.nbtfile.save(filename=self.path, gzipped=False)

    def export(self, export_path):
        if not self.servers:
            raise ValueError("Empty servers list")

        with open(export_path, "w", encoding="utf-8") as f:
            for row in self.rows:
                name, ip, icon, textures = row

                f.write(f"name = {name}\n")
                f.write(f"ip = {ip}\n")

                if icon:
                    f.write(f"icon = {icon}\n")

                if textures in (0, 1):
                    f.write(f"acceptTextures = {textures}\n")

                f.write("\n")