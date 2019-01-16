from microbit import *
import radio
radio.config(channel=8)
radio.on()

received = []
packets_received = []
TIMEOUT = 1000
unprinted_message = False
while True:
  msg = radio.receive()
  current_time = running_time()

  # handle message coming in
  if msg:
    message_num = int(msg[0])
    # if we have the message already, send another ack
    if message_num in packets_received:
      radio.send(str(message_num)+'ack00')
    
    # otherwise, handle message, making sure its not a rogue ack
    elif 'ack00' not in msg:
      packets_received.append(message_num)
      radio.send(str(message_num)+'ack00')
      sleep(50)
      received.append(msg)
      received.sort()
      received_time = running_time()
      unprinted_message = True
  
  # after timeout, and there is a new message to print, display it
  if received and unprinted_message and (current_time - received_time) > TIMEOUT:
    received_str = ""
    for packet in received:
      received_str += packet[1:]
    print(received_str)
    display.scroll(received_str, wait=False, loop=True)
    unprinted_message = False
  


  