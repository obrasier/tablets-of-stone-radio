from microbit import *
import radio
radio.config(channel=8)
radio.on()

received = []
packets_received = []
new_message = False
while True:
  msg = radio.receive()
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
      new_message = True
  
  # there is a new message to print, display it
  if received and new_message:
    received_str = ""
    for packet in received:
      received_str += packet[1:]
    print(received_str)
    display.scroll(received_str, wait=False, loop=True)
    new_message = False
  
  # if b pressed, reset
  if button_b.was_pressed():
    received = []
    packets_received = []
    new_message = False
    display.clear()
  


  