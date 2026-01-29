import math

def cal_irms(Vin:float , f:float , R:float , C:float)->float:
    return  2 * Vin * math.sqrt((f * C / R) * math.tanh(1 / (4 * f * R * C)))
def rise_time(R, C, f):
    return -R*C * math.log(0.05 + 0.95 * math.exp(-1/(2*f*R*C)))






if __name__ == "__main__":
    while True:
        R = float(input("R=?--->"))
        irms = cal_irms(15,20e3,R,0.1e-6)
        PRg = irms*irms*R
        Tr = rise_time(R,0.1e-6,20e+3)
        print(f"with R={R}, IRMS={irms} , P={PRg}, Rise time = {Tr}")




