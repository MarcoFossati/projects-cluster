set term x11
set grid
plot "convergence.vtk" using 1:14 with lines
pause 1
reread


