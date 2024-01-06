
import sys






#------------------------------------------------------------------------------#

if __name__ == "__main__":

    params = None
    rectangles = []
    items = []

    # Read input
    c = 0
    for line in sys.stdin:

        if line == "\n":
            c = 1
            continue

        # Read coordinates
        coord = [float(x) for x in line.strip().split(',')]

        # First line contains parameters
        if params is None:
            params = coord
        
        # Add rectangles and items
        elif c == 0:
            rectangles.append(
                [(coord[0], coord[1]),  #bottom left corner
                (coord[0], coord[3]),   #top left corner
                (coord[2], coord[3]),   #top right corner
                (coord[2], coord[1])]   #bottom right corner
            )
        else:
            items.append((coord[0], coord[1]))
            
    solve(rectangles, items, params[2])