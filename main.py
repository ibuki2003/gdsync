import rclone
import files
import sys

def main(dry: bool, yes: bool):
    f = files.get_new_files()

    if not dry:
        fs = [] # success
        
        for i in f:
            if i[1] in ['N', 'M']:
                print("uploading file", i[0])
                if yes or input("is this OK?").lower() != 'y':
                    print("aborting")
                    return
                if rclone.upload(i[0]):
                    fs.append(i[0])
        files.register_files(fs)
    else:
        for i in f:
            print('registered file', i[0])
        files.register_files([x[0] for x in f])

if __name__ == "__main__":
    dry = False # run without uploading but updating db
    yes = False
    if '-d' in sys.argv:
        dry = True
    if '-y' in sys.argv:
        yes = True
    if '-dy' in sys.argv or '-yd' in sys.argv:
        dry = True
        yes = True
    
    main(dry, yes)
