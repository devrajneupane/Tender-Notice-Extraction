import os
import fitz
from pathlib import Path
import multiprocessing as mp


#CPU_COUNT returns the no of threads available
#so that we can use all the available threads
#during the execution of the program
CPU_COUNT = mp.cpu_count()

#Control the resolution of the image to be extracted
DPI=200

def paper_to_image(epaper_dir,source,newspaper,path):
    """
    Convert each page of PDF to Image
    epaper_dir= path of the newspapers folder
    source= name of the newspaper source
    newspaper= name of the newspaper
    path= path of the current file
    """
    output_path = path.parent.joinpath("Images")
    if not path.parent.joinpath(output_path).exists():
        os.mkdir(output_path)
    paper_path = path.parent.joinpath(epaper_dir, source, newspaper)

    #Open the PDF
    with fitz.open(epaper_dir.joinpath(source, newspaper)) as doc:
        output_path = path.parent.joinpath("Images", newspaper[:-4])
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        #Iterate over each page
        for i in range(0, doc.page_count):
            #Load the page
            page = doc.load_page(i)

            #Convert the page to pixels with a resolution of given DPI parameter
            pix = page.get_pixmap(dpi=DPI)

            output = newspaper[:-4] + "_pg_" + str(i+1) + ".jpg"
            print(f"\t==>Image conversion of {newspaper[:-15]} page [{i + 1}/{doc.page_count}]")
            pix.save(output_path.joinpath(output))
        print(f"\n\t=====Image conversion of {newspaper[:-15]} finished=====\n")
        

def extract_image():

    print("\n========Converting PDF to Images=======\n")
    path = Path(__file__).parent
    if not path.parent.joinpath("Images").exists():
        os.mkdir(path.parent.joinpath("Images"))

    epaper_dir = path.parent.joinpath("Newspapers")
    try:
        indv_dir = os.listdir(epaper_dir)
    except FileNotFoundError:
        print(f"==>'Newspapers' folder not found in: \n{path.parent}\n==<")
        exit()
    all_newspapers=[]
    if len(indv_dir)==0:
        print(f"==>'Newspapers' folder is empty in:\n {path.parent}\n<==")
        exit()
    #Making a list of all the newspapers present in the Newspapers folder
    #This is done to make multiprocessing more effictient
    for source in indv_dir:
        newspapers = os.listdir(path.parent.joinpath(epaper_dir, source))    
        if len(newspapers)==0:
            print(f"==>\n{source} folder is empty in: \n{path.parent.joinpath(epaper_dir)}\n<==")
            continue
        for newspaper in newspapers:
            all_newspapers.append([newspaper,source])

    #Multiprocessing the execution of the program
    CPU_USED=0
    newspaper_count = 0
    processs=[]
    for newspaper,source in all_newspapers:
        no_of_newspapers = len(all_newspapers)        
        newspaper_count += 1
        print(f"Processing newspaper: {newspaper} ===================[{newspaper_count}/{no_of_newspapers}]")
        
        if newspaper.endswith(".pdf"):

            CPU_USED+=1   #number of processes used so far
            
            #If the no of processes are less than CPU_COUNT, 
            # continue adding new processes
            if CPU_USED<=CPU_COUNT: 
                process=mp.Process(target=paper_to_image, args=(epaper_dir,source,newspaper,path))
                processs.append(process)
            
            #If the no of processes are equal tto CPU_COUNT,
            #Or if no further process can be added,
            # then start the execution of the processes
            if CPU_USED==CPU_COUNT or newspaper_count==no_of_newspapers:

                #Start the execution of the processes
                for process in processs:
                    process.start()
                
                #Wait for the processes to finish
                #This is done to make sure that all the processes are finished
                #before moving to the next newspaper
                #After the processes are finished, it is terminated
                for process in processs:
                    process.join()
                    process.terminate()
                processs=[]
                CPU_USED=0


if __name__ == "__main__":
    extract_image()
