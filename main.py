import os
from read import read_input_file_as_adjmat

if __name__ == '__main__':
    input_dir = "./inputs"
    for file_name in os.listdir(input_dir):
        with open(os.path.join(input_dir, file_name), 'r') as f:
            adjmat = read_input_file_as_adjmat(f)
        print(adjmat)

    # test
    # with open("/home/project/CS170-Project/25.in") as f:
    #     adjmat = read_input_file_as_adjmat(f)
    # for i in range(25):
    #     for j in range(i):
    #         assert adjmat[i, j] == adjmat[j, i]