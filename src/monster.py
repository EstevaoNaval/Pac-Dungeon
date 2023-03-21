from math import dist
from operator import ne
from os import path
from random import randint
import pygame
from knight import Knight

from settings import NUM_TILE_MAZE_X, NUM_TILE_MAZE_Y, screen, CELL_WIDTH, CELL_HEIGHT, INITIAL_POSITION_X_GAME, INITIAL_POSITION_Y_GAME
from game_data import *
from support import grid_2_pix_pos, import_and_cut_tileset_into_tiles, pix_2_grid_pos

vec = pygame.math.Vector2

class Monster(pygame.sprite.Sprite):
    def __init__(self, level, pos, monster_number, monster_type):
        pygame.sprite.Sprite.__init__(self)
        self.level = level

        self.grid_pos = pos
        self.starting_pos = [pos[0], pos[1]]
        self.pix_pos = grid_2_pix_pos(pos)

        self.monster_number = str(monster_number)
        self.monster_type = monster_type
        self.action_mode = "scatter"
        self.monster_personality = self.set_monster_personality()

        self.direction = vec(0, 0)
        self.speed = self.set_speed()
        self.target = None
        self.last_right_or_left_direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = 1
        self.load_maze_grid()

        self.load_monster_sprite()

        self.img_with_prey_sprite = 1
        self.curr_sprite = 0
        self.image = self.monster_right_sprites[self.curr_sprite]

        self.rect = pygame.Rect(0, 0, self.monster_width, self.monster_height)

    def update(self):
        if self.direction == vec(-1, 0) or self.last_right_or_left_direction == vec(-1, 0):
            if self.level.knight.action_mode == "chaser":
                if self.level.knight.monster_mode_flash:
                    if self.img_with_prey_sprite:
                        self.image = self.monster_left_sprites[int(self.curr_sprite)]
                    else:
                        self.image = self.monster_prey_left_sprites[int(self.curr_sprite)]
                else:
                    self.image = self.monster_prey_left_sprites[int(self.curr_sprite)]
            else:
                self.image = self.monster_left_sprites[int(self.curr_sprite)]
        elif self.direction == vec(1, 0) or self.last_right_or_left_direction == vec(1, 0):
            if self.level.knight.action_mode == "chaser":
                if self.level.knight.monster_mode_flash:
                    if self.img_with_prey_sprite:
                        self.image = self.monster_right_sprites[int(self.curr_sprite)]
                    else:
                        self.image = self.monster_prey_right_sprites[int(self.curr_sprite)]
                else:
                    self.image = self.monster_prey_right_sprites[int(self.curr_sprite)]
            else:
                self.image = self.monster_right_sprites[int(self.curr_sprite)]

        self.speed = self.set_speed()

        self.target = self.set_target()

        self.action_mode = self.set_action_mode()

        if self.target != self.grid_pos:
            
            self.pix_pos[0] += self.direction.x * self.speed
            self.pix_pos[1] += self.direction.y * self.speed

            self.rect.x = self.pix_pos[0]
            self.rect.y = self.pix_pos[1]

            if self.time_to_move():
                if self.stored_direction != None:
                    self.direction = self.stored_direction
                self.move()

        # self.image = self.monster_right_sprites[int(self.curr_sprite)]

        self.curr_sprite += 0.1
        if self.curr_sprite >= len(self.monster_left_sprites): self.curr_sprite = 0

        self.grid_pos = pix_2_grid_pos(self.pix_pos)
    
    def remaining_pill(self):
        return len(self.level.rect_pill)
    
    def draw(self):
        self.image.blit(screen, self.pix_pos)
        pass

    def set_speed(self):
        if self.grid_pos in self.level.coord_tunnel:
            return specs["step_{}".format(self.level.main.step)]["monster_tunnel_speed"]
        elif self.action_mode == "prey":
            return specs["step_{}".format(self.level.main.step)]["fright_ghost_speed"]
        elif self.action_mode == "elroy_2":
            return  specs["step_{}".format(self.level.main.step)]["elroy_2_speed"]
        elif self.action_mode == "elroy_1":
            return  specs["step_{}".format(self.level.main.step)]["elroy_1_speed"]
        elif self.action_mode in ["chaser", "scatter"]:
            return specs["step_{}".format(self.level.main.step)]["monster_speed"]
        

    def set_target(self):
        if self.monster_personality == "blinky":
            return self.level.knight.grid_pos
        elif self.monster_personality == "pinky":
            '''if dist(self.grid_pos, self.level.knight.grid_pos) <= 4:
                return self.level.knight.grid_pos
            else:
                return [self.level.knight.grid_pos[0] + 4 * int(self.level.knight.direction.y), self.level.knight.grid_pos[1] + 4 * int(self.level.knight.direction.x)]'''
            return self.level.knight.grid_pos
        elif self.monster_personality == "inky":
            '''knight_offset = [self.level.knight.grid_pos[0] + 2 * self.level.knight.direction.x, self.level.knight.grid_pos[1] + 2 * self.level.knight.direction.y]
            return [2 * (knight_offset[0] - self.level.monsters[0].grid_pos[0]), 2 * (knight_offset[1] - self.level.monsters[0].grid_pos[1])]'''
            return self.level.knight.grid_pos
        else:
            '''if dist(self.grid_pos, self.level.knight.grid_pos) >= 8:
                return self.level.knight.grid_pos
            else:
                pass'''
            return self.level.knight.grid_pos
    
    def get_nearest_walkable_tile(self, target):
        min = float(1000)
        min_index_column = 0
        min_index_row = 0

        for index_row in range(0, NUM_TILE_MAZE_X):
            for index_column in range(0, NUM_TILE_MAZE_Y):
                if [index_column, index_row] not in self.level.coord_wall and [index_column, index_row] not in self.level.coord_path_monster_go_through_wall:
                    if dist([index_column, index_row], [target[0], target[1]]) < min:
                        min = dist([index_column, index_row], [target[0], target[1]])
                        min_index_column = index_column
                        min_index_row = index_row
        
        return [min_index_column, min_index_row]

        '''for neightbor_raius in range(1, 5):
            for index_row in range(max(0, target[1] - neightbor_raius), min(target[1] + neightbor_raius+1, NUM_TILE_MAZE_X)):
                for index_column in range(max(0, target[0] - neightbor_raius), min(target[0] + neightbor_raius+1, NUM_TILE_MAZE_Y)):
                    if (abs(target[1] - index_row) >= neightbor_raius or abs(target[0] - index_column) >= neightbor_raius):
                        if [index_column, index_row] not in self.level.coord_wall and [index_column, index_row] not in self.level.coord_path_monster_go_through_wall:
                            return [index_column, index_row]
        pass'''


    def time_to_move(self):
        if int(self.pix_pos[0]) % CELL_WIDTH == 0: 
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0): return 1
        if int(self.pix_pos[1]) % CELL_HEIGHT == 0: 
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0): return 1
        return 0

    def move(self):
        if self.monster_personality in ["blinky","pinky","inky","clyde"]:
            self.direction = self.get_path_direction(self.target)
        '''if self.monster_personality == "clyde":
            self.direction = self.get_random_direction()'''
        
        if self.direction == vec(-1, 0) or self.direction == vec(1, 0):
            self.last_right_or_left_direction = self.direction
        self.stored_direction = self.direction
    
    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)
    
    def find_next_cell_in_path(self, target):
        if target[0] >= 28: target[0] = 27
        elif target[0] < 0: target[0] = 0

        if target[1] >= 36: target[1] = 35
        elif target[1] < 0: target[1] = 0

        if target in self.level.coord_wall or target in self.level.coord_path_monster_go_through_wall:
            target = self.get_nearest_walkable_tile(target)

        path = self.a_star(self.grid_pos, target)
        if len(path) > 1:
            return list(path[1])
        else: 
            return list(path[0])

    def get_random_direction(self):
        while True:
            number = randint(1, 4)
            if number == 1:
                x_dir, y_dir = 1, 0
            elif number == 2:
                x_dir, y_dir = 0, 1
            elif number == 3:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos[0] + x_dir, self.grid_pos[1] + y_dir)
            if next_pos not in self.level.coord_wall:
                break
        return vec(x_dir, y_dir)

    class Node:
        '''
        A node class for A* Pathfinding
        parent is parent of the current Node
        position is current position of the Node in the maze
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
        '''

        def __init__(self, parent=None, position=None):
            self.parent = parent
            self.position = position

            self.g = 0
            self.h = 0
            self.f = 0
        def __eq__(self, other):
            return self.position == other.position

    #This function return the path of the search
    def return_path(self, current_node):
        path = []

        # here we create the initialized result maze with -1 in every position
        current = current_node

        while current is not None:
            path.append(current.position)
            current = current.parent
        # Return reversed path as we need to show from start to end path
        path = path[::-1]

        return path
        
    def a_star(self, start, end):
        '''
            Returns a list of tuples as a path from the given start to the given end in the given maze
            :param start:
            :param end:
            :return:
        '''

        # Create start and end node with initized values for g, h and f
        start_node = self.Node(None, tuple(start))
        start_node.g = start_node.h = start_node.f = 0

        '''if end[0] >= 28: end[0] = 27
        elif end[0] < 0: end[0] = 0

        if end[1] >= 36: end[1] = 35
        elif end[1] < 0: end[1] = 0'''

        '''if self.maze[end[1]][end[0]] == 2:
            if self.maze[end[1] + 1][end[0]] not in [1,2]:
                end = [end[0], end[1] + 1]
            elif self.maze[end[1]][end[0] - 1] not in [1,2]:
                end = [end[0] - 1, end[1]]
            elif self.maze[end[1] - 1][end[0]] not in [1,2]:
                end = [end[0], end[1] - 1]
            elif self.maze[end[1]][end[0] + 1] not in [1,2]:
                end = [end[0]+1, end[1]]'''

        end_node = self.Node(None, tuple(end))
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both yet_to_visit and visited list
        # in this list we will put all node that are yet_to_visit for exploration. 
        # From here we will find the lowest cost node to expand next
        yet_to_visit_list = []  
        # in this list we will put all node those already explored so that we don't explore it again
        visited_list = [] 
        
        # Add the start node
        yet_to_visit_list.append(start_node)
        
        # Adding a stop condition. This is to avoid any infinite loop and stop 
        # execution after some reasonable number of steps
        outer_iterations = 0
        max_iterations = (len(self.maze) // 2) ** 10

        # what squares do we search . serarch movement is left-right-top-bottom 
        #(4 movements) from every positon

        move  = [[0, -1], # go up
                [ -1, 0], # go left
                [ 0, 1 ], # go down
                [ 1, 0 ]] # go right


        """
            1) We first get the current node by comparing all f cost and selecting the lowest cost node for further expansion
            2) Check max iteration reached or not . Set a message and stop execution
            3) Remove the selected node from yet_to_visit list and add this node to visited list
            4) Perofmr Goal test and return the path else perform below steps
            5) For selected node find out all children (use move to find children)
                a) get the current postion for the selected node (this becomes parent node for the children)
                b) check if a valid position exist (boundary will make few nodes invalid)
                c) if any node is a wall then ignore that
                d) add to valid children node list for the selected parent
                
                For all the children node
                    a) if child in visited list then ignore it and try next node
                    b) calculate child node g, h and f values
                    c) if child in yet_to_visit list then ignore it
                    d) else move the child to yet_to_visit list
        """
        #find maze has got how many rows and columns 
        no_rows, no_columns = NUM_TILE_MAZE_X, NUM_TILE_MAZE_Y
        
        # Loop until you find the end
        
        while len(yet_to_visit_list) > 0:
            
            # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
            outer_iterations += 1    

            
            # Get the current node
            current_node = yet_to_visit_list[0]
            current_index = 0
            for index, item in enumerate(yet_to_visit_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    
            # if we hit this point return the path such as it may be no solution or 
            # computation cost is too high
            if outer_iterations > max_iterations:
                print ("giving up on pathfinding too many iterations")
                return self.return_path(current_node)

            # Pop current node out off yet_to_visit list, add to visited list
            yet_to_visit_list.pop(current_index)
            visited_list.append(current_node)

            '''if len(visited_list) > 1:
                return self.return_path(current_node)'''

            # test if goal is reached or not, if yes then return the path
            if current_node == end_node:
                return self.return_path(current_node)

            # Generate children from all adjacent squares
            children = []

            for new_position in move: 

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range (check if within maze boundary)
                if (node_position[0] > (no_rows - 1) or 
                    node_position[0] < 0 or 
                    node_position[1] > (no_columns -1) or 
                    node_position[1] < 0):
                    continue

                # Make sure walkable terrain
                if self.maze[node_position[1]][node_position[0]] in [1,2]:
                    continue

                # Create new node
                new_node = self.Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                
                # Child is on the visited list (search entire visited list)
                if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + abs(current_node.position[0] - child.position[0]) + abs(current_node.position[1] - child.position[1])
                ## Heuristic costs calculated here, this is using eucledian distance
                child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)) 

                child.f = child.g + child.h

                # Child is already in the yet_to_visit list and g cost is already lower
                if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                    continue

                # Add the child to the yet_to_visit list
                yet_to_visit_list.append(child)
        
    def load_monster_sprite(self):
        if self.monster_type == "zombie":
            self.monster_width, self.monster_height = 32, 34

            path_monster_left = path.join(base_path["path_monster"], "zombie\\", "zombie_{}_run_left.png".format(self.monster_number))
            path_monster_right = path.join(base_path["path_monster"], "zombie\\", "zombie_{}_run_right.png".format(self.monster_number))

            path_monster_prey_left = path.join(base_path["path_monster"], "zombie\\", "prey\\", "zombie_prey_run_left.png")
            path_monster_prey_right = path.join(base_path["path_monster"], "zombie\\" "prey\\", "zombie_prey_run_right.png")
        elif self.monster_type == "ogre":
            self.monster_width, self.monster_height = 32, 32
            
            path_monster_left = path.join(base_path["path_monster"], "ogre\\","ogre_{}_run_left.png".format(self.monster_number))
            path_monster_right = path.join(base_path["path_monster"], "ogre\\","ogre_{}_run_right.png".format(self.monster_number))
        elif self.monster_type == "dark_knight":
            self.monster_width, self.monster_height = 32, 32
            
            path_monster_left = path.join(base_path["path_monster"], "dark_knight\\", "dark_knight_{}_run_left.png".format(self.monster_number))
            path_monster_right = path.join(base_path["path_monster"], "dark_knight\\", "dark_knight_{}_run_right.png".format(self.monster_number))
        else:
            self.monster_width, self.monster_height = 32, 36

            path_monster_left = path.join(base_path["path_monster"], "hades\\", "hades_{}_run_left.png".format(self.monster_number))
            path_monster_right = path.join(base_path["path_monster"], "hades\\", "hades_{}_run_right.png".format(self.monster_number))
            pass

        self.monster_left_sprites = import_and_cut_tileset_into_tiles(path_monster_left, self.monster_width, self.monster_height, self.starting_pos)
        self.monster_right_sprites = import_and_cut_tileset_into_tiles(path_monster_right, self.monster_width, self.monster_height, self.starting_pos)

        self.monster_prey_left_sprites = import_and_cut_tileset_into_tiles(path_monster_prey_left, self.monster_width, self.monster_height, self.starting_pos)
        self.monster_prey_right_sprites = import_and_cut_tileset_into_tiles(path_monster_prey_right, self.monster_width, self.monster_height, self.starting_pos)

    def load_maze_grid(self):
        self.maze = [[0 for x in range(NUM_TILE_MAZE_X)] for x in range(NUM_TILE_MAZE_Y)]
        for cell in self.level.coord_wall:
            if cell[0] < NUM_TILE_MAZE_X and cell[1] < NUM_TILE_MAZE_Y:
                self.maze[cell[1]][cell[0]] = 1
        
        for cell in self.level.coord_path_monster_go_through_wall:
            if cell[0] < NUM_TILE_MAZE_X and cell[1] < NUM_TILE_MAZE_Y:
                self.maze[cell[1]][cell[0]] = 2

    def set_monster_personality(self):
        if self.monster_number == '1':
            return "blinky"
        elif self.monster_number == '2':
            return "pinky"
        elif self.monster_number == '3':
            return "inky"
        else:
            return "clyde"
    
    def set_action_mode(self):
        if self.monster_personality == "blinky":
            if self.remaining_pill() <= specs["step_{}".format(self.level.main.step)]["elroy_2_dots_left"]:
                return "elroy_2"
            elif self.remaining_pill() <= specs["step_{}".format(self.level.main.step)]["elroy_1_dots_left"]:
                return "elroy_1"
        
        return "chaser"

        '''elif self.action_number == 0:
            return "chaser"
        elif self.action_number == 1:
            return "prey"
        elif self.action_number == 2:
            return "defeated"
        else:
            return "scatter"'''
