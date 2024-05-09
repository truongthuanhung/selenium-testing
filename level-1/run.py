import sys

sys.path.extend([
    'Submit_Assignment/',
    'Submit_Assignment/data/',
    'Search_Activity/',
    'Search_Activity/data/'
])

def main(functional, data_driven):
    
    if functional == 'Submit-Assignment':

        if data_driven == 'usecase':
            from Submit_Assignment import usecase as sb_usecase
            sb_usecase.main(data_driven)
        elif data_driven == 'equivalence':
            from Submit_Assignment import equivalence as sb_equivalence
            sb_equivalence.main(data_driven)
            
    elif functional == 'Search-Activity':

        if data_driven == 'usecase':
            from Search_Activity import usecase as sa_usecase
            sa_usecase.main(data_driven)
        elif data_driven == 'equivalence':
            from Search_Activity import equivalence as sa_equivalence
            sa_equivalence.main(data_driven)
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
