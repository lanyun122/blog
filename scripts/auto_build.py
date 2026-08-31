import os
import json
import urllib.request
import urllib.error
import re
from datetime import datetime

# ==========================================
# 1. 节点原料大厂 (十万百万级池子同时抓取)
# ==========================================
NODE_SOURCES = [
    "https://raw.githubusercontent.com/XHAO05/freevpn/main/all.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt",
    "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/vfreefly/vfreefly/main/sub",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/yokingma/clash_node/master/all.txt",
    "https://raw.githubusercontent.com/Jetyu/V2Ray-Subscribe/master/V2Ray.txt"
]

POSTS_DIR = "docs/nodes/posts"
PASSWORD_FILE = "scripts/passwords.json"
MAX_NODES = 150  # 升级为150个精选节点

def get_today_password(date_str):
    """读取当天密码，如果没预设，默认用 MMDD"""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
            pwd_dict = json.load(f)
            return pwd_dict.get(date_str, date_str[5:].replace("-", ""))
    return date_str[5:].replace("-", "")

def fetch_from_url(url):
    """带超时和备用代理的下载程序"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 尝试直连，如果失败或被墙，自动尝试使用 CDN 镜像网关转接
    urls_to_try = [url]
    if "raw.githubusercontent.com" in url:
        urls_to_try.append(url.replace("https://raw.githubusercontent.com/", "https://ghproxy.net/https://raw.githubusercontent.com/"))
        urls_to_try.append(url.replace("https://raw.githubusercontent.com/", "https://fastly.jsdelivr.net/gh/"))

    for u in urls_to_try:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception:
            continue
    return ""

def fetch_and_clean_nodes():
    """去十大源进货并智能过滤"""
    print("⏳ 正在派出八爪鱼爬虫，前往全球十大节点源疯狂进货...")
    all_raw_lines = []
    
    for idx, url in enumerate(NODE_SOURCES, 1):
        print(f"  └─ [{idx}/{len(NODE_SOURCES)}] 正在抓取: {url.split('/')[3]} ...")
        content = fetch_from_url(url)
        if content:
            all_raw_lines.extend(content.strip().split('\n'))
            
    print(f"📦 累计抓取原始数据 {len(all_raw_lines)} 条，正在清洗过滤去重...")
    
    # 过滤出纯正的节点协议，去重
    valid_nodes = set()
    valid_prefixes = ('vmess://', 'vless://', 'trojan://', 'ss://', 'ssr://', 'hysteria2://', 'hy2://')
    
    for line in all_raw_lines:
        line = line.strip()
        # 1. 必须是合法协议开头
        if any(line.lower().startswith(proto) for proto in valid_prefixes):
            # 2. 简单过滤明显的死节点、广告节点或本地环回节点
            if "127.0.0.1" in line or "localhost" in line or len(line) < 25:
                continue
            valid_nodes.add(line)
            
    sorted_nodes = list(valid_nodes)
    print(f"💎 清洗完毕！共获得优质精选节点 {len(sorted_nodes)} 个！")
    
    # 截取前 MAX_NODES 个，排成文本
    if not sorted_nodes:
        return "vless://error-fetching-nodes@127.0.0.1:443#请确认你的网络是否畅通后重试"
    return "\n".join(sorted_nodes[:MAX_NODES])

def generate_markdown():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    today_cn = now.strftime("%Y年%m月%d日")
    
    password = get_today_password(today_str)
    nodes_text = fetch_and_clean_nodes()
    
    # 确保保存文章的路径存在
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    # 构建高转化 Markdown 文章模板
    md_content = f"""---
date: {today_str}
categories:
  - 免费节点
---

# 【免费节点】{today_cn}精选高速翻墙节点分享 | 4K秒开 | 每日更新密码解锁

> **⚠️ 使用须知与重要提醒：**
> 为防止爬虫批量抓取、保障真正粉丝的节点使用体验与速度，本站**不提供长期订阅链接**。
> 所有免费节点均为**独立单节点（时效 24~48 小时）**，每日定时更替。请务必观看**今日 YouTube 视频**获取专属解密密码！

<!-- more -->

---

