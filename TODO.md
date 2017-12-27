- [x] DiGraph
```python
g.add_edge('a','b',weight=4)
g.add_edge('a','c',weight=3)
g.add_edge('d','a',weight=3)
g.add_edge('d','b',weight=3)
g.add_edge('e','a',weight=30)
```
- [x] Сериализация (pickle, last version with timestamp)
- [x] Реализовать граф долгов
- [ ] Эвристики на графах
   - [x] self_debt: $x \xrightarrow{a} x \Rightarrow 0$
   - [x] no_debt: $x \xrightarrow{0} y \Rightarrow 0$
   - [x] aggregate: $x \xrightarrow{a} y \land x \xrightarrow{b} y \Rightarrow x \xrightarrow{a+b} y$
   - [x] x\_to\_y\_to\_x: $x \xrightarrow{a} y \land y \xrightarrow{b} x \land a > b \Rightarrow x \xrightarrow{a - b} y$
   - [x] transitive: $x \xrightarrow{a} y \land y \xrightarrow{a} z \Rightarrow x \xrightarrow{a} z$
   - [ ] cycle: $x_1 \xrightarrow{d_1} x_2 \land x_2 \xrightarrow{d_2} x_3 \land \cdots \land x_n \xrightarrow{d_n} x_1 \Rightarrow d_i := d_i - \min\limits_{j}(d_{j})​$
   - [ ] rucksack: $x_1 \xrightarrow{a_1} y \land \cdots \land x_n \xrightarrow{a_n} y \land y \xrightarrow{a_1+ \cdots +a_n} z \Rightarrow x_1 \xrightarrow{a_1} z \land \cdots \land x_n \xrightarrow{a_n} z$
- [ ] Журнал транзакций
   - [ ] Возможность запросить у бота всю историю долгов для данного чата
      - [ ] История за конкретный период
      - [x] Последние N транзакций
      - [x] История для конкретного юзера
   - [ ] Возможность очистить историю долгов (с согласия всех фигурантов)
      - [ ] Запрос на очистку сбрасывается (и/или):
         - [ ] При добавлении транзакции
         - [ ] Через N минут
   - [ ] Возможность отмены транзакции (старая транзакция остаётся в журнале, однако не учитывается при расчёте графа долгов). При этом граф (либо):
      - [ ] Пересчитывается с нуля
      - [ ] Обновляется с учётом добавления обратной транзакции. Например, отмена транзакции $x \xrightarrow{a} y$ приведёт к тому, что в граф добавится ребро $y \xrightarrow{a} x$
   - [ ] Добавить описание транзакций
- [ ] Общая покупка (поход в бар, ресторан)
   - [ ] Сохранить чек
      - [ ] Доступ к истории сообщений
      - [ ] Ссылка на гуглодоку
      - [ ] File Upload
   - [ ] Кто сколько должен и кто сколько внёс -> кто и кому должен или кому должны денег и кто должны
- [ ] Тесты
   - [x] Добавить тесты
   - [ ] Запуск тестов
- [ ] Логи
   - [ ] Добавить логи

