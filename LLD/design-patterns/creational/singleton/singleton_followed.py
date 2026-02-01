import time
import threading
from datetime import datetime

# BASIC SINGLETON (Double-Checked Locking)
class DatabaseConnection:

    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("\n[DB] Creating singleton database connection")
                    print(f"[DB] Timestamp: {datetime.now().strftime('%H:%M:%S.%f')}")
                    time.sleep(0.5)  
                    
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        else:
            print("\n[DB] Reusing existing database connection")
        
        return cls._instance
    
    def _initialize(self):
        self.connection_id = id(self)
        self.host = "localhost"
        self.port = 5432
        self.database = "myapp_db"
        self.query_count = 0
        
        print(f"[DB] Connection ready (id={self.connection_id})")
    
    def query(self, sql):
        self.query_count += 1
        print(f"\n[DB:{self.connection_id}] Executing query #{self.query_count}")
        print(f"[DB] SQL: {sql}")
        return f"Result from connection {self.connection_id}"
    
    def get_stats(self):
        return {
            "connection_id": self.connection_id,
            "query_count": self.query_count,
            "host": self.host,
            "database": self.database
        }
    
    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None


# METACLASS SINGLETON
class SingletonMeta(type):

    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigurationManager(metaclass=SingletonMeta):
    
    _init_lock= threading.Lock()

    def __init__(self):
        with self._init_lock:
            if not hasattr(self, "_initialized"):
                print("\n[Config] Loading configuration")
                print(f"[Config] Instance id={id(self)}")
                time.sleep(0.3)
                
                self.config = {
                    "app_name": "MyApp",
                    "version": "1.0.0",
                    "debug": False,
                    "max_connections": 100
                }
                
                self._initialized = True
                print("[Config] Configuration loaded")
            else:
                print("\n[Config] Reusing configuration instance")
    
    def get(self, key):
        return self.config.get(key)
    
    def set(self, key, value):
        print(f"[Config:{id(self)}] Set {key}={value}")
        self.config[key] = value
    
    def get_all(self):
        return self.config.copy()


# DECORATOR SINGLETON
def singleton(cls):
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Logger:
    
    def __init__(self, log_file="app.log"):
        print("\n[Logger] Creating singleton logger")
        print(f"[Logger] Instance id={id(self)}")
        print(f"[Logger] Log file={log_file}")
        
        self.log_file = log_file
        self.log_count = 0
        self.logs = []
    
    def log(self, level, message):
        self.log_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(entry)
        print(f"{entry} (logger_id={id(self)}, count={self.log_count})")
    
    def get_stats(self):
        return {
            "instance_id": id(self),
            "total_logs": self.log_count,
            "log_file": self.log_file
        }


def test_thread_safety():
    print("\n" + "=" * 70)
    print("THREAD SAFETY TEST")
    print("=" * 70)
    
    instances = []
    
    def create_instance(thread_id):
        print(f"[Thread-{thread_id}] Requesting DB connection")
        db = DatabaseConnection()
        instances.append(id(db))
        db.query(f"Query from thread {thread_id}")
    
    threads = []
    for i in range(20):
        t = threading.Thread(target=create_instance, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    unique_ids = set(instances)
    # print("lenght====",len(instances)) the length will affect if you not join threads before because by deafut threads are Non-Daemon.

    print("\n[Result]")
    for i, instance_id in enumerate(instances):
        print(f"Thread-{i} -> instance_id={instance_id}")
    
    if len(unique_ids) == 1:
        print("[OK] All threads received the same instance")
    else:
        print("[ERROR] Multiple instances detected:", unique_ids)


# USAGE

print("=" * 70)
print("RESOURCE MANAGEMENT - WITH SINGLETON PATTERN")
print("=" * 70)

# Database
print("\n" + "=" * 70)
print("DATABASE CONNECTION")
print("=" * 70)

db1 = DatabaseConnection()
# db1= None
db2 = DatabaseConnection()
db3 = DatabaseConnection()

print(f"\nSame instance: {db1 is db2 is db3}")

db1.query("SELECT * FROM users")
db2.query("SELECT * FROM products")
db3.query("SELECT * FROM orders")

print("\nDB stats:", db1.get_stats())

# Configuration
print("\n" + "=" * 70)
print("CONFIGURATION MANAGER")
print("=" * 70)

config1 = ConfigurationManager()
config2 = ConfigurationManager()
# print(ConfigurationManager._instances)

print(f"\nSame instance: {config1 is config2}")

config1.set("debug", True)
config1.set("max_connections", 200)

print("config1.debug =", config1.get("debug"))
print("config2.debug =", config2.get("debug"))

# Logger
print("\n" + "=" * 70)
print("LOGGER")
print("=" * 70)

logger1 = Logger()
logger2 = Logger()
logger3 = Logger()

# print("Logger Class type==",type(Logger))
# print("ConfigurationManager Class type==",type(ConfigurationManager))

print(f"\nSame instance: {logger1 is logger2 is logger3}")

logger1.log("INFO", "Application started")
logger2.log("ERROR", "Database connection failed")
logger3.log("DEBUG", "Processing request")

print("\nLogger stats:", logger1.get_stats())

# Thread safety
test_thread_safety()
