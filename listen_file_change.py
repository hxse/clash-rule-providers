#!/usr/bin/python
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from build import run_build_config
from pathlib import Path

lastTime = 0


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global lastTime
        nowTime = int(time.time())  # 秒级时间戳
        try:
            if nowTime - lastTime > 1:
                lastTime = int(time.time())
                print(nowTime, lastTime)
                print(f"event type: {event.event_type}  path : {event.src_path}")
                if event.src_path.endswith("config.custom.yaml"):
                    p = Path(event.src_path)
                    run_build_config(p.resolve())
                    time.sleep(3)
                    print("refresh", "config.custom.yaml")
        except AttributeError as e:  # 会出莫名其妙的bug,建议放弃监听,用手动build
            print(e, 233)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
