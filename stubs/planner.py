from queue import PriorityQueue
from typing import List, Tuple, TypeVar, Dict
from tilsdk.localization import *
import heapq
from a_star_algorithm import astar

T = TypeVar('T')

class NoPathFoundException(Exception):
    pass


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def is_empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


class Planner:
    def __init__(self, map_:SignedDistanceGrid=None, sdf_weight:float=0.0):
        '''
        Parameters
        ----------
        map : SignedDistanceGrid
            Distance grid map
        sdf_weight: float
            Relative weight of distance in cost function.
        '''
        self.map = map_
        self.sdf_weight = sdf_weight

    def update_map(self, map:SignedDistanceGrid):
        '''Update planner with new map.'''
        self.map = map

    def heuristic(self, a:GridLocation, b:GridLocation) -> float:
        '''Planning heuristic function.
        
        Parameters
        ----------
        a: GridLocation
            Starting location.
        b: GridLocation
            Goal location.
        '''
        return euclidean_distance(a, b)

    def plan(self, start:RealLocation, goal:RealLocation) -> List[RealLocation]:
        '''Plan in real coordinates.
        
        Raises NoPathFileException path is not found.
        Parameters
        ----------
        start: RealLocation
            Starting location.
        goal: RealLocation
            Goal location.
        
        Returns
        -------
        path
            List of RealLocation from start to goal.
        '''

        path = self.plan_grid(self.map, self.map.real_to_grid(start), self.map.real_to_grid(goal))
        return [self.map.grid_to_real(wp) for wp in path]

    def plan_grid(self, arena:SignedDistanceGrid, start:GridLocation, goal:GridLocation) -> List[GridLocation]:
        '''Plan in grid coordinates.
        
        Raises NoPathFileException path is not found.

        Parameters
        ----------
        start : GridLocation
            Starting location.

        goal : GridLocation
            Goal location.
        
        Returns
        -------
        path : list
            List of GridLocation from start to goal.
        '''

        if not self.map:
            raise RuntimeError('Planner map is not initialized.')

        # TODO: Participant to complete

        # A* algorithm
        start_tuple = (start.x, start.y)
        goal_tuple = (goal.x, goal.y)

        path = astar(arena.grid, start_tuple, goal_tuple)

        path_new = []

        for i in path:
            path_new.apppend(GridLocation(i[0], i[1]))

        return path_new

    def reconstruct_path(self,
                         came_from:Dict[GridLocation, GridLocation],
                         start:GridLocation, goal:GridLocation) -> List[GridLocation]:
        '''Traces traversed locations to reconstruct path.
        
        Parameters
        ----------
        came_from: dict
            Dictionary mapping location to location the planner came from.
        start: GridLocation
            Start location for path.
        goal: GridLocation
            Goal location for path.

        Returns
        -------
        path
            List of GridLocation from start to goal.
        '''
        
        current: GridLocation = goal
        path: List[GridLocation] = []
        
        while current != start:
            path.append(current)
            current = came_from[current]
            
        # path.append(start)
        path.reverse()
        return path