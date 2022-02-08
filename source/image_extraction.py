import os
import fitz
from pathlib import Path
import multiprocessing as mp

CPU_COUNT = mp.cpu_count()*2

def paper_to_image(epaper_dir,source,newspaper,path):
    with fitz.open(epaper_dir.joinpath(source, newspaper)) as doc:
        output_path = path.parent.joinpath("Images", newspaper[:-4])
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        for i in range(0, doc.page_count):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(5, 5))
            output = newspaper[:-4] + "_pg_" + str(i+1) + ".jpg"
            print(f"\t==>Image conversion of page [{i + 1}/{doc.page_count}]")
            pix.save(output_path.joinpath(output))

def extract_image():
    path = Path(__file__).parent
    if not path.parent.joinpath("Images").exists():
        os.mkdir(path.parent.joinpath("Images"))

    epaper_dir = path.parent.joinpath("Newspapers")
    indv_dir = os.listdir(epaper_dir)
    all_newspapers=[]
    for source in indv_dir:
        newspapers = os.listdir(path.joinpath(epaper_dir, source))
        
        for newspaper in newspapers:
            #make list of newspaper,source
            all_newspapers.append([newspaper,source])
    CPU_USED=0
    newspaper_count = 0
    processs=[]
    for newspaper,source in all_newspapers:
        no_of_newspapers = len(all_newspapers)        
        newspaper_count += 1
        print(f"Processing newspaper: {newspaper} ===================[{newspaper_count}/{no_of_newspapers}]")
        
        if newspaper.endswith(".pdf"):
            CPU_USED+=1   
            
            if CPU_USED<=CPU_COUNT: 
                process=mp.Process(target=paper_to_image, args=(epaper_dir,source,newspaper,path))
                processs.append(process)
                print("starting process : %s" % process)
                # pool.apply_async(page_to_image,args=(page, output_path,newspaper,i,page_count))
            if CPU_USED==CPU_COUNT or newspaper_count==no_of_newspapers:
                for process in processs:
                    process.start()
                for process in processs:
                    process.join()
                    process.terminate()
                processs=[]
                CPU_USED=0
                print("One iteration completed")


if __name__ == "__main__":
    extract_image()
