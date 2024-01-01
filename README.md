# Inrith

Python module for real-valued interval arithmetic with support of interval union.

## Examples

```python
from inrith import Interval

i1 = Interval(2, 4)
i2 = Interval(1, 6)
i3 = Interval(0, 1)
print(i1*i2 + i3)
```

## Things to do
* Special cases of division between 2 intervals
* Interval union
