from microbit import *
import radio
import random
radio.on()
radio.config(channel=7)

def pass_message(msg, to_channel):
  radio.config(channel=to_channel)
  sleep(50)
  radio.send(msg)
  

def handle_message(msg, channel, message_queue):
  if channel == 7:
    to_channel = 8
  else:
    to_channel = 7
  rand = random.randint(0, 9)
  # 50% of the time, send the message
  if rand < 5:
    if message_queue:
      # handle message queue - send first item and append this item
      next_message = message_queue.pop(0)
      if msg not in message_queue:
        message_queue.append(msg)
        print(message_queue, channel)
    else:
      next_message = msg
    print('sending message:',next_message,'from:',channel)
    pass_message(next_message, to_channel)
  # 30% of the time - add to message queue - after the next one
  elif rand <= 7:
    print('queuing message:',msg,'from:',channel)
    if msg not in message_queue:
      message_queue.append(msg)
      print(message_queue, channel)
  # 20% of the time, drop the packet
  else:
    print('dropped packet:',msg,'from:',channel)
  # 8, 9 - ignore the message.
  return message_queue

message_queue_sender = []
message_queue_receiver = []

TIMEOUT = 5000
last_cleared_sender = 0
last_cleared_receiver = 0
while True:
  current_time = running_time()

  # sender is on ch7, receiver on ch8
  for ch in (7, 8):
    radio.config(channel=ch)
    sleep(50)
    msg = radio.receive()
    if msg:
      if ch == 7:
        message_queue_sender = handle_message(msg, ch, message_queue_sender)
      else:
        message_queue_receiver = handle_message(msg, ch, message_queue_receiver)
  
  # clear 1 item from the send or receive queue every 5 seconds, if there is a queue
  if message_queue_sender and (current_time - last_cleared_sender) > TIMEOUT:
    msg = message_queue_sender.pop(0)
    print('clearing queue msg:',msg,'from:',7)
    pass_message(msg, 8)
    last_cleared_sender = running_time()
  if message_queue_receiver and (current_time - last_cleared_receiver) > TIMEOUT:
    msg = message_queue_receiver.pop(0)
    print('clearing queue msg:',msg,'from:',8)
    pass_message(msg, 7)
    last_cleared_receiver = running_time()
  
  


    
    

