
###  1.变量
1. 标识符：允许 数字 字母 _ ，不能使用关键字，严格区分大小写
2. 变量 函数 方法 snake_case 蛇形命名；类名 SnakeCase 大驼峰；常量：MAX_PAGE
### 2.数据结构
1. int \ Decimal \  str
	1. s.strip()、s.split(",")、",".join(["a","b"])、s.replace("python","java")、s.startswith(" he")、s.upper()、len(s)
2. list \ deque \ dict \ set
	1. lst.append(40)，lst.remove(20)，lst.clear()，lst.sort(reverse=True)，lst.reverse()，len(lst)
	2. for k,v in d.items():，d.keys()，d.get("c", 0)
	3. s1.add(10)，len(s1)
3. json
	1. json.dumps(obj)  :  python 对象 → **JSON 字符串**
	2. json.loads(s)  :  JSON 字符串 → **python 对象**
	3. json.dump(obj,fp)  :  ython 对象 → **直接写入文件对象**
	4. json.load(fp)  :  从**文件对象读取** → python 对象
### 3.逻辑条件判断（逻辑表达式）
1. if elif else
2. while True: print("一直跑")
3. for k,v in dict.items(): print(k,v)
4. break 跳出for和while
### 4.函数
1. 构造器
### 5.异常
### 6.面向对象
**定义**:类 = 数据(属性)+ 行为(方法)的封装单元,是"模板";实例 = 按模板创建的具体对象。核心价值:相关数据和操作绑定、边界清晰、职责单一,是模块化架构的原子。四大理念:**封装、继承、多态、抽象**。

#### 6.1 类
1. 最小可用类
```python
class User:
    def __init__(self, name: str, age: int):   # 构造器;self = 实例自身
        self.name = name                        # 实例属性
        self.age = age

    def greet(self) -> str:                     # 实例方法
        return f"hi, {self.name}"

u = User("wyf", 28)      # 实例化,不用 new
u.greet()
```
2. 类属性 vs 实例属性:类属性所有实例共享(常量/计数),实例属性各自独立
```python
class User:
    kind = "human"                # 类属性(共享)
    count = 0
    def __init__(self, name):
        self.name = name          # 实例属性(独立)
        User.count += 1
```
3. 三种方法
```python
class Date:
    def echo(self): ...                      # 实例方法:操作实例状态
    @classmethod
    def from_string(cls, s):                 # 类方法:工厂,替代构造器
        y, m, d = s.split("-")
        return cls(y, m, d)
    @staticmethod
    def is_leap(year): ...                   # 静态方法:无状态工具函数
```
4. @property:方法伪装成属性,读写受控(替代 getter/setter)
```python
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self): return self._balance     # 读
    @balance.setter
    def balance(self, v):                       # 写,可校验
        if v < 0: raise ValueError("balance < 0")
        self._balance = v
```
5. `__repr__` 必写:调试/日志直接可读
```python
    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age})"
```
6. @dataclass:纯数据类自动生成 `__init__/__repr__/__eq__`(生产首选)
```python
from dataclasses import dataclass, field

@dataclass
class Order:
    id: str
    items: list = field(default_factory=list)
    status: str = "created"
```
7. `__slots__`:固定属性、省内存(百万级实例才需要)
```python
class Point:
    __slots__ = ("x", "y")
```

#### 6.2 特性（继承）
1. 封装:藏数据、露接口
	1. `_x` 单下划线 = 约定内部用;`__x` 双下划线 = 名称改写(防子类误覆盖)
	2. 对外只暴露方法/@property,内部实现可随时改 -- 这就是封装的价值
2. 继承:复用 + 建模 "is-a" 关系
```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):                     # 覆写
        return f"{self.name}: wang"
    def fetch(self):                     # 扩展
        return "fetching"
```
	1. `super().__init__(name)` 调父类构造
	2. `isinstance(d, Animal)` 为 True;MRO:Dog -> Animal -> object
	3. 继承层数 <= 2,更深说明设计有问题
3. 多态:同一接口,不同行为
```python
def make_speak(animal):        # 不关心具体类型,只关心"会 speak"
    print(animal.speak())      # Dog/Cat/RobotDog 各自实现
```
	1. 鸭子类型:会 speak 就是可 speak 的对象,不看继承链
