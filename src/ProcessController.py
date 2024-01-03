from src.rawExtrection import extractRawRegions, extractdefiniedRegions
from src.refineExtractions import refineRegions


def process_file (filepath):
   output=  extractRawRegions(filepath)
   refineRegions(output)
   extractdefiniedRegions(output)
   
   print(output)
