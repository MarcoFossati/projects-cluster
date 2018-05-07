mesh = 5;
Point(1) = {30, 0, 0, mesh};
Point(2) = {120, 0, 0, mesh};
Line(1) = {1, 2};

Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2}{
Line{1};Layers{9};
}

Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} {
Surface{5};Layers{8};Recombine;
}