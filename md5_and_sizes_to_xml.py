import sys
import subprocess
import random
import time
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser, TreeBuilder




# 1 - Launch the md5 command to see the values
def scanner(location):
    with open(temp_scanner, 'w') as f:
        coffee_time = ["Just relax and take a coffee", " ", "☕", "☕", "☕", "☕", "☕", "☕"]
        print('\n\n Time to scan the file. This usually takes around 5-6 minutes.\n')
        i = 0
        while i < len(coffee_time):
            print(coffee_time[i], end='', flush=True)
            i = i + 1
            if i > 0:
                time.sleep(0.2)
                print(coffee_time[i], end='', flush=True)
                i = i + 1
        print('\n')
        
        scanner = subprocess.Popen(f'ls -l && md5 *.* ', cwd=location, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, text=True,)            
           
        for line in scanner.stdout:
            sys.stdout.write(line)
            f.write(line)


        print('SCAN DONE')

    artwork16x9 = []
    artwork2x3 = []
    main = []
    preview = []
    captions = []
    
    extract_scanner = open(temp_scanner, "r")
# 2 - Get the values and save them in variables
    for line in extract_scanner:
        if line.__contains__("16x9.png"):
            artwork16x9.append(line.split())
        elif line.__contains__("2x3.png"):
            artwork2x3.append(line.split())
        elif line.__contains__("en.itt"):
            captions.append(line.split())
        elif line.__contains__("full.mov"):
            main.append(line.split())
        elif line.__contains__("preview.mov"):
            preview.append(line.split())
    

    try:
        # In the list, the first part contains the size
        # From the first part in the list, the fourth one contains the number we want (this would be the original output: [['-rw-r--r--', '1', 'albertorodriguez', 'staff', '2714537', 'Sep', '3', '07:34', 'kn23BE5939-16x9.png'], ['MD5', '(kn23BE5939-16x9.png)', '=', '5440cdc4fe6c9d1a89b6e4fda9f2dfc6']] )
        artwork16x9_size = artwork16x9[0][4]
        # In the list, the second part contains the checksum
        artwork16x9_checksum = artwork16x9[1][3]
    except:
        artwork16x9_size = None
        artwork16x9_checksum = None
    
    try:
        artwork2x3_size = artwork2x3[0][4]
        artwork2x3_checksum = artwork2x3[1][3]
    except:
        artwork2x3_size = None
        artwork2x3_checksum = None

    try:
        captions_size = captions[0][4]
        captions_checksum = captions[1][3]
    except:
        captions_size = None
        captions_checksum = None

    try:
        main_size = main[0][4]
        main_checksum = main[1][3]
    except:
        main_size = None
        main_checksum = None

    try:
        preview_size = preview[0][4]
        preview_checksum = preview[1][3]
    
    except:
        preview_size = None
        preview_checksum = None

    
    subprocess.run(f'rm {temp_scanner}', shell=True)

    return main_size, main_checksum, captions_size, captions_checksum, artwork16x9_size, artwork16x9_checksum, artwork2x3_size, artwork2x3_checksum, preview_size, preview_checksum




