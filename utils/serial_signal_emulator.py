import serial
import time

# Porta virtual ou física
ser = serial.Serial("COM11", 115200)

adc = 0  # valor inicial
step = 2  # variação a cada 0.1 s (~0.1 V/s)
direcao = 1  # 1 = subindo, -1 = descendo

while True:
    # Formata a mensagem para TER SEMPRE 14 BYTES exatos
    # "VALOR " + valor (4 dígitos) + " OK\n" = 6 + 4 + 4 = 14 bytes
    mensagem = f"VALOR {adc:04d} OK\n"  # Exemplo: "VALOR 0512 OK\n"
    ser.write(mensagem.encode("utf-8"))
    print("Enviado:", mensagem.strip())

    # Atualiza o valor (sobe e desce)
    adc += direcao * step
    if adc >= 1023:
        adc = 1023
        direcao = -1
    elif adc <= 0:
        adc = 0
        direcao = 1

    time.sleep(0.01)
