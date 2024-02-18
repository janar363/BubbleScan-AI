from abc import ABC, abstractmethod

class Grader(ABC):
    """
        Grader class : Grader class can processes pdf's of Scranton/Custom sheets and returns a detail overview of test in csv format.
                       User initalizes grader fucntion with the path of the pdf and calls getResults() function to get test results.
                       Note : If grader model is uncertain about results or encounters errors student sheet would be flaged for review.
    """

    def __init__(self, path) -> None:
        super().__init__()
        self.pdfPath = path

    @abstractmethod
    def getResults(self):
        """
            getResults function : It is access by user after importing grader module in their project.
            implementation : process pdf input from user -> extract key sheet options 
                                -> extract student sheet options -> grade 
                                -> return results in csv format
        """
        pass 

    def processPdf(self):
        """
            processPdf : processes scanned test sheets in the form of pdf and convert them into image (jpg/png)
        """
        pass  
    
    def getBinaryImage(self):
        """
            getBinaryImage : Generates a binary image with only bright(for foreground) and dark(for background) pixels
        """
        pass

    def EnhanceBinaryImage(self):
        pass

    @abstractmethod
    def getOptions(self):
        """
            getOptions function : Is an abstract function implemented by child grader classes 
            Returns : list of options (A,B,C,D,E or None) 
        """
        pass

    @abstractmethod
    def getId(self):
        """
            getId function : Is an abstract function implemented by child grader classes
            Returns : A string (Student Id)
        """
        pass

class ScantronGrader95945(Grader):
    def __init__(self, path) -> None:
        super().__init__(path)
        print("recived path : ", self.pdfPath)

    def getResults(self):
        pass
    
    def getOptions(self):
        pass
    
    def getId(self):
        pass
   
class CustomGrader(Grader):
    
    def __init__(self, path) -> None:
        super().__init__(path)
        print("recived path : ", self.pdfPath)

    def getResults(self):
        pass
    
    def getOptions(self):
        pass
    
    def getId(self):
        pass

