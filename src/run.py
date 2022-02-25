import os, sys
import subprocess



def print_red(msg):
    print("\033[91m {}\033[00m".format(msg))

def write_to_log(filename, msg=""):
    log.write(filename + "\t" + msg + "\n")

if __name__ == "__main__":
    dir_path = sys.argv[1]
    log = open(os.path.join(dir_path, "log.txt"), "a")
    files = filter(lambda file: file.endswith(".py") and not file.endswith(".ir.py"), os.listdir(dir_path))
    sorted_files = sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0]))
    for file in sorted_files:
        file_path  = os.path.join(dir_path, file)
        result = subprocess.run(["2to3", "-w", file_path]) 
        if result.returncode:
            print_red("Conversion failed!")
            write_to_log(file, "Conversion failed")
        result = subprocess.run(["python3", "-m", "src.main", file_path]) 
        if result.returncode:
            print_red("Analysis failed!")
            if result.returncode == 37:
                write_to_log(file, "Failed to parse!")
            else:
                write_to_log(file, "Unknown: " + str(result.returncode))
            continue
        write_to_log(file, "Success!")
    log.close()

    # main.main(test_file_path)