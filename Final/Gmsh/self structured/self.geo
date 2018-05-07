mesh = 5;

Point(1) = {0, -30, 0, mesh};
Point (2) = {0, -120, 0, mesh};

Line(1) = {1, 2};

Extrude {{0, 0, 1}, {0, 0, 0}, Pi}{
Line{1};Layers{10};
}
