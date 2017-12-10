- [x] DiGraph
```python
g.add_edge('a','b',weight=4)
g.add_edge('a','c',weight=3)
g.add_edge('d','a',weight=3)
g.add_edge('d','b',weight=3)
g.add_edge('e','a',weight=30)
```
- [x] Сериализация (pickle, last version with timestamp)
- [ ] Реализовать граф долгов
- [ ] Эвристики на графах
   - [ ] self_debt: x -(a)-> x => 0
   - [ ] aggregate: x -(a)-> y & x -(b)-> y => x -(a+b)-> y
   - [ ] x_to_y_to_x: x -(a)-> y & y -(b)-> x & a > b => x -(a - b)-> y
   - [ ] transitive: x -(a)-> y & y -(a)-> z => x -(a)-> z
   - [ ] rucksack: x_1 -(a_1)-> y & ... & x_n -(a_1)-> y & y -(a_1+..+a_n)-> z => x_1 -(a_1)-> z & ... & x_n -(a_1)-> z
