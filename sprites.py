import pygame
from settings import *
import math
import numpy
pygame.mixer.init()



class Audio:
    def __init__(self, frequency: int):
        duration = 0.5
        bits = 16
        sample_rate = 44100
        total_samples = int(round(duration * sample_rate))
        data = numpy.zeros((total_samples, 2), dtype=numpy.int16)
        max_sample = 2 ** (bits - 1) - 1

        for sample in range(total_samples):
            sample_time = float(sample) / sample_rate
            for channel in range(2):
                data[sample][channel] = int(round(max_sample * math.sin(2 * math.pi * frequency * sample_time)))

        self.sound = pygame.sndarray.make_sound(data)
        self.current_channel = None

    def play(self):
        self.current_channel = pygame.mixer.find_channel(True)
        self.current_channel.play(self.sound)

    def set_volume(self, volume):
        self.sound.set_volume(volume)