## 一、 🚀 稳定机场与自建节点 VPS 推荐（省心翻墙首选）

如果你厌倦了每天寻找免费节点、忍受不稳定和限速，强烈推荐使用以下博主长期精选的高速 VPS 与优质专线。无论是自己搭建节点还是直接用机场，均支持 4K/8K 秒开：

* **【白月光专线机场】：** 极速稳定的精选专线，全节点解锁 ChatGPT 与流媒体。
  [👉 点击前往注册试用](https://www.sibker.com/register?invite_code=AL2a9oZV)
* **【搬瓦工 BandwagonHost】：** 传家宝级高端 VPS，极其适合自建稳定不翻车的强力翻墙节点！
  [👉 点击这里直达抢购](https://bandwagonhost.com/aff.php?aff=82013)
* **【华纳云 HNCloud】：** 高性价比免备案云服务器，延迟稳如泰山。结账输入优惠码 `10%OFF` 立享 **9 折**。
  [👉 点击领取优惠上车](https://www.hncloud.com/light_cloud.html?k=AJBOVJ)
* **【JTTI 极速服务器】：** 优质专线网络，抗风控与解锁能力极强。
  [👉 点击前往选购套餐](https://www.jtti.cc/zh/light_cloud.html?k=KBZNYL)
* **【VMISS】：** 低至十几元每月的优质 BGP 线路 VPS，多号运营与自建极具性价比。
  [👉 点击这里立省发车](https://app.vmiss.com/aff.php?aff=5292)

---

## 二、 🏠 纯净住宅 IP 与防封节点资源（跨境避坑神器）

做跨境电商、TikTok 运营或 Web3 多号防封，最核心的就是要有**纯净的美国/海外原生家庭宽带 IP**，别再使用公用廉价节点导致封号：

* **【Webshare】：** 全网极致性价比的静态住宅 IP，月付低至 4.8 元，深评测绝对不过期！
  [👉 点击领取优惠注册](https://www.webshare.io/?referral_code=lq6gy4n0ui6c)
* **【Talor 住宅代理】：** 高纯净度住宅代理平台，业务成功率极高。注册时填写博主邀请码 `as5pidqk` 享受专属福利。
  [👉 点击前往直达后台](https://dashboard.talordata.com/reg?inviter_code=as5pidqk)

---

## 三、 💳 **国际虚拟卡申请教程：**

  [▶️ Bybit U卡（台湾）](https://partner.bybit.com/b/148332)　[▶️ Bybit U卡（哈萨克斯坦）](https://partner.bybit.com/b/148332)

  
---

## 四、 🎬 奈飞 / Disney+ / AI 工具独立账号合租

买得起节点，但看不起几百块一年的流媒体官方会员？使用平台发车，花几块钱直接上车顶流 AI 和影音综合平台：

## 🏆 账号星球 (Chris节约时间推荐)

* **📝 平台简介：** 一个综合性的海外账号与数字服务交易平台。如果你不想在基础的注册环节浪费太多精力，这里可以作为你的“出海补给站”。
* **🛒 核心业务：** **TG (Telegram) 电报账号**
  * **ChatGPT / Gemini 等各类热门 AI 工具成品号及订阅代充**
  * 海外各区 Apple ID (美区/港区/日区等)
  * Google 账号、Gmail 邮箱、微软账号
  * 常见社媒成品账号 (Twitter/X、Facebook、Instagram 等)
* **💰 折扣福利：** 🎁 **点击下方链接直达平台后，记得先领取 5 元专属优惠券再下单！**
* **🔗 官方选购通道：** [👉 点击直达账号星球 (Chris专属推荐) ↗](https://accboy7chris.acceboy.com)

---


## 🚌 环球巴士 · 借个号（短期会员租赁推荐）

如果只是偶尔看一部剧、临时使用 AI 工具，单独购买 Netflix、YouTube、ChatGPT 等长期会员，不但价格高，很多时候账号还会闲置。

环球巴士的 **“借个号”** 业务主打按需短租：需要时再借，用完即停，不必为了几天的使用需求购买整月甚至整年的会员。

- **🎫 按需短租：** 追剧、写论文或临时使用某项工具时，可以根据商品选择短期租赁，减少长期订阅产生的闲置费用。
- **🧰 类型丰富：** 覆盖影视、音乐、AI 工具和设计软件等类别；官网目前展示 Netflix、YouTube、Spotify、ChatGPT、Adobe PS＋LR 等服务。
- **🔄 一个会员灵活切换：** 不需要分别订阅多个平台，可根据自己的需求借用不同账号。
- **👥 支持多个同时借用：** 白银、黄金和钻石会员分别支持同时借用 1 个、2 个和 3 个账号。
- **💰 入门成本较低：** 月付会员目前最低 ¥29.99 起，更适合使用频率不固定、但偶尔需要高价会员服务的用户。
- **💡 支持提交心愿：** 如果暂时没有想要的平台，可以提交产品名称，需求较高的服务可能优先采购上架。
- **🛡️ 提供售后规则：** 根据官方协议，首次租用后 24 小时内可以申请首单退款；充值、礼品卡和兑换码等特殊商品除外，具体条件请查看官方规则。

> 官网展示的账号种类和实际库存可能随时调整，购买前建议先确认租期、设备数量、地区限制和使用规则。共享账号不建议保存个人隐私、支付信息或重要文件。

- **🎁 专属优惠：** 下单时填写优惠码 `lanyun`，首单享 **9 折优惠**
- **🔗 官方邀请链接：** [点击进入环球巴士](https://universalbus.cn?s=fpoRdmZCPZ)

> **推广说明：** 本链接属于邀请推广链接，通过该链接购买可能会为本站带来一定推广收益，还会降低你的购买价格。请根据自己的实际需求理性选择。


---

## 五、 📱 跨境硬件与 eSIM 神器

做跨境运营、注册各类海外高风险账号（如 Telegram、美区 Apple ID、TikTok 等），海外手机卡是刚需！

这里为你推荐kitesim的两款神卡，两款神卡的核心属性对比：
## 💡 两款神卡核心属性对比

| 核心维度 | 🇭🇰 香港带号漫游流量卡（主推） | 🍁 KiteSim 加拿大保号卡 |
| :--- | :--- | :--- |
| **月租/价格** | **低至 $0.56 / GB**（0月租，长周期流量包） | **$0.1 美元 / 月**（几乎白嫖，网页直接接码） |
| **核心功能** | 国内免 VPN 翻墙、带有香港实体号码 | 海外短信接码、注册账号、长期保号 |
| **网络漫游** | 漫游直接绕过 GFW，开数据即上外网 | 适合在国内长期待机接短信 |
| **AI 解锁能力** | **直接解锁 ChatGPT、Gemini 等 AI** | 仅作为号码使用（不含大流量） |
| **最适合人群** | 经常出差旅游、厌倦梯子、重度 AI 依赖者 | 需要批量养号、绑定银行/交易所/APP 的用户 |
| **购买链接** | [立即抢购香港漫游卡](https://h5.kitesim.co/register/?invite=CSZHOC) | [立即申请加拿大神卡](https://h5.kitesim.co/register/?invite=CSZHOC)  |

---
* **【Xesim 写卡器】—— 终极黑科技，让你的普通国产手机秒变支持全球 eSIM 的手机！**
  * **博主专属连接：** [👉 点击前往官网查看与选购](https://xesim.cc/?DIST=RkdHGlk%3D)
  * **专属九折优惠码：** 结算时输入 `KX13bx` 即享全单 **9 折**优惠！

---

## 🔥 加入 Chris Talk 专属交流社区

> 💡 **搭建节点遇到疑难杂症？翻墙或者跨境防封碰到坑？**
> 欢迎直接点击加入我们的 Telegram 粉丝群，与各位大佬一起交流探讨！
> [👉 点击立即加入 Telegram 交流群](https://t.me/+BwyeTrhg9NQ5MjVl)

---

## 三、 🎁 {today_cn}免费节点限时领取区

!!! warning "节点有效提示"
    * 下方节点为单节点分享，不支持导入订阅，请点击“一键复制”后在客户端（v2rayN / 小火箭 / Clash / Mihomo）中选择 **“从剪贴板导入”**。
    * **今日专属密码**已经公布在今日的 YouTube 视频画面或置顶评论中！

<div id="lock-screen" style="margin-top: 25px; padding: 30px; background: linear-gradient(145deg, #181818, #222222); text-align: center; border-radius: 12px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
  <div style="font-size: 3rem; margin-bottom: 10px;">🔒</div>
  <h3 style="color: #ffffff; margin-top: 0;">今日免费节点已加密保护</h3>
  <p style="color: #aaa; margin-bottom: 20px; font-size: 0.9rem;">输入今日 YouTube 视频中的专属密码即可解锁全部优质高带宽节点：</p>
  
  <div style="display: flex; justify-content: center; gap: 10px; max-width: 350px; margin: 0 auto;">
    <input type="password" id="node-pwd" placeholder="请输入今日视频密码" style="flex: 1; padding: 12px 16px; border-radius: 6px; border: 1px solid #555; background: #000; color: #fff; font-size: 1rem; text-align: center; outline: none;">
    <button onclick="checkPwd()" style="padding: 12px 20px; background-color: #00c853; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: background 0.2s;">解锁 ⚡</button>
  </div>
  <p id="error-msg" style="color: #ff5252; font-size: 0.85rem; margin-top: 15px; display: none;">❌ 密码错误，请前往今日 YouTube 视频获取正确密码！</p>
</div>

<div id="secret-nodes" style="display:none; margin-top: 25px; padding: 25px; background: #111111; border-top: 4px solid #00c853; border-radius: 8px; box-shadow: 0 5px 20px rgba(0,0,0,0.3);">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 10px;">
    <h3 style="color: #00c853; margin: 0;">🎉 解锁成功！请在 24 小时内导入使用：</h3>
    <button onclick="copyAllNodes()" id="copy-btn" style="padding: 8px 16px; background: #24A1DE; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.85rem;">📋 一键复制全部节点</button>
  </div>
  
  <p style="color: #888; font-size: 0.8rem; margin-bottom: 10px;">💡 操作提示：点击上方蓝色按钮复制全部内容，然后打开客户端按 <kbd>Ctrl</kbd> + <kbd>V</kbd>（手机端点击从剪贴板添加）即可！</p>

  <textarea id="node-list" readonly style="width: 100%; height: 280px; background: #000000; color: #00e676; padding: 15px; border-radius: 6px; border: 1px solid #333; font-family: monospace; font-size: 0.85rem; line-height: 1.5; resize: vertical; outline: none;">{nodes_text}</textarea>
</div>

<script>
function checkPwd() {{
  var inputPwd = document.getElementById('node-pwd').value.trim();
  var correctPwd = '{password}'; 
  
  if(inputPwd === correctPwd) {{
    document.getElementById('secret-nodes').style.display = 'block';
    document.getElementById('lock-screen').style.display = 'none';
  }} else {{
    var errorMsg = document.getElementById('error-msg');
    errorMsg.style.display = 'block';
    document.getElementById('node-pwd').style.borderColor = '#ff5252';
    setTimeout(function(){{ errorMsg.style.display = 'none'; document.getElementById('node-pwd').style.borderColor = '#555'; }}, 3000);
  }}
}}

document.getElementById('node-pwd').addEventListener('keypress', function (e) {{
    if (e.key === 'Enter') {{ checkPwd(); }}
}});

function copyAllNodes() {{
  var nodeText = document.getElementById('node-list');
  nodeText.select();
  nodeText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(nodeText.value).then(function() {{
    var btn = document.getElementById('copy-btn');
    var originalText = btn.innerHTML;
    btn.innerHTML = '✅ 复制成功！快去导入吧';
    btn.style.backgroundColor = '#00c853';
    setTimeout(function() {{
      btn.innerHTML = originalText;
      btn.style.backgroundColor = '#24A1DE';
    }}, 2500);
  }});
}}
</script>
"""
    
    file_path = os.path.join(POSTS_DIR, f"{today_str}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ 成功生成今日文章: {file_path}")
    print(f"🔑 今日专属解密密码已设定为: 【 {password} 】")

if __name__ == "__main__":
    generate_markdown()