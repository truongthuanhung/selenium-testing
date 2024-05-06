import sys

sys.path.extend([
    'Submit_Assignment/',
    'Submit_Assignment/data/'
])

def main(functional, data_driven):
    
    if functional == 'Submit-Assignment':
        from Submit_Assignment import usecase as sb_usecase
        sb_usecase.main(data_driven)
    else:
        usage()

def usage():
    print("################### USAGE ###################")
    print("python run.py test Submit-Assignment usecase")
    print("python run.py test Submit-Assignment equivalence")
    print("python run.py test Submit-Assignment boundary")
    print("python run.py test Search-Activity usecase")
    print("python run.py test Search-Activity equivalence")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()
    else:
        main(sys.argv[2], sys.argv[3])
