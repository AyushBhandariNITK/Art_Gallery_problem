# Art_Gallery_problem
The Art Gallery Problem (AGP) is one of the classic problems in Computational Geometry.
Many variants of these problems have already been studied.In this paper, we propose an algorithm to solve the art gallery problem in which guards are placed on the vertices of the polygon P i.e gallery.


Problem Statement
Guarding an art gallery with the minimum number of guards who can keep a check on the whole gallery.
We have considered the layout of the art gallery be a simple polygon in which guards are to be placed on the vertices of the polygon .
Let a set S of points is said to guard a polygon if, for every point p in the polygon, there is some q ∈ S such that the line joining p and q does not leave the polygon.


IMPLEMENTATION
First we built a polygon and used a graphical user interface to show instructions on how we can use the tool. 
In the design part we also used prev and next buttons where users can navigate and visualize  the implementation.   
We have used the following algorithms in this tool:
• Ear Clipping Algorithm for Triangulation 
• M-coloring using backtracking for 3-coloring 
• Polygon Visibility

Sample input and sample output

![](images/polygon.png)
Here n=48.We can create polygon of any size and shape.

![](images/triangulation.png)
Results after applying Ear Clipping Algorithm for Triangulation.

![](images/three_coloring_using_dfs.png)
3-coloring algorithm

![](images/displaypos.png)
It tells about possible variations of position of guard that can be used to cover whole polygon

![](images/visibilty.png)
It tells about the range uptil a guard can see in one of the optimal variation
