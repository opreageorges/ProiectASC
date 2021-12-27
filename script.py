# Cod importat din exterior
import time
from pyGT511C3 import FPS
import RPi.GPIO as gpio

# Variabile dependente de implementare

# Numarul maxim de amprente
max_fp = 20

# Pinul la care este conectat butonul de Add
add_fp = 25

# Pinul la care este conectat butonul de DeleteAll
delete_all = 27

# Pinul care v-a da comanda de incuiere
lock_comand_pin = 24

# Pinul care v-a da comanda de descuiere
unlock_comand_pin = 23

# Locul unde este conectat senzorul
device = '/dev/ttyS0'

# Viteza de comunicare senzorului
device_com_rate = 9600

# Starea curenta
curent_state = "unlocked"

def wait_finger(fps):
    while not fps.IsPressFinger():
        FPS.delay(1)
    return

# Functia care face procesul de a adauga o ampenta 
def add_mode(fps):
    id = fps.GetEnrollCount()
    if id == max_fp
        print("Nr maxim de amprente a fost atins")
        return
        
    fps.EnrollStart(id)
    wait_finger(fps)
    if fps.CaptureFinger(True):
        fps.Enroll1()
    else  
        print("Adaugarea amprentei a esuat")
        return

    wait_finger(fps)
    if fps.CaptureFinger(True):
        fps.Enroll2()
    else
        print("Adaugarea amprentei a esuat")    
        return
        
    wait_finger(fps)
    if fps.CaptureFinger(True):
        fps.Enroll3()
    else  
        print("Adaugarea amprentei a esuat")
        return
        
    return

# Functia care sterge toate amprentele  
def dell_mode(fps):
    fps.DeleteAll()
    return

def lock_unlock(fps):
    
    if fps.Identify1_N() != max_fp:
    
        if state == "unlocked":
            gpio.output(lock_comand_pin, gpio.HIGH)
            time.sleep(1)
            gpio.output(lock_comand_pin, gpio.LOW)
            state = "locked"
            
        elif state == "locked":
            gpio.output(unlock_comand_pin, gpio.HIGH)
            time.sleep(1)
            gpio.output(unlock_comand_pin, gpio.LOW)
            state = "unlocked"
            
    return
    
def clean(fps):
    gpio.cleanup()
    fps.Close()

def main():
    
    # Setup initial
    gpio.setmode(gpio.BCM)
    gpio.setup(lock_comand_pin, gpio.OUT)
    gpio.setup(unlock_comand_pin, gpio.OUT)

    gpio.setup(add_fp, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(delete_all, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    
    # Incerc sa fac o conexiune cu senzorul de amprenta
    try:
        fps =  FPS.FPS_GT511C3(device_name=device, baud=device_com_rate,timeout=2,is_com=False)
    except Exception as e:
        print('Exception message: ' + str(e))
        exit(1)
    
    # Daca conexiunea a reusit verific daca a fost data vreo comanda si o execut
    # Daca nu a fost data, astpet 0.5 secunte
    while True:
        try:
            if gpio.input(add_fp):
                add_mode(fps)
            elif gpio.input(delete_all):
                dell_mode(fps)
            elif fps.IsPressFinger():
                lock_unlock(fps)
                
            time.sleep(0.5)
        except KeyboardInterrupt and SystemExit:
            clean()
            exit(0)
            
 if __name__ == "__main__":
    main()