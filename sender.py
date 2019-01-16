from microbit import *
import radio
radio.config(channel=7)
radio.on()

PACKET_SIZE = 6
msg_size = PACKET_SIZE - 1

def generate_packets(message):
  packets = []
  packet_num = 0
  while message:
    if packet_num > 9:
      return packets
    packet = str(packet_num) + message[:msg_size]
    packets.append(packet)
    packet_num += 1
    message = message[msg_size:]
  return packets

def send_packets(acks_to_receive, packets):
  for ack in acks_to_receive:
    radio.send(packets[ack])
    print(packets[ack])

acks_to_receive = []
TIMEOUT = 1000
msg_sent = False
while True:
  current_time = running_time()
  msg = "today is the first day of summer"

  # button a to start and send all packets
  if button_a.was_pressed():
    packets = generate_packets(msg)
    for i in range(len(packets)):
      acks_to_receive.append(i)
    send_packets(acks_to_receive, packets)
    time_sent = current_time
    msg_sent = True
  
  # receive acks
  msg = radio.receive()
  if msg and 'ack00' in msg:
    ack_num = int(msg[0])
    if ack_num in acks_to_receive:
      acks_to_receive.remove(ack_num)
  
  # on timeout, send all which haven't been acked
  if msg_sent and (current_time - time_sent) > TIMEOUT:
    send_packets(acks_to_receive, packets)
    time_sent = current_time
  
  # have sent and received all acks
  if msg_sent and len(acks_to_receive) == 0:
    display.show(Image.HAPPY)

  # button b resets
  if button_b.was_pressed():
    msg_sent = False
    acks_to_receive = []
    display.clear()
  