def write_XML(section_to_edit, location):

    ## Here we add the results that we got from md5
    values = {
        'full': [main_size, main_checksum],
        'captions': [captions_size, captions_checksum],
        'artwork_16:9': [artwork16x9_size, artwork16x9_checksum],
        'artwork': [artwork2x3_size, artwork2x3_checksum],
        'preview': [preview_size, preview_checksum]
                }


    ctb = TreeBuilder(insert_comments=True)
    xp = XMLParser(target=ctb)
    tree = ET.parse(f'{location}/metadata.xml', parser=xp)
    root = tree.getroot()

    for asset in root.iter('{}asset'): # Into the brackets goes a specific url that I had to remove in order to upload the code to Github for company privacy as this is job related.
        type = asset.get('type')
    
        for value in values:
            if value == section_to_edit:
                element = values[value]
                if value == type:
                    # The asset full has 2 sizes and 2 checksums because it has integrated the captions
                    # We have to edit that part in a different way, that's why this if statement.
                    if type != 'full':
                        for data_file in asset:
                            for i in data_file:
                                if i.tag == '{}size': # Into the brackets goes a specific url that I had to remove in order to upload the code to Github for company privacy as this is job related.
                                    size = i
                                    print(f'\nCurrent size for {type} is: {size.text}')
                                    size.text = f'{element[0]}'
                                    print(f'New size for {type} is: {size.text}')
                                    
                                    ET.register_namespace("", "")
                                    tree.write(f'{location}/metadata.xml')
                                if i.tag == '{}checksum': # Into the brackets goes a specific url that I had to remove in order to upload the code to Github for company privacy as this is job related.
                                    checksum = i
                                    print(f'\nCurrent checksum for {type} is: {checksum.text}')
                                    checksum.text = f'{element[1]}'
                                    print(f'New checksum for {type} is: {checksum.text}')

                                    ET.register_namespace("", "")
                                    tree.write(f'{location}/metadata.xml')

                 # Special treatment for main and captions
                    else:
                        for data_file in asset:
                            role = data_file.get('role')
                            if role == 'source':
                                for i in data_file:
                                    if i.tag == '{}size': # Into the brackets goes a specific url that I had to remove in order to upload the code to Github for company privacy as this is job related.
                                        full_size = i
                                        print(f'\nCurrent main size is: {full_size.text}')
                                        full_size.text = f'{element[0]}'
                                        print(f'New main size is: {full_size.text}')
                                        
                                        ET.register_namespace("", "")
                                        tree.write(f'{location}/metadata.xml')
                                    if i.tag == '{}checksum': # Into the brackets goes a specific url that I had to remove in order to upload the code to Github for company privacy as this is job related.
                                        full_checksum = i
                                        print(f'\nCurrent main checksum is: {full_checksum.text}')
                                        full_checksum.text = f'{element[1]}'
                                        print(f'New main checksum is: {full_checksum.text}')
                                        
                                        ET.register_namespace("", "")
                                        tree.write(f'{location}/metadata.xml')
                            else:
                                for i in data_file:
                                    if i.tag == '{}size': # Into the brackets goes a specific url that I had to remove in order to upload the code to Github for company privacy as this is job related.
                                        caps_size = i
                                        print(f'\nCurrent captions size is: {caps_size.text}')
                                        caps_size.text = f'{values["captions"][0]}'
                                        print(f'New captions size is: {caps_size.text}')
                                        
                                        ET.register_namespace("", "")
                                        tree.write(f'{location}/metadata.xml')
                                    if i.tag == '{}checksum': # Into the brackets goes a specific url that I had to remove in order to upload the code to Github for company privacy as this is job related.
                                        caps_checksum = i
                                        print(f'\nCurrent captions checksum is: {caps_checksum.text}')
                                        caps_checksum.text = f'{values["captions"][1]}'
                                        print(f'New captions checksum is: {caps_checksum.text}')

                                        ET.register_namespace("", "")
                                        tree.write(f'{location}/metadata.xml')


  






if __name__ == "__main__":

    n_output = random.randint(9999999999999, 9999999999999999999)
    temp_scanner =f"md5scanner{n_output}.txt" 

    location = input('Which is the location of the folder? ').strip()

    md5_values = scanner(location)
    print('scanner properly done')
    main_size = md5_values[0]
    main_checksum = md5_values[1]
    captions_size = md5_values[2]
    captions_checksum = md5_values[3]
    artwork16x9_size = md5_values[4]
    artwork16x9_checksum = md5_values[5]
    artwork2x3_size = md5_values[6]
    artwork2x3_checksum = md5_values[7]
    preview_size = md5_values[8]
    preview_checksum = md5_values[9]

    package_content = ['full', 'captions', 'artwork_16:9', 'artwork']

    has_trailer = input('\nDo you have the original trailer? (type <n> if it is missing or has been removed) y/n \n').lower()

    while True:
        if has_trailer == 'y':
            package_content.append('preview')
            break
        elif has_trailer == 'n':
            break
        else:
            print('Sorry, I did not understand.') # Here I add the variable in the main
        has_trailer = input('Do you have the original trailer (type <n> if it is missing or has been removed)? y/n \n').lower()


    # Write the values in the xml
    for element in package_content:
        write_XML(package_content[package_content.index(element)], location)


