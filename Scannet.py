import socket
import subprocess


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    address = s.getsockname()[0]
    s.close()
    return str(address)


def net_check(ip_address):
    result_output = ""
    ports = [22, 80, 443, 8080, 3306, 25565, 3000, 25, 143, 465, 110, 993, 995, 21]
    for port in ports:
        s = socket.socket()
        s.settimeout(2)
        try:
            s.connect((ip_address, port))
            s.close()
            result_output += "Address: " + ip_address + ":" + str(port) + " is open\n"
        except socket.error:
            continue
    return result_output


def check_on(hostname):
    response = subprocess.call(("ping", "-c", "1", hostname))
    return response == 0


if __name__ == "__main__":
    output = ""
    local = get_ip_address().split(".")
    local_not_changed = get_ip_address()
    local.pop(len(local) - 1)
    joined = '.'.join([str(x) for x in local])  # list comprehension
    for x in range(1, 256):
        try:
            remote_address = str(socket.gethostbyaddr(joined + "." + str(x)))
            ip = remote_address.split("'")[3]
            if check_on(ip):
                output += net_check(ip)
            else:
                continue
        except socket.error:
            continue
    print(output)
