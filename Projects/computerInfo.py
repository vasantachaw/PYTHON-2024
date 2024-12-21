import os
import sys
import psutil
import platform
import subprocess


# This Script that collects and display basic system details


class Power:
    def __init__(self):

        self.ram = psutil.virtual_memory()
        self.informations = {
            "Node Name": platform.node(),
            "System": platform.system(),
            "Os Name": os.name,
            "Machine": platform.machine(),
            "Platform": sys.platform,
            "System": platform.system(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Architecture": platform.architecture()[0],
            "Processor": platform.processor(),
            "CPU Count": os.cpu_count(),
            "Physical Cores": psutil.cpu_count(logical=False),
            "Logical Cores": psutil.cpu_count(logical=True),
            "Memory Info": f"{round(psutil.virtual_memory().total/(1024**3),2)} GB",
            "Disk Usage": {
                "Disk Type": (
                    "HDD"
                    if "SolidState"
                    in subprocess.check_output(
                        "wmic diskdrive get MediaType", shell=True
                    ).decode()
                    else "SSD"
                ),
                "Total (GB)": round(psutil.disk_usage("/").total / (1024**3), 2),
                "Used (GB)": round(psutil.disk_usage("/").used / (1024**3), 2),
                "Free (GB)": round(psutil.disk_usage("/").free / (1024**3), 2),
            },
            "Ram": {
                "Total GB": round(self.ram.total / 1024**3),
                "Used GB": round(self.ram.used / 1024**3),
                "Free GB": round(self.ram.available / 1024**3),
                "Used Ram Percent": self.ram.percent,
            },
        }

    def shutdown(self):
        print("Your computer will be shuttdown in 30 seconds")
        os.system("shutdown -s -t 30")

    def restart(self):
        print("Your computer restarting now !")
        os.system("shutdown/r")

    def logoff(self):
        print("Your computer loggoff now !")
        os.system("shutdown/l")

    def sleep(self):
        print("your computer sleep now !")
        os.system("shutdown/h")

    def abort(self):
        print("your  computer abort !")
        os.system("shutdown/a")


class ComputerInfo(Power):
    def __init__(self):
        super().__init__()

    def Message(self):
        print()
        print(" 1 . Get System Information ")
        print(" 2 . Get  C P U  Information ")
        print(" 3 . Get RAM Information ")
        print(" 4 . Get Disk Information ")
        print(" 5 . Get Network Information ")
        print(" 6 . Get Power Button ")

    def powerMessage(self):
        print()
        print(" 1 . Get Shutdown ")
        print(" 2 . Get Restart ")
        print(" 3 . Get Logoff ")
        print(" 4 . Get Sleep")
        print(" 5 . Get Abort ")

        print()

    def SystemInfo(self):
        print()
        print(f" Node Name : {self.informations['Node Name']}")
        print(f" OS System : {self.informations['System']}")
        print(f" Platform : {self.informations['Platform']}")
        print(f" Machine : {self.informations['Machine']}")

        try:
            result = subprocess.run(["systeminfo"], capture_output=True, text=True)

            for line in result.stdout.splitlines():
                if "Host Name" in line:
                    pass
                elif "OS Name" in line:
                    print(f" OS Name : {line.split(':')[1].strip()}")
                elif "OS Version" in line:
                    print(f" OS Version : {line.split(':')[1].strip()}")
                elif "System Manufacturer" in line:
                    print(f" System Manufacturer : {line.split(':')[1].strip()}")
                elif "System Model" in line:
                    print(f" System Model : {line.split(':')[1].strip()}")
        except Exception as e:
            print(f"Error: {e}")

        try:
            result = subprocess.run(
                ["wmic", "path", "win32_videocontroller", "get", "caption"],
                capture_output=True,
                text=True,
            )
            graphics_cards = result.stdout.strip().split("\n")[1:]
            if graphics_cards:
                print(" Graphics Cards : ", end="")
                for card in graphics_cards:
                    print(f"{card}", end="")
            else:
                print("No graphics card detected.")

        except Exception as e:
            print(f"Error: {e}")
        print(f" ")

    def ProcessorInfo(self):
        print()
        print(f" Processor : {self.informations['Processor']}")
        print(f" Architecture : {self.informations['Architecture']}")
        print(f" Physical Cores : {self.informations['Physical Cores']}")
        print(f" Logical Cores : {self.informations['Logical Cores']}")
        print(f" CPU Count : {self.informations['CPU Count']}")

        print()

    def DiskInfo(self):
        print()

        print(f" Disk Type : {self.informations['Disk Usage']['Disk Type']}")
        print(f" Total GB : {self.informations['Disk Usage']['Total (GB)']}")
        print(f" Total GB : {self.informations['Disk Usage']['Used (GB)']}")
        print(f" Total GB : {self.informations['Disk Usage']['Free (GB)']}")
        print()

    def RamInfo(self):
        print()
        print(f" Total GB : {self.informations['Ram']['Total GB']}")
        print(f" Used GB : {self.informations['Ram']['Used GB']}")
        print(f" Free GB : {self.informations['Ram']['Free GB']}")
        print(f" Used % : {self.informations['Ram']['Used Ram Percent']}")

    def NetworkInfo(self):
        network_info = psutil.net_if_addrs()
        net_stats = psutil.net_io_counters()
        print()
        print("Network Interfaces and IP Addresses :")
        for interface, addrs in network_info.items():
            print(f"\nInterface : {interface}")
            for addr in addrs:
                print(
                    f"Address: {addr.address}, Netmask: {addr.netmask}, Broadcast: {addr.broadcast}"
                )

        print("\nNetwork Statistics:")
        print(f"Bytes Sent: {round(net_stats.bytes_sent/1024**2)} KB/s")
        print(f"Bytes Received: {round(net_stats.bytes_recv/1024**2)} KB/s")
        print(f"Packets Sent: {net_stats.packets_sent}")
        print(f"Packets Received: {net_stats.packets_recv}")


if __name__ == "__main__":
    com = ComputerInfo()
    print()
    print("--- Welcome To Computer Details---")
    while True:
        com.Message()
        nu = int(input(" 7 . Exit "))
        print("")
        if nu == 1:
            com.SystemInfo()
        elif nu == 2:
            os.system("cls")
            com.ProcessorInfo()
        elif nu == 3:
            os.system("cls")
            com.RamInfo()
        elif nu == 4:
            os.system("cls")
            com.DiskInfo()
        elif nu == 5:
            os.system("cls")
            com.NetworkInfo()
        elif nu == 6:
            os.system('cls')
            while True:
                os.system('cls')
                com.powerMessage()
                num = print(" 6 . Exit ")
                if num == 1:
                    com.shutdown()
                elif num == 2:
                    os.system("cls")
                    com.restart()
                elif num == 3:
                    os.system("cls")
                    com.logoff()
                elif num == 4:
                    os.system("cls")
                    com.sleep()
                    os.system("cls")
                elif num == 5:
                    os.system("cls")
                    com.abort()
                else:
                    break
        else:
            break
