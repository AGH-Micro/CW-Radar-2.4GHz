from machine import ADC, Pin
import utime
import ulab as np
from ulab import fft

adc = ADC(26)  # Tutaj pin do ktorego podlaczamy ADC

SAMPLE_SIZE = 1024       # Liczba próbek (N)
sample_rate = 10000      # Częstotliwość próbkowania [Hz]
sample_buffer = np.zeros(SAMPLE_SIZE)
sample_count = 0

def calculate_delta_f(peak_index):
    return sample_rate / SAMPLE_SIZE * peak_index

def find_peak(spectrum):
    # Для пропуску сталої, беремо від 1 індекса
    max_index = 1
    for i in range(2, len(spectrum) // 2):
        if spectrum[i] > spectrum[max_index]:
            max_index = i
    return max_index

def process_samples():
    global sample_buffer, sample_count
    
    # Wykonanie FFT
    spectrum = fft.fft(sample_buffer)
    
    # Obliczenie amplitudy
    magnitude = np.sqrt(spectrum.real * spectrum.real + spectrum.imag * spectrum.imag)
    
    # Szukanie szpilkiiiiiii
    peak_index = find_peak(magnitude)
    
    # Obliczenie delta f
    delta_f = calculate_delta_f(peak_index)
    
    print(f"Wykryto pik przy indeksie {peak_index}")
    print(f"Delta f: {delta_f} Hz")
    
    # Resetowanie bufora i licznika
    sample_count = 0
    sample_buffor.fill(0)
    
    return delta_f

def main():
    global sample_count
    
    # Ustawienie okresu próbkowania
    sample_period_us = int(1000000 / sample_rate)  # w microsek z zalozenia ze mamy 10000Hz 
    
    last_sample_time = utime.ticks_us()
    
    while True:
        current_time = utime.ticks_us()
        
        # Sprawdzenie, czy nadszedł czas na pobranie próbki
        if utime.ticks_diff(current_time, last_sample_time) >= sample_period_us:
            if sample_count < SAMPLE_SIZE:
                # Pobieranie próbki z ADC
                sample_buffer[sample_count] = adc.read_u16()
                sample_count += 1
                last_sample_time = current_time
            
            # Jeśli bufor jest pełny, przetwórz dane
            if sample_count >= SAMPLE_SIZE:
                delta_f = process_samples()
                # Tutaj cos mozna kombinowac z delta_f

if __name__ == "__main__":
    main()
