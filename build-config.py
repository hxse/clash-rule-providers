#!/usr/bin/env python3
# coding: utf-8
import requests
from pathlib import Path
import yaml
from yaml import CSafeLoader as Loader, CSafeDumper as Dumper


def set_udp(path="./profiles/proxies"):
    for i in Path(path).glob("*.yaml"):
        with open(i, "r", encoding="utf8") as f:
            data = yaml.load(f, Loader=Loader)
            for item in data["proxies"]:
                item["udp"] = True
        with open(i, "w", encoding="utf8") as f:
            yaml.dump(data, f, allow_unicode=True, Dumper=Dumper)


set_udp()

with open("config.custom.yaml", "r", encoding="utf8") as f:
    custom_data = yaml.load(f, Loader=Loader)

with open("config.template.yaml", "r", encoding="utf8") as f:
    template_data = yaml.load(f, Loader=Loader)
    template_providers = template_data["proxy-providers"]
    custom_providers = custom_data["proxy-providers"]
    for template_name in template_providers:
        template_item = template_providers[template_name]
        if template_item["type"] == "file":
            continue
        custom_item = custom_providers[template_name]

        for custom_k, custom_v in custom_item.items():
            template_item[custom_k] = custom_v

    fields = [
        "mixed-port",
        "allow-lan",
        "mode",
        "log-level",
        "external-controller",
        "dns",
        "tun",
        "proxies",
        "rules",
    ]
    assert "rules" in custom_data, "请定义rules字段"
    for i in fields:
        if i in template_data and i in custom_data:
            template_data[i] = custom_data[i]

with open("config.yaml", "w", encoding="utf8") as f:
    yaml.dump(template_data, f, allow_unicode=True, Dumper=Dumper)


def reload_config(path, url="http://127.0.0.1:9090/configs"):
    requests.put(url, json={"path": path})


def get_rules(url="http://127.0.0.1:9090/rules"):
    return requests.get(url)


def connections(name, url="http://127.0.0.1:9090/connections"):
    return requests.delete(url + f"/{name}")


def all_connections(mode, url="http://127.0.0.1:9090/connections"):
    if mode == "get":
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    if mode == "delete":
        requests.delete(url)


configPath = Path("config.yaml").absolute()
reload_config(configPath.as_posix())
print("已重载配置", configPath)
all_connections("delete")
print("已清空连接")
