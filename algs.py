import heapq
import sys

class Vertex: # Use for A*
        def __init__(self, id, parent=None, cost=0, heur=0):
            self.id = id
            self.parent = parent
            self.cost = cost  
            self.heur = heur  
            self.tot_cost = cost + heur

        def __lt__(self, other):
            return self.tot_cost < other.tot_cost

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█', print_end='\r'):
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}',)
        sys.stdout.flush()
        if iteration == total:
            print(print_end)

class GraphAlgorithms:    
    def dijkstras(adjacency_list, movie_names, start, end):
        queue = [(0, start, [])] # cost, current, predecessors
        visited = set()
        
        while len(queue) != 0:
            cost, current, path = heapq.heappop(queue)
            
            if current == end: # Return if the end vertex was reached
                return [movie_names[movie_id] for movie_id in path + [current]]
            
            if current in visited: # If the current movie has already been visited, continue
                continue
            
            # Regsiter the current movie as visited
            visited.add(current)
            
            if current in adjacency_list: # Check the neighboring movie ids
                for neighbor, edge_cost in adjacency_list[current]:
                    if neighbor not in visited:
                        # Calculate the total cost to reach the neighbor
                        total_cost = cost + edge_cost 
                        
                        # Add the neighbor to the queue with updated cost and path
                        heapq.heappush(queue, (total_cost, neighbor, path + [current]))
        
        # No path exists
        return None

    def astar(adjacency_list, movie_names, start, end):

        open_set = []
        closed_set = set()

        start_vertex = Vertex(start)
        end_vertex = Vertex(end)

        heapq.heappush(open_set, start_vertex)

        while len(open_set) != 0:

            current_vertex = heapq.heappop(open_set)

            if current_vertex.id == end_vertex.id: # Retrace shortest path when current_vertex is is the end_node
                path = []
                while current_vertex:
                    path.append(movie_names[current_vertex.id])
                    current_vertex = current_vertex.parent
                return path[::-1]

            closed_set.add(current_vertex.id)

            if current_vertex.id not in adjacency_list: # Some adjacent values do not hold key values. Nevertheless we can skip these since they have 0 outdegrees
                continue

            for neighbor, edge_cost in adjacency_list[current_vertex.id]:
                if neighbor in closed_set: # If neighbour has been visited already
                    continue
                cost = current_vertex.cost + edge_cost
                heur = 0 # A star is known for a heuristic function that is useful when finding shortest path in a maze like environment. Since our data is not structured like a maze we return 0
                adj_vertex = Vertex(neighbor, current_vertex, cost, heur)

                if any(v.id == adj_vertex.id and v.tot_cost <= adj_vertex.tot_cost for v in open_set): # Check if the vertex is in the open set and if the new edge cost value is greater than what has already been recorded
                    continue

                heapq.heappush(open_set, adj_vertex)
    
    def bellman_ford(adjacency_list, id_to_movie, start, end): #O((V-1)(V)(E) + E) Worst case graph is organized like a linked list

        # Create sitance an predecessors map
        distances = {vertex: float('inf') for vertex in adjacency_list}
        predecessors = {vertex: None for vertex in adjacency_list}
        distances[start] = 0

        # Relax edges V-1 times
        for i in range(len(adjacency_list) - 1):
            for vertex in adjacency_list:
                for neighbor, edge_cost in adjacency_list[vertex]:
                    if neighbor not in distances:
                        distances[neighbor] = float('inf')
                    if distances[vertex] + edge_cost < distances[neighbor]:
                        distances[neighbor] = distances[vertex] + edge_cost
                        predecessors[neighbor] = vertex
            print_progress_bar(i, len(adjacency_list) - 1, prefix='Progress:', suffix='Complete', length=50) # This search algorithm takes the longest time because it is calculating the shortest path to all vertices

        # Retrace the path
        path = []
        current_vertex = end
        while current_vertex is not None:
            path.append(id_to_movie[current_vertex])
            current_vertex = predecessors[current_vertex]

        # Return the distance to the end
        return distances[end], path[::-1]