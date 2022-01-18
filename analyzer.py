from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import os
import smtplib
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import glob
import csv
from xlsxwriter.workbook import Workbook

# inzr
# Color palette to use on terminal
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# It transforms the .csv file to an xsls format
def conversion():
    for csvfile in glob.glob(os.path.join('.', '*.csv')):
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()


# Takes the data using the raspi current analyzer module
# and makes an adjustment to get more accurate resuuls
def comprobar_corriente():
    data = []
    i2c_bus = board.I2C()

    ina1 = INA219(i2c_bus,addr=0x40)

    ina1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina1.bus_voltage_range = BusVoltageRange.RANGE_16V

    current1 = ina1.current
    power1 = ina1.power

    # Adjustment
    watts = round(power1 * 100, 1) # There is a deviation dealing with big currents
    
    ''' TODO: Apply a percentage of variation correction to improve accuracy'''
    
    return(watts)

# Send the files by email
def sendfiles():
    try:
        print("Sender: Sending results by email...")
        fromaddr = "" # Email address used to send the data
        toaddr = "" # Email address that receive the data
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Objective Achieved - Medicion de Corriente"
        body = "Aqui tienes los resultados del analisis de corriente!"
        msg.attach(MIMEText(body, 'plain'))


        filename = "results.xlsx"
        attachment = open("results.xlsx", "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls() # TLS for more security
        
        s.login(fromaddr, "") # The email sender password should be inserted here
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        attachment.close()
        print("Sender: Email sent successfully!")
        os.remove("results.csv")
        os.remove("results.xlsx")

    except Exception as ex:
        print(str(ex))
        print("Sender: Failed to send email...")

# Send control
# It is needed to send the results faster
# and to avoid overwritting the previous data
instant_sender = False

if instant_sender:
    conversion()
    sendfiles()
    exit()

# Header of the file
resultado = "Fecha,Potencia" + "\n"

# Control variables
count = 0
MAX =  3600 # This will be the (hours of sampling in seconds / the sleep time in seconds) (5 hours in this case with 5 seconds of sleep time)

while(count < MAX):
    time.sleep(5) # We take a sample every 5 seconds of execution
    count = count + 1
    ahora = datetime.now()
    power = comprobar_corriente()
    print(OKBLUE+"(" + str(round((count/MAX)*100)) +"%)"+ ENDC + OKGREEN + "["+ str(ahora) + "]: "+ENDC + OKCYAN + str(power) + "W" + ENDC)
    resultado = resultado + str(ahora) + "," + str(power) + "\n"

file_object = open('results.csv', 'a')
file_object.write(resultado)
file_object.close()
print("Results saved!")

conversion()

sendfiles()