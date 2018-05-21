# This file copy pastes a mesh side by side.
# It warps the two channels of a side-by-side stereoscopic video separately.
# The .data meshmap file produced by meshmapper software 
# documents the map starting at bottom left corner and ends in the upper right corner,
# progressing from left to right and then bottom to top.
# See http://paulbourke.net/dataformats/meshwarp/ for a detailed format of meshfile
import sys, os


def main():
    infile_name = sys.argv[1]
    path = infile_name.split(os.sep)
    path[-1] = 'sbs_{}'.format(path[-1])
    outfile_name = os.sep.join(path)
    print("Converting {} to SBS image {}".format(infile_name, outfile_name))

    with open(infile_name, 'r') as infile, open(outfile_name, 'w') as outfile:
        outfile.write(infile.readline()) # read the type. expected: 2 (rectangular)
        line = infile.readline() # read the size of mesh
        w, h = [int(el) for el in line.strip().split()]
        a = w/h  # estimate of aspect ratio

        # Copy the lines
        outfile.write("{} {}\n".format(w*2, h))
        for _ in range(h):

            # print left side
            row_queue = []
            for _ in range(w):
                line = infile.readline()
                assert line != "", "Unexpectedly hit EOF"
                row = [float(num) for num in line.strip().split()]  # read row
                row_queue.append(row)
                row_left = convert_to_stereo_left(a, *row)
                writerow(outfile, row_left)

            # print right side
            assert len(row_queue) == w, "q_length: {}, width: {}, row: {}".format(len(row_queue), w, row)
            for row in row_queue:
                row_right = convert_to_stereo_right(a, *row)
                writerow(outfile, row_right)

def convert_to_stereo_left(a, x, y, u, v, i):
    return round((x-a)/2,8), y, round((u-0)/2,8), v, i

def convert_to_stereo_right(a, x, y, u, v, i):
    return round((x+a)/2,8), y, round((u+1)/2,8), v, i

def writerow(outfile, row):
    row = [str(el) for el in row]
    outfile.write('\t'.join(row)+'\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\
        Usage: python MeshToSBS.py meshfile.data\n\
        This script converts a mesh file into another mesh file that can be used for side-by-side 3D videos.\n\
        See http://paulbourke.net/dataformats/meshwarp/ for the format of mesh file.")
        exit()
    main()