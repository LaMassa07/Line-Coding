import numpy as np
import matplotlib.pyplot as plt

def manchester(bits):
    t = []
    y = []
    for i, b in enumerate(bits):
        t.append(i*1)
        t.append((i*1)+1/2)
        if b == 0:
            y.append(1)
            y.append(0)
        else:
            y.append(0)
            y.append(1)
    t.append(len(bits)*1)
    y.append(bits[-1])

    return t, y

def plot_nrz_spectrum_analytic(x_signal, y_signal):
    """
    Plotta il segnale NRZ e il suo spettro analitico (forma sinc²),
    con ampiezza scalata in base alla potenza media della sequenza.
    """

    # --- Stima T_bit dai dati ---
    dx = np.diff(x_signal)
    T_bit = np.min(dx[dx > 1e-12])

    # --- Potenza media del segnale (varia con la sequenza) ---
    # Pesa ogni livello per la durata del simbolo
    power = 0.0
    total_time = x_signal[-1] - x_signal[0]
    for i in range(len(x_signal) - 1):
        duration = x_signal[i+1] - x_signal[i]
        power += (y_signal[i] ** 2) * duration
    power /= total_time  # potenza media normalizzata

    # --- Spettro analitico NRZ: S(f) = A * T * sinc²(f*T) ---
    f_max = 4.0 / T_bit   # mostra fino a 4 lobi
    freqs = np.linspace(0, f_max, 10000)

    # sinc in numpy è sinc(x) = sin(πx)/(πx), quindi sinc(f*T) = sinc(f*T)
    spectrum = power * T_bit * (np.sinc(freqs * T_bit)) ** 2

    # Frequenza normalizzata per l'asse x
    freqs_norm = freqs * T_bit   # in unità di 1/T_bit

    # --- Plot ---
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle('Segnale NRZ e Spettro di Potenza (Analitico)', fontsize=14, fontweight='bold')

    # Subplot 1: segnale
    ax1 = axes[0]
    ax1.step(x_signal, y_signal, where='post', color='royalblue', linewidth=2.5)
    ax1.set_title('Segnale NRZ nel tempo')
    ax1.set_xlabel('Tempo [s]')
    ax1.set_ylabel('Ampiezza')
    ax1.set_ylim(-0.3, 1.3)
    ax1.margins(x=0.02)
    ax1.grid(True, alpha=0.3)

    # Subplot 2: spettro sinc²
    ax2 = axes[1]
    ax2.fill_between(freqs_norm, spectrum, alpha=0.15, color='crimson')
    ax2.plot(freqs_norm, spectrum, color='crimson', linewidth=2.5)

    # Linee tratteggiate agli zero-crossing (n/T_bit → n in freq norm)
    for n in range(1, 5):
        ax2.axvline(x=n, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        ax2.text(n + 0.03, max(spectrum) * 0.02, f'{n}/T', fontsize=8,
                 color='gray', va='bottom')

    ax2.set_title('Densità spettrale di potenza NRZ  —  S(f) = P·T·sinc²(f·T)')
    ax2.set_xlabel('Frequenza normalizzata  [× 1/T_bit]')
    ax2.set_ylabel('S(f)')
    ax2.set_xlim(0, 4)
    ax2.set_ylim(bottom=0)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# ── ESEMPIO ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    bits  = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    T_bit = 1.0

    x_pts, y_pts = manchester(bits)

    plot_nrz_spectrum_analytic(np.array(x_pts), np.array(y_pts))