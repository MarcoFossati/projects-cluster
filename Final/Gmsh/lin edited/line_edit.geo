//Points
Point(1) = {0, 0, 0, 1};
Point(2) = {6371, 0, 0, 1};
Point(3) = {6491, 0, 0, 1};
Point(4) = {0, 6371, 0, 1};
Point(5) = {0, 6491, 0, 1};
Point(6) = {0, -6371, 0, 1};
Point(7) = {0, -6491, 0, 1};

//Outer Circle
Circle(1) = {5, 1, 3}; Transfinite Line {1} = 10 Using Progression 1;
Circle(3) = {3, 1, 7}; Transfinite Line {3} = 10 Using Progression 1;

//Inner Circle
Circle(2) = {4, 1, 2}; Transfinite Line {2} = 10 Using Progression 1;
Circle(4) = {2, 1, 6}; Transfinite Line {4} = 10 Using Progression 1;

//Lines
Line(5) = {5, 4}; Transfinite Line {5} = 25 Using Progression 1;
Line(6) = {3, 2}; Transfinite Line {6} = 25 Using Progression 1;
Line(7) = {7, 6}; Transfinite Line {7} = 25 Using Progression 1;

//Surfaces
Line Loop(1) = {5, 2, -6, -1};
Plane Surface(1) = {1}; Transfinite Surface {1};
Line Loop(2) = {6, -3, -7, 4};
Plane Surface(2) = {2}; Transfinite Surface {2};

//Recombine Surfaces
Recombine Surface {2};
Recombine Surface {1};

//Revolve
Extrude {{0, 1, 0}, {0, 0, 0}, Pi}{
Surface{1};Layers{18};Recombine;
}
Extrude {{0, 1, 0}, {0, 0, 0}, Pi}{
Surface{2};Layers{18};Recombine;
}