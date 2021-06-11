
import cv2
import os



class SVM:
    namelabels = []
    # function to convert image to features
    def getFeatures(self,image):
        image = cv2.resize(image, (500, 500))
        # convert the image to HSV color-space
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # compute the color histogram
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        # normalize the histogram
        cv2.normalize(hist, hist)
        return hist.flatten()



    # Step1:  prepare training data
    def prepareTrainingData(self,folderPath):
        animals = []
        labels = []

        # Read each directory
        for directoryName in os.listdir(folderPath):

            if directoryName.startswith("."):
                continue

            # Read each image
            for imageName in os.listdir(folderPath + "/" + directoryName):

                if imageName.startswith("."):
                    continue

                # read each image
                imagePath = folderPath + "/" + directoryName + "/" + imageName
                image = cv2.imread(imagePath)

                animals.append(self.getFeatures(image))
                labels.append(SVM.namelabels.index(directoryName))

        return animals, labels
