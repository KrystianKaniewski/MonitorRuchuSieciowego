import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import psutil as psutil
import time


def check_port(port, port_name, timeout):
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    ans = s.connect_ex((host_ip, port))

    if ans == 0:
        print("[+] port " + port_name + " is open")
    else:
        print("[-] port " + port_name + " is closed")

    s.settimeout(None)
    s.close()


def update(frame):
    global temp1, temp2

    inter = psutil.net_io_counters(pernic=True)
    bytes_recv = inter['Wi-Fi'].bytes_recv
    bytes_sent = inter['Wi-Fi'].bytes_sent

    data_received.append(bytes_recv - temp1)
    # data_received.append(round((bytes_recv - temp1 - data_received[-1]) / 1024))
    if len(data_received) > 10:
        del data_received[0]

    data_sent.append(bytes_sent - temp2)
    # data_sent.append(round((bytes_sent - temp2 - data_sent[-1]) / 1024))
    if len(data_sent) > 40:
        del data_sent[0]

    time_recv.append(time_recv[-1] + 2.0)
    if len(time_recv) > 40:
        del time_recv[0]

    temp1 = bytes_recv
    temp2 = bytes_sent

    print('Odebrane:\t{} bajtów'.format(data_received[-1]))
    print('Wysłane:\t{} bajtów\n'.format(data_sent[-1]))
    # print('Odebrane:\t{} bajtów'.format(bytes_recv))
    # print('Wysłane:\t{} bajtów\n'.format(bytes_sent))

    plt.cla()
    
    ax1.plot(time_recv, data_received, color='tab:red')
    ax1.set_xlabel('time')
    ax1.set_ylabel('received')

    ax2.plot(time_recv, data_sent, color='tab:blue')
    ax2.set_xlabel('time')
    ax2.set_ylabel('sent')

    time.sleep(2)


if __name__ == "__main__":
    std_ports = {'FTP_cont': 20, 'FTP_trans': 21, 'SSH': 22, 'Telnet': 23, 'SMTP': 25,
                 'DNS': 53, 'HTTP': 80, 'POP3': 110, 'NNTP': 119, 'NTP': 123,
                 'IMAP': 143, 'SNMP': 161, 'HTTPS': 443, 'RDP': 3389}
    # for std_port_name, std_port in std_ports.items():
    # check_port(std_port, std_port_name, 5)

    data_received = []
    data_sent = []
    time_recv = []
    for tmp in range (0, 50):
        data_received.append(0)
        data_sent.append(0)
        time_recv.append(0)

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(time_recv, data_received, color='tab:red')
    ax1.set_xlabel('time')
    ax1.set_ylabel('received')

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(time_recv, data_sent, color='tab:blue')
    ax2.set_ylabel('sent', color='tab:blue')

    if time_recv[-1] == 0:
        print('Stan połączenia {}:'.format('Wi-Fi'))
        interfaces = psutil.net_io_counters(pernic=True)
        temp1 = interfaces['Wi-Fi'].bytes_recv
        temp2 = interfaces['Wi-Fi'].bytes_sent

        time.sleep(2)
    ani = FuncAnimation(fig1, update, frames=100, interval=0)
    plt.show()
