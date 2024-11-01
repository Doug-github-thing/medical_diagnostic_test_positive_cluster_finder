import random

POSITIVE = "x"
NEGATIVE = "_"
CLUSTER = "c"

def populate_raw_data():
    # populate the data file with sample ids and results
    with open('cluster_results.csv',"w") as file:
        for i in range(96):
            result = POSITIVE if (int)(random.random()*1.2)==1 else NEGATIVE
            file.write(f"{i+1},{result}\n")

# A queue data structure, for use evaluating BFS
class Queue:
    def __init__(self):
        self.queue = []
    def insert(self, element):
        self.queue.append(element)
    def pop(self):
        element = self.queue[0]
        self.queue = self.queue[1:len(self.queue)]
        return element
    def is_empty(self):
        return len(self.queue) == 0

# Each sample as has an id, a result, and a "bfs_status", indicating if it's been queued or visited
class Sample:
    # expects "sample_props", a comma delimited string
    # representing id and result
    # ie: "34,1\n" representing sample 34 with result 1 
    def __init__(self, sample_props):
        split_props = (str)(sample_props).split(",")
        self.id = split_props[0]
        self.result = (split_props[1].split("\n")[0]) # remove the trailing \n
        self.bfs_status = "not visited"

# Read from the results csv, and return a 2D array of results representing the 96 well plate
def parse_data_into_plate():
    # Parse data into a string of Sample objects
    with open('cluster_results.csv', "r") as file:
        raw_results = file.readlines()
    rows = [row for row in raw_results]
    samples_list = [Sample(sample_props) for (sample_props) in [row for row in rows]]

    # Arrange it into a platemap with rows of length 12, by iterating one sample at a time,
    # and making a new row whenever the number is divisible by 12
    plate = []
    plate_row = []
    for i, sample in enumerate(samples_list):
        plate_row.append(sample)
        if (i+1) % 12 == 0:
            plate.append(plate_row)
            plate_row = []
    return plate

def print_plate(plate):
    for row in plate:
        for sample in row:
            print(sample.result,end=" ")
        print()

def check_adjacent_samples(plate, r, c, queue):
    # check up
    if r > 0 and plate[r-1][c].bfs_status == "not visited" and plate[r-1][c].result == POSITIVE:
        queue.insert((plate[r-1][c], r-1, c))
        plate[r-1][c].bfs_status = "queued"
    # check down
    if r < 7 and plate[r+1][c].bfs_status == "not visited" and plate[r+1][c].result == POSITIVE:
        queue.insert((plate[r+1][c], r+1, c))
        plate[r+1][c].bfs_status = "queued"
    # check left
    if c > 0 and plate[r][c-1].bfs_status == "not visited" and plate[r][c-1].result == POSITIVE:
        queue.insert((plate[r][c-1], r, c-1))
        plate[r][c-1].bfs_status = "queued"
    # check right
    if c < 11 and plate[r][c+1].bfs_status == "not visited" and plate[r][c+1].result == POSITIVE:
        queue.insert((plate[r][c+1], r, c+1))
        plate[r][c+1].bfs_status = "queued"
    

def process_positive(plate, r, c):
    this_cluster = []
    sample = plate[r][c]
    sample.bfs_status = "visited"
    
    # Queue contains positives to check
    queue = Queue()
    queue.insert((sample, r, c))
    while not queue.is_empty():
        this_sample, r, c = queue.pop()
        this_sample.bfs_status = "visited"
        this_cluster.append(this_sample)
        check_adjacent_samples(plate, r, c, queue)
    return this_cluster


def search_for_clusters(plate):
    clusters = [] #hold a list of lists. Each inner list is sample ids within a given cluster

    for r in range(8):
        for c in range(12):
            sample = plate[r][c]
            if sample.bfs_status == "not visited":
                if sample.result == POSITIVE:
                    cluster = process_positive(plate, r, c)
                    if len(cluster) >= 3:
                        clusters.append(cluster)
                else:
                    sample.bfs_status = "visited"

    for row in plate:
        for sample in row:
            for cluster in clusters:
                if sample in cluster:
                    sample.result = CLUSTER

    return clusters

def print_clusters(clusters):
    if len(clusters) == 0:
        print("No clusters")
    else:
        print(f"clusters:")
        for cluster in clusters:
            cluster_str = "{"
            for sample in cluster:
                cluster_str += sample.id + " "
            cluster_str = cluster_str[0:len(cluster_str)-1]
            cluster_str += "}"
            print(cluster_str)

populate_raw_data()
plate = parse_data_into_plate()
clusters = search_for_clusters(plate)
print_plate(plate)
print_clusters(clusters)
