# File Collector
## 

### NAME

- *file collector (file_collector.py)*

### DESCRIPTION

- *Walks through a given directory tree finding given file formats and stores it in a zip file*
    
### OPTIONS

- -v  verbose
    
      Prints the filename and its path to stdout.
       
- -m  media
    
      Includes most commom media file extensions to the search criteria.
       
- source
    
      Path to directory tree that will be scanned.
       
- zipfile destination
    
      Path and filename to directory where the zip archive will be placed.
       
- extensions
    
      Files extensions or filename ending as a search criteria ex: txt pdf xls jpeg

### SYNOPSIS

      python3 file_collector.py [OPTIONS] [SOURCE] [ZIPFILE] [EXTENSIONS]
    
### EXAMPLES

      python3 file_collector.py /home/myusername/ /home/documents/my_documents.zip txt pdf doc docx odt

- verbose:

      python3 file_collector.py -v /home/myusername/ /home/documents/my_documents.zip txt pdf doc docx odt

- media:

      python3 file_collector.py -m /home/myusername/ /home/documents/my_documents.zip txt pdf doc docx odt

- verbose & media:

      python3 file_collector.py -vm /home/myusername/ /home/documents/my_documents.zip txt pdf doc docx odt
