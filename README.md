# icosphere

Creating geodesic icosahedron with given subdivision frequency. This is different than a more common approach which recursively applies Loop-like subdivision.

Advantage of being able to choose integer subdivision frequency, compared to the recursive subdivision, is in controlling the mesh resolution. Mesh resolution grows quadratically with subdivision frequencies while it grows exponentially with iterations of the recursive subdivision. To be precise, using the recursive subdivision (each iteration being a subdivision with frequency 2), the possible number of vertices grows with iterations <img src="https://render.githubusercontent.com/render/math?math=i"> as 

    <img src="https://render.githubusercontent.com/render/math?math=V(i)= 12 %2B 10\,(2^i %2B 1)\,(2^i - 1)">

which gives a sequence

    12, 42, 162, 642, 2562, 10242, 40962, 163842, 655362, 2621442... 

Notice for example there is no mesh having between 2562 and 10242 vertices. Using subdivision frequency, possible number of vertices grows with <img src="https://render.githubusercontent.com/render/math?math=\nu"> as

    <img src="https://render.githubusercontent.com/render/math?math=V(\nu)=12 %2B 10\,(\nu %2B 1)\,(\nu - 1)">

which gives a sequence  
    
     12, 42, 92, 162, 252, 362, 492, 642, 812, 1002, 1212, 1442, 1692, 1962, 
     2252, 2562, 2892, 3242, 3612, 4002, 4412, 4842, 5292, 5762, 6252, 6762, 
     7292, 7842, 8412, 9002, 9612, 10242...

where <img src="https://render.githubusercontent.com/render/math?math=\nu=32"> gives 10242 vertices, and there are 15 meshes having between 2562 and 10242 vertices. The advantage is even more pronounced when using higher resolutions.
