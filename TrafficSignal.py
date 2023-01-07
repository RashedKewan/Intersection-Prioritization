
class TrafficSignal:
    def __init__(self, red:int, yellow:int, green:int, minimum:int, maximum:int):
        self.red              :int = red
        self.yellow           :int = yellow
        self.green            :int = green
        self.minimum          :int = minimum
        self.maximum          :int = maximum
        self.signal_text      :str = "30"
        self.total_green_time :int = 0
