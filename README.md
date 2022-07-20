This project is all about extracting tender notice published on newspaper.
As whole currently this system can extract notices form 5 newspaper portals,
they are Gorkhapatra, Himalayan Times, Kantipur, Kathmandu Post and Rising Nepal.

Not only that each module can be run isolately hence one can give newspaper pdf of any newspaper publisher and the system will extract tender notices. 
If the requirement is to get not only tender notice but all kind of notice then one can skip last module where only tender notices was filtered.

This whole project is implemented on Pyhton Language, it uses Convolution Neural Network to accomplish its objective.




Sample `.env` file

```
URL1 = https://<remaining part of url>
URL2 = https://<remaining part of url>
...
DRIVER_PATH = <full path to>\\chromedriver.exe
BINARY_EXECUTABLE = <full path to>\\brave.exe or /usr/bin/brave
TESSERACT_EXECUTABLE = <path to tesseract executable> // For windows only
USER=<usr>
KEY=<key>
```.
