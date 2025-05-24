# A* Pathfinding Visualization

## Overview
This project is a visualization tool for the A* pathfinding algorithm, created as a side project during High School. The application provides an interactive grid where users can experiment with pathfinding concepts and observe how the A* algorithm works in real-time.

## Features
- Interactive grid-based environment for pathfinding visualization
- Multiple modes: standard grid, noise-based terrain, and maze
- Ability to set start and end points by dragging
- Add and remove walls/obstacles with mouse clicks
- Real-time visualization of the A* search algorithm
- Path drawing with highlighted visited nodes and final path

## Controls
- Left Click: Place walls or drag start/end points
- Right Click: Remove walls
- Enter: Start the A* search algorithm
- R: Reset the current grid
- N: Switch to noise mode (terrain with varying costs)
- G: Switch to regular grid mode
- M: Switch to maze mode

## How A* Works
A* is an informed search algorithm used for pathfinding. It combines elements from both Dijkstra's algorithm (complete exploration) and greedy best-first search (heuristic-based).

Here's how it works:

1. Initialization: 
   - Start with the beginning node and assign it a cost of 0
   - Add the start node to an "open set" of nodes to be evaluated

2. Node Evaluation:
   - For each node, A* calculates two costs:
     - g(n): The exact cost to reach this node from the start
     - h(n): The estimated cost (heuristic) to reach the goal from this node
     - f(n): The sum g(n) + h(n), representing the estimated total cost

3. Exploration Process:
   - Always select the node with the lowest f(n) value
   - Examine all neighboring nodes
   - For each neighbor, calculate its g, h, and f values
   - Add unexplored neighbors to the open set
   - Move the current node to a "closed set" (already evaluated)

4. Path Reconstruction:
   - When the goal is reached, follow parent pointers back to the start
   - This reconstructed path is guaranteed to be optimal if the heuristic is admissible

In this implementation, the heuristic used is the Euclidean distance (straight-line distance), which is admissible because it never overestimates the actual cost.

## Why A* Is Efficient
A* is more efficient than other pathfinding algorithms like Dijkstra's algorithm because:
1. It uses a heuristic to guide the search toward the goal more directly
2. It guarantees the shortest path (if the heuristic is admissible)
3. It typically explores fewer nodes than Dijkstra's algorithm

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Ensure you have Python installed
2. Install the required dependency:
   pip install pygame
3. Run the program:
   python main.py

## Project Context
This project is part of a larger exploration of pathfinding algorithms, including Dijkstra and others. It serves as a practical demonstration of how these algorithms work and how they can be visualized to better understand their mechanics.
