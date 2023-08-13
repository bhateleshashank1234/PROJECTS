import cv2
import numpy as np
import pandas as pd

# Reading the image with opencv
img = cv2.imread("download.png")

# Declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

# Function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    global b,g,r,xpos,ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

# Set mouse callback for the image window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

# Main loop that waits for a key press event
while(1):
    cv2.imshow("image", img)
    if (clicked):
        # Draw a rectangle on the image
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
        # Create text string to display (Color name and RGB values)
        text = getColorName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+str(b)
        # Put the text string on the image
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        # If the sum of the RGB values is greater than or equal to 600, change the text color to black
        if(r+g+b>=600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    # If the user presses the 'Esc' key, exit the main loop
    if cv2.waitKey(20) & 0xFF ==27:
        break

# Destroy all windows when the main loop finishes
cv2.destroyAllWindows()