# import modules
import qrcode
from PIL import Image
import sqlalchemy.pool as pool
import psycopg2
# taking image which user wants
# in the QR code center
Logo_link = 'ocm-clear.png'

logo = Image.open(Logo_link)

# taking base width
basewidth = 100

# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
QRcode = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H
)




query = "select household_id, people_id from v_registrants"

#function that returns the database connection
def getconn():
    c = psycopg2.connect(
        user='postgres', 
        host='www.cloudority.com', 
        dbname='ocm_db',
        password='passwordrm',
        port='5432'
        )
    return c

#creates a variable called mypool that handles pool connections: max 10
mypool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)

#creates the connection to OCM database
conn = mypool.connect()

#creates cursor for querying the database
cursor = conn.cursor()

#gets the household and people ids of all the people in v_registrants
cursor.execute(query)

#records is a table of all the results
results = cursor.fetchall()
def generateQr(param1, param2):
    code = param2 + "," + param1
    QRcode.clear()
    QRcode.add_data(code, optimize=0)

    QRcode.make()

    QRcolor = 'Black'

    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert("RGB")
    
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    QRimg.save(str(param2) + ".png")


#loop through each row of the results table
count = 0
for row in results:
    household_id = row[0]
    if household_id == None:
        household_id = ""
    people_id = row[1]
    generateQr(household_id, people_id)
    count = count + 1
print("Generated " + str(count) + " QR codes")

#close the database connection
cursor.close()
conn.close()