4. 抽象:ABC 定义契约,强制子类实现
```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, msg: str): ...

class EmailNotifier(Notifier):
    def send(self, msg): print(f"email: {msg}")
    # 子类不实现 send,实例化直接报错 -- 错误提前暴露
```
5. 魔术方法:让对象像内置类型
	1. `__str__/__repr__` 打印、`__eq__` 比较、`__len__` 支持 len()、`__iter__` 支持 for、`__enter__/__exit__` 支持 with

#### 6.3 生产最佳实践
1. `__repr__` 必写(日志/调试第一生产力);@dataclass 自动带
2. @property 替代 getter/setter;`_` 前缀约定私有
3. **组合优于继承**:has-a 用成员字段,is-a 才继承;继承只为建模和多态
4. @dataclass 写数据类,别手写 `__init__/__repr__/__eq__`
5. 类要小:一个类只有一个变化理由(SRP);超 300 行考虑拆
6. @classmethod 工厂方法比塞满逻辑的 `__init__` 清晰
7. 依赖"接口"(ABC/Protocol)不依赖具体实现,测试才能替换
8. Protocol 结构化类型:不用继承也能定义契约(现代写法)
```python
from typing import Protocol

class Repo(Protocol):
    def save(self, order): ...
# 任何带 save 方法的类自动满足 Repo,无需继承
```
9. 魔术方法按需实现:要打印写 `__repr__`,要比较写 `__eq__`,别一次全写

#### 6.4 与模块/业务结合设计
1. 领域建模:业务概念 -> 类,业务规则进方法(充血模型),不散落成函数
	1. User/Order/Payment 各自带规则:`order.total()`、`order.cancel()`
2. 分层架构里各类的职责
	1. Entity(领域层):数据 + 业务规则(@dataclass + 方法)
	2. Service(业务层):编排流程,依赖注入进来
	3. Repository(数据层):save/load,隔离 DB 细节
3. 组合 + 依赖注入实战(订单结算,可直接跑):
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# ── 领域层:实体自带规则 ──
@dataclass
class Order:
    id: str
    prices: list = field(default_factory=list)
    status: str = "created"

    def total(self) -> int:                       # 业务规则在实体上
        return sum(self.prices)

    def cancel(self):
        if self.status == "paid":
            raise ValueError("paid order cannot cancel")
        self.status = "cancelled"

# ── 多态:支付方式可扩展,加一种 = 加一个类 ──
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: int) -> str: ...

class Alipay(PaymentMethod):
    def pay(self, amount): return f"alipay paid {amount}"

class WechatPay(PaymentMethod):
    def pay(self, amount): return f"wechat paid {amount}"

# ── 数据层:Repository 隔离存储 ──
class OrderRepo(ABC):
    @abstractmethod
    def save(self, order: Order): ...

class MemoryOrderRepo(OrderRepo):
    def __init__(self): self._db = {}
    def save(self, order): self._db[order.id] = order

# ── 业务层:Service 组合依赖(注入,不自己 new)──
class OrderService:
    def __init__(self, repo: OrderRepo, payment: PaymentMethod):
        self.repo = repo                  # 组合 + 注入:测试时可换假实现
        self.payment = payment

    def checkout(self, order: Order) -> str:
        amount = order.total()
        result = self.payment.pay(amount)  # 多态调用
        order.status = "paid"
        self.repo.save(order)
        return result

# ── 组装:入口决定具体实现 ──
svc = OrderService(MemoryOrderRepo(), Alipay())
order = Order("O1", [100, 200])
print(svc.checkout(order))        # alipay paid 300
```
4. 这样设计的架构收益
	1. 换支付:传 WechatPay,Service 一行不改(多态 + 注入)
	2. 换存储:MemoryOrderRepo -> SqlOrderRepo,业务不动(Repository 隔离)
	3. 好测试:注入假 Repo / 假 Payment,单测不碰 DB 和真实支付
	4. 规则内聚:total/cancel 长在 Order 上,改规则只动一处

**一句话原则**:类 = 数据 + 行为的内聚单元;封装定边界、抽象定契约、多态定扩展点、组合做装配。生产姿势:@dataclass 承载数据、ABC/Protocol 定义契约、依赖注入组装 -- 加功能 = 加一个类,不改老代码(开闭原则)。

### 7.标准库
###  8.网络编程
### 9.文件处理
