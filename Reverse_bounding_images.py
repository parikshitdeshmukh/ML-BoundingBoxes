from lib import *

def main():
    datasetPath = input("Please provide the NFPA dataset path in the format path/Dataset_folder_name/\n")
    #'/media/parik/New Volume/PractiseProbems/ESSI/NFPA_dataset/'
    color = input("Please provide the bounding box's color as Red or Blue or Green\n")

    bigD = parseImageAndFiles(datasetPath)
    print("Parsing finished!")
    #print(bigD)

    if(color.lower()== "red"):
        l = [0,0,255]
    elif(color.lower() == "green"):
        l = [0,255,0]
    elif(color.lower() == "blue"):
        l = [255,0,0]
    reverse_bound(bigD,datasetPath,l)

    print("The process has been successfully completed! Please check the OutputLabels and OutputImages folders!")

if __name__ == '__main__':
    print("The module has been built considering Python3.6 version in use. It also runs for other versions except some depracations")
    main();
