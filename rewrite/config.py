import os 
import yaml

_cfg = None

def load_config():
    global _cfg
    if _cfg is None:
        path = os.path.join(os.path.dirname(__file__),"config.yaml")
        with open(path,encoding = "utf-8") as f:
            _cfg = yaml.safe_load(f)
    return _cfg

def get(env = None):
    cfg = load_config()
    env = env or os.getenv("ENV",cfg.get("env","test"))
    return cfg["environments"][env]