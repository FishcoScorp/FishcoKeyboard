# FishcoKeyboard
My keyboard for the program fallout by hackclub\
\
This keyboard was made with convieniece in mind, with 15 customizable macro keys (4 on left 11 on right) as well as a volume dial and small screen. 

# Table of Contents
Bill of Materials: https://github.com/FishcoScorp/FishcoKeyboard/edit/main/README.md#:~:text=Build_Files-,BOM,-.csv \
Photo Gallery: https://github.com/FishcoScorp/FishcoKeyboard/edit/main/README.md#:~:text=Fallout%20Zine.md-,Photo,-Gallery.md \
Code: https://github.com/FishcoScorp/FishcoKeyboard/edit/main/README.md#:~:text=README.md-,code,-.py \
Zine: https://github.com/FishcoScorp/FishcoKeyboard/edit/main/README.md#:~:text=BOM.csv-,Fallout,-Zine.md \
\
I am also in the process of working on a software that will interface with the keyboard and allow me to easily switch macro keys and the display on the screen, and make it easy to flash new code to the keyboard.\
\
<img width="1728" height="2304" alt="Fallout Zine (1)" src="https://github.com/user-attachments/assets/b9a8a6cf-b9f9-49dc-b606-feb89abb5515" />
\
How to put it together! \
I used Kicad, and started by making a matrix with all the keys at about where I thought they were on a subsheet. That looks like this (Don't forget to add diodes too!!!) This works by wiring rows and columns which, when shorted by pressing a button, can be identified and pinpointed similar to using x and y on a graph so that it sends the correct input to your device!
<img width="955" height="661" alt="Screenshot 2026-04-27 at 12 48 47 PM" src="https://github.com/user-attachments/assets/213e1361-f150-4cac-8b38-c14336622c7c" />
\
Then I have the main schematic sheet, where I make all the rest of the connections. Using tags I connect the matrix to the ESP and also the screen and rotary encoder. Notice I connect the grounds of the latter two elements using a GND tag. This is because I am going to use a gnd fill later, which means the board will be coated in a thin layer of copper, removing the need for GND connections as this coating will serve that purpose.
<img width="915" height="627" alt="Screenshot 2026-04-27 at 12 53 35 PM" src="https://github.com/user-attachments/assets/c95b4233-4187-4312-852b-f0b982430c49" />
\
Now bring it over to the PCB editor, where you will shape what your keyboard looks like. You can use an app called KB Placer by creating a layout beforehand on the website http://keyboard-layout-editor.com/ and then importing the JSON to KB placer. However, this did not work for me so I had to manually place everything and create the outline of the keyboard myself. I then connected the matrix, rotary encoder, and screen before adding the GND fill (the red in this photo)
<img width="1263" height="542" alt="Screenshot 2026-04-13 at 10 05 19 PM" src="https://github.com/user-attachments/assets/b246f0a8-3c77-493d-bfbe-129f6b38c093" />
\
Then it was time to cad a case. I used Fusion, using the exported .step file model to draw an outline for my case. Then I added some standoffs using the PCB as a reference with the screw holes I had placed earlier, ensuring stabilization but not breaking the PCB. In this case I made so both the bottom and top had walls so that it would look clean and sleek. I also sunk the keys into the keyboard a little so that it would look slim and cool. I also added a window into the ESP cause I think it would look really cool to be abe to see it, a little glimpse into the work/electronics that are required to make this a reality.
<img width="1274" height="633" alt="Screenshot 2026-04-16 at 11 17 34 AM" src="https://github.com/user-attachments/assets/fe726e19-3f35-4053-a3f1-e5b4d5e4c53c" />
\ 
After this I designed my zine and submitted it, and here we are!


