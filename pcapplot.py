from scapy.all import *
import sys

def ip_class(ip):
    classes = ['public',          # 0
               '0.0.0.0/8',       # 1
               '10.0.0.0/8',      # 2
               '127.0.0.0/8',     # 3
               '169.254.0.0/16',  # 4
               '172.16.0.0/12',   # 5
               '192.0.0.0/24',    # 6
               '192.0.2.0/24',    # 7
               '192.18.0.0/15',   # 8
               '192.88.99.0/24',  # 9
               '192.168.0.0/16',  # 10
               '198.51.100.0/24', # 11
               '203.0.113.0/24',  # 12
               '224.0.0.0/4',     # 13
               '240.0.0.0/4'      # 14
              ]
    result = ''
    stripped_ip = ip.split(".")
    oct1 = stripped_ip[0]
    oct2 = stripped_ip[1]
    oct3 = stripped_ip[2]
    oct4 = stripped_ip[3]

    if int(oct1) == 0:
        result = classes[1]
    elif int(oct1) in range(1,10):
        result = classes[0]
    elif int(oct1) == 10:
        result = classes[2]
    elif int(oct1) in range(11,127):
        result = classes[0]
    elif int(oct1) == 127:
        result = classes[3]
    elif int(oct1) == 169 and int(oct2) == 254:
        result = classes[4]
    elif int(oct1) in range(128,172):
        result = classes[0]
    elif int(oct1) == 172 and int(oct2) in range(0,16):
        result = classes[0]
    elif int(oct1) == 172 and int(oct2) in range(16,32):
        result = classes[5]
    elif int(oct1) == 172 and int(oct2) in range(32,256):
        result = classes[0]
    elif int(oct1) in range(173,192):
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) == 0 and int(oct3) == 0:
        result = classes[6]
    elif int(oct1) == 192 and int(oct2) == 0 and int(oct3) == 1:
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) == 0 and int(oct3) == 2:
        result = classes[7]
    elif int(oct1) == 192 and int(oct2) == 0 and int(oct3) in range(3,256):
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) in range(1,18):
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) in range(18,20):
        result = classes[8]
    elif int(oct1) == 192 and int(oct2) in range(20,88):
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) == 88 and int(oct3) in range(0,99):
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) == 88 and int(oct3) == 99:
        result = classes[9]
    elif int(oct1) == 192 and int(oct2) == 88 and int(oct3) in range(100,256):
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) in range(89,168):
        result = classes[0]
    elif int(oct1) == 192 and int(oct2) == 168:
        result = classes[10]
    elif int(oct1) == 192 and int(oct2) in range(169,256):
        result = classes[0]
    elif int(oct1) in range(193,198):
        result = classes[0]
    elif int(oct1) == 198 and int(oct2) in range(0,51):
        result = classes[0]
    elif int(oct1) == 198 and int(oct2) == 51 and int(oct3) in range(0,100):
        result = classes[0]
    elif int(oct1) == 198 and int(oct2) == 51 and int(oct3) == 100:
        result = classes[11]
    elif int(oct1) == 198 and int(oct2) == 51 and int(oct3) in range(101,256):
        result = classes[0]
    elif int(oct1) == 198 and int(oct2) in range(52,256):
        result = classes[0]
    elif int(oct1) in range(199,203):
        result = classes[0]
    elif int(oct1) == 203 and int(oct2) == 0 and int(oct3) in range(0,113):
        result = classes[0]
    elif int(oct1) == 203 and int(oct2) == 0 and int(oct3) == 113:
        result = classes[12]
    elif int(oct1) == 203 and int(oct2) == 0 and int(oct3) in range(114,256):
        result = classes[0]
    elif int(oct1) == 203 and int(oct2) in range(1,256):
        result = classes[0]
    elif int(oct1) in range(204,224):
        result = classes[0]
    elif int(oct1) in range(224,240):
        result = classes[13]
    elif int(oct1) in range(240,256):
        result = classes[14]
    # anything else is not a valid ipv4 address
    return result

def main():
    capture = rdpcap(sys.argv[1])
    sessions = capture.sessions()
    aggr_dict = {}

    for session in sessions:
        payload_len = 0
        s_num = 0
        s_type = "UNKNOWN"
        if sessions[session]:
            if sessions[session][TCP]:
                s_type = "TCP"
                s_num += 1
                p_num = 0
                for pkt in sessions[session][TCP]:
                    p_num += 1
                    payload_len += len(pkt.payload)
            elif sessions[session][UDP]:
                s_type = "UDP"
                s_num += 1
                p_num = 0
                for pkt in sessions[session][UDP]:
                    p_num += 1
                    payload_len += len(pkt.payload)
            if s_type != "UNKNOWN":
                print "src_ip: ", sessions[session][0][IP].src,
                print ip_class(sessions[session][0][IP].src)
                print "src_port: ", sessions[session][0][IP].sport
                print "dst_ip: ", sessions[session][0][IP].dst,
                print ip_class(sessions[session][0][IP].dst)
                print "dst_port:", sessions[session][0][IP].dport
                print "sessions: ", s_num
                print "packets:", p_num
                print "total payload length:", payload_len
                print

if __name__ == "__main__":
    main()