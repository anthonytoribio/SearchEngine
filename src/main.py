import os


def main():

    # assign directory
    directory = 'SearchEngine/DEV/'
    
    # iterate over files in
    # that directory
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            file =os.path.join(subdir, file)
            with open(file, 'r') as opened:
                print('success')
    


if __name__ == "__main__":
    main()