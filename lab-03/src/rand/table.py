from pathlib import Path

class BuiltinTable():
    def __init__(self):
        self.dataFolder = Path("rand/meta/")
        self.oneDigitFilename = 'onedigit.txt'
        self.twoDigitsFilename = 'twodigits.txt'
        self.threeDigitsFilename =  "threedigits.txt"
    def Generate(self, digits = 1):
        if digits == 1:
            fileToOpen = self.dataFolder / self.oneDigitFilename
        elif digits == 2:
            fileToOpen = self.dataFolder / self.twoDigitsFilename
        else:
            fileToOpen = self.dataFolder / self.threeDigitsFilename
        
        f = open(fileToOpen, 'r')

        nums = []
        for line in f:
            nums.append(int(line.strip('\n')))
            
        return nums