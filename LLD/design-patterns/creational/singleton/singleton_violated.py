import time
from datetime import datetime

# DATABASE CONNECTION 
class DatabaseConnection:
    
    def __init__(self):
        print("\n[DB] Creating new database connection")
        print(f"[DB] Timestamp: {datetime.now().strftime('%H:%M:%S.%f')}")
        time.sleep(0.5) 
        
        self.connection_id = id(self)
        self.host = "localhost"
        self.port = 5432
        self.database = "myapp_db"
        
        print(f"[DB] Connection established (id={self.connection_id})")
    
    def query(self, sql):
        print(f"\n [DB:{self.connection_id}] Executing query")
        print(f"[DB] SQL: {sql}")
        return f"Result from connection {self.connection_id}"
    
    def close(self):
        print(f"\n[DB:{self.connection_id}] Closing connection")


# CONFIGURATION MANAGER 
class ConfigurationManager:
    def __init__(self):
        print("\n[Config] Loading configuration")
        print(f"[Config] Instance id={id(self)}")
        time.sleep(0.3)  
        
        self.config = {
            "app_name": "MyApp",
            "version": "1.0.0",
            "debug": False,
            "max_connections": 100
        }
        
        print("[Config] Configuration loaded")
    
    def get(self, key):
        return self.config.get(key)
    
    def set(self, key, value):
        print(f"\n[Config:{id(self)}] Setting {key}={value}")
        self.config[key] = value


# LOGGER 
class Logger:
    
    def __init__(self, log_file="app.log"):
        print("\n[Logger] Creating logger instance")
        print(f"[Logger] Instance id={id(self)}")
        print(f"[Logger] Log file={log_file}")
        
        self.log_file = log_file
        self.log_count = 0
    
    def log(self, level, message):
        self.log_count += 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(
            f"[{timestamp}] [{level}] {message} "
            f"(logger_id={id(self)}, count={self.log_count})"
        )


# USAGE 

print("=" * 70)
print("RESOURCE MANAGEMENT - WITHOUT SINGLETON PATTERN")
print("=" * 70)

print("\n" + "=" * 70)
print("PROBLEM 1: Multiple Database Connections")
print("=" * 70)

db1 = DatabaseConnection()
db2 = DatabaseConnection()
db3 = DatabaseConnection()

print("\n[WARN] Created 3 separate database connections")
print(f"db1 id={db1.connection_id}")
print(f"db2 id={db2.connection_id}")
print(f"db3 id={db3.connection_id}")
print("[ISSUE] Each connection has setup and memory overhead")

db1.query("SELECT * FROM users")
db2.query("SELECT * FROM products")

print("\n" + "=" * 70)
print("PROBLEM 2: Inconsistent Configuration State")
print("=" * 70)

config1 = ConfigurationManager()
config2 = ConfigurationManager()

print("\n[WARN] Created 2 configuration instances")
print(f"config1 id={id(config1)}")
print(f"config2 id={id(config2)}")

config1.set("debug", True)
print(f"config1.debug = {config1.get('debug')}")
print(f"config2.debug = {config2.get('debug')}")
print("[ISSUE] State is inconsistent across instances")

print("\n" + "=" * 70)
print("PROBLEM 3: Multiple Logger Instances")
print("=" * 70)

logger1 = Logger()
logger2 = Logger()
logger3 = Logger()

logger1.log("INFO", "Application started")
logger2.log("ERROR", "Database connection failed")
logger3.log("DEBUG", "Processing request")

print("\n[WARN] Created 3 logger instances")
print(f"logger1 count={logger1.log_count}")
print(f"logger2 count={logger2.log_count}")
print(f"logger3 count={logger3.log_count}")
print("[ISSUE] No centralized logging")


print("\n" + "=" * 70)
print("PROBLEM 5: No Global Access Point")
print("=" * 70)

def some_function():
    db = DatabaseConnection()
    db.query("SELECT * FROM orders")

def another_function():
    db = DatabaseConnection()
    db.query("SELECT * FROM customers")

some_function()
another_function()

print("\n[ISSUE] Each function creates its own connection")
print("[ISSUE] No shared, centralized instance")
