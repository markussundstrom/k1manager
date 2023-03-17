import jack
import math

def init_midi():
    global jack_rb
    global max_bytes
    global client
    global outport
    client = jack.Client('K1-Manager')
    outport = client.midi_outports.register('output')
    jack_rb = jack.RingBuffer(512)
    max_bytes = math.floor(client.blocksize / client.samplerate * 31250 / 8)
    @client.set_process_callback
    def process(frames):
        outport.clear_buffer()
        to_read = jack_rb.read_space
        if (to_read > 0):
            if (max_bytes < to_read):
                buffer = jack_rb.read(max_bytes)
            else:
                buffer = jack_rb.read(to_read)
            outport.write_midi_event(0, bytes(buffer))
    @client.set_blocksize_callback
    def set_max_bytes(blocksize):
        global max_bytes
        max_bytes = math.floor(client.blocksize / client.samplerate * 31250 / 8)
    client.activate()

def send_message(message):
    written = jack_rb.write(message)
    if written < len(message):
        print("Ringbuffer write error")

def get_midi_ports():
    ports = client.get_ports('', False, True, True, False, False, False)
    portnames = []
    for p in ports:
        portnames.append(p.name)
    return portnames

def connect_port(port):
    outport.disconnect()
    destport = client.get_port_by_name(port)
    outport.connect(destport)
