
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
**定义**:类 = 数据(属性)+ 行为(方法)的封装单元,是"模板";实例 = 按模板创建的具体对象。核心价值:相关数据和操作绑定、边界清晰、职责单一,是模块化架构的原子。
四大理念:**封装、继承、多态、抽象**。

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

### 10.进程和线程
**定义**:进程 = 资源分配单位(独立内存空间,互不共享);线程 = CPU 调度单位(同一进程内共享内存)。Python 关键约束:**GIL**(全局解释器锁)使同一时刻仅一个线程执行 Python 字节码 --> 核心推论:**CPU 密集用多进程,IO 密集用多线程/异步**。并发(交替处理任务)≠ 并行(多核同时执行)。

#### 10.1 选型(最重要的决策,先做这一步)
| 任务类型 | 特征 | 方案 |
|---|---|---|
| IO 密集 | 网络请求/读写文件/DB,大部分时间在**等** | ThreadPoolExecutor / asyncio |
| CPU 密集 | 计算/加密/解析,大部分时间在**算** | ProcessPoolExecutor(绕开 GIL) |

1. 判断方法:去掉网络和磁盘,纯计算快不快?快 = IO 密集;慢 = CPU 密集

#### 10.2 线程(threading)-- IO 密集
1. 基本用法
```python
import threading

def worker(n):
    print(f"thread {n} running")

t = threading.Thread(target=worker, args=(1,))
t.start()          # 启动,不阻塞
t.join()           # 等它结束
```
2. 线程安全:共享可变状态必须加锁
```python
import threading

counter = 0
lock = threading.Lock()

def inc():
    global counter
    with lock:                 # 不加锁,count += 1 会丢更新(非原子)
        counter += 1
```
3. 线程间通信:queue.Queue(自带锁,生产首选,别裸传共享变量)
```python
from queue import Queue

q = Queue(maxsize=100)
q.put(item)          # 生产者;队列满自动阻塞(天然限流)
item = q.get()       # 消费者;队列空自动等待
q.task_done()        # 处理完标记
```
4. 生产首选:线程池(池化复用 + 限并发,别裸建线程)
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

urls = [f"https://api.x.com/{i}" for i in range(20)]

def fetch(url):
    ...                       # requests.get(url) 之类 IO

with ThreadPoolExecutor(max_workers=8) as pool:
    futures = {pool.submit(fetch, u): u for u in urls}
    for f in as_completed(futures):
        try:
            data = f.result()          # 子任务异常在这里抛
        except Exception as e:
            print(f"{futures[f]} failed: {e}")
```

#### 10.3 进程(multiprocessing)-- CPU 密集
1. 生产首选:进程池(concurrent.futures 统一接口,和线程池同款 API)
```python
from concurrent.futures import ProcessPoolExecutor
import os

def heavy(n: int) -> int:              # 纯计算,CPU 密集
    return sum(i * i for i in range(n))

if __name__ == "__main__":             # 必须!见下条
    nums = [10_000_000] * os.cpu_count()
    with ProcessPoolExecutor() as pool:        # 默认 worker = cpu_count
        total = sum(pool.map(heavy, nums))     # 每个任务独立进程,绕开 GIL
    print(total)
```
2. `if __name__ == "__main__"` 必写:macOS/Windows 默认 spawn 启动(重新 import 主模块),没有守护会无限递归拉起进程直接崩
3. 进程间不共享内存:参数/返回值靠 pickle 序列化传递 --> **别传大对象**(序列化开销可能比计算还贵),传文件路径/ID

#### 10.4 asyncio(高并发 IO 的现代方案,入门一句话)
1. 单线程事件循环:`await` = 主动让出控制权,等 IO 时切换到别的任务;万级并发 IO 才需要它,常规几十并发用线程池即可
```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(0.5)           # 模拟 IO;await = 让出控制权
    return f"done {url}"

async def main():
    urls = [f"u{i}" for i in range(10)]
    results = await asyncio.gather(*[fetch(u) for u in urls])   # 并发执行
    print(results)

asyncio.run(main())
```
2. 容错版:`asyncio.gather(*tasks, return_exceptions=True)` 收集异常而非整体失败

#### 10.5 生产最佳实践
1. **先选型再动手**:IO -> 线程池/asyncio;CPU -> 进程池(见 10.1)
2. 用 `concurrent.futures` 的池,别裸 Thread/Process:池管理生命周期 + 限流 + 复用
3. 池大小:CPU 密集 = `os.cpu_count()`;IO 密集经验值 8~64(过大反而拖垮对端/本机)
4. 线程共享可变状态必须 Lock;更好的设计是**无共享**--用 Queue 传消息
5. multiprocessing 入口必须 `if __name__ == "__main__"`(macOS/Windows)
6. `f.result()` 才会抛子任务异常 -- 只 submit 不取结果 = 异常被吞、失败无感知
7. 池用 `with`(结束自动 shutdown);长生命周期服务记得优雅关闭
8. `daemon=True` 线程随主进程退出,只用于可随时中断的辅助任务
9. 一切等待设超时:`f.result(timeout=30)` / `asyncio.wait_for(coro, 30)`,防卡死
10. 子进程参数要可 pickle;大对象传路径不传数据

#### 10.6 业务结合设计
1. 业务模式:批量调 API/拉数据(IO -> 线程池)、批量计算/解析/加密(CPU -> 进程池);池在 Service 层做批量编排,结果交 Repository 落库,失败接异常体系(重试/日志,见 6.4 与 5.异常)
2. 实战:批量调 API(线程池 + 限并发 + 单点失败不影响整体)
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import random, time

def call_api(uid: int) -> dict:
    time.sleep(random.uniform(0.2, 0.5))          # 模拟网络 IO
    if random.random() < 0.1:
        raise ConnectionError(f"uid {uid} failed")
    return {"uid": uid, "ok": True}

def batch_call(users: list, max_workers: int = 8):
    """批量调 API:池限并发,单个失败跳过并收集,部分成功"""
    results, errors = [], []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(call_api, u): u for u in users}
        for f in as_completed(futures):
            try:
                results.append(f.result())
            except Exception as e:
                errors.append({"uid": futures[f], "error": str(e)})
    return results, errors
```
3. 实战:CPU 密集并行(进程池)= 10.3 的 heavy 例子,N 核约 N 倍加速
4. 架构收益量化:100 个请求串行 ~35s -> 8 并发 ~5s;8 核计算并行 ~8x
5. **一句话原则**:先问 IO 还是 CPU -> 上池(Executor) -> 取结果拿异常(result) -> 设并发上限(max_workers) -- 并发四件套:选型、池化、容错、限流。
### 10.进程和线程

