# Charlie Cook's Midpoint Circle Algortihm Implementation

This python script works together with PIL to compute and render rasterized circles. It can also output ASCII-art representations of said circles.

## Example code
```Python
import mpca
c = mpca.RasterCircle(7)
c.printASCII()
```

### Output
```
Pixels generated for radius 7.
ASCII Art representation set.
            [][][]
        [][]      [][]
    [][]              [][]
    []                  []
  []                      []
  []                      []
[]                          []
[]                          []
[]                          []
  []                      []
  []                      []
    []                  []
    [][]              [][]
        [][]      [][]
            [][][]
```
