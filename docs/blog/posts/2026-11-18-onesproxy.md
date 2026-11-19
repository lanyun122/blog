---
date: 2026-11-18
categories:
  - 工具视频教程
slug: onesproxy-isp-3x-ui
tags:
  - 静态 ISP
  - OnesProxy
  - IP 检测
  - 3x-ui
  - 链式代理
---

# 🎁 # 静态 ISP 原理与实测｜OnesProxy 三地出口与 3x-ui 链式代理

![封面图](../../assets/images/photomode_01082023_035351.jpg){ style="display:block; width:900px; max-width:100%; height:auto; margin:24px auto 14px; border-radius:10px; box-shadow:0 6px 18px rgba(0,0,0,0.16);" }

<div style="margin: 0 0 25px; text-align: center;">
  <a href="https://youtu.be/hVe9xlYEATI?si=__QEIFCwzK_Z3rnF"
     target="_blank"
     rel="noopener noreferrer"
     class="md-button md-button--neutral"
     style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 24px; font-size: 0.85rem; border-radius: 20px; text-decoration: none; font-weight: bold; border: 1px solid rgba(0,0,0,0.1); transition: all 0.3s ease;">
    <span aria-hidden="true"
          style="display: inline-flex; align-items: center; justify-content: center; width: 1.4em; height: 1em; background-color: #ff0000; border-radius: 0.3em; flex: 0 0 auto;">
      <span style="display: block; width: 0; height: 0; margin-left: 0.08em; border-top: 0.27em solid transparent; border-bottom: 0.27em solid transparent; border-left: 0.44em solid #ffffff;"></span>
    </span>
    <span>立即观看完整视频</span>
  </a>
</div>


---

**本期要点** ｜ 讲清静态 ISP 的地址来源，以及它与机房 IP、家庭宽带住宅 IP 的区别。以 OnesProxy 的美国、香港、日本节点为例，演示购买流程，并用 IPinfo 和 ping0.cc 查看 IP 归属与风险标记。最后用 3x-ui 搭建 VLESS 节点、配置链式代理，核对实际出口，再测试 AI 服务、YouTube 和 TikTok 的访问情况。

<!-- more -->
---

## 🔗 相关链接

- **NodeMach 精品线路 VPS（CN2 GIA，含 IPv4 + /64 IPv6）：**[Chris 专属链接，购买与续费终身额外享 95 折](https://www.nodemach.com/welcome?vcd=9f2694fe)

- **OnesProxy 静态 ISP 代理** ｜ [通过我的推广链接注册可领取 9 折优惠券](https://app.onesproxy.com/channel_agent/track?invite_code=u900002035&user_source=1) ｜ 邀请码 `u900002035`

- **各价位VPS推荐：**[点击查看](https://lanyun122.github.io/blog/recommend/1-vps/)

- **TG交流群：**[点击加入](https://telegram.me/+BwyeTrhg9NQ5MjVl)

### 2. 3X-UI 一键部署命令

在 FinalShell 中复制并执行下面的命令：

固定安装 3X-UI v3.6.0（与本教程版本保持一致）
```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh) v3.6.0
```


## 🖥️ 远程连接工具

- **FinalShell：**[点击跳转](https://www.hostbuf.com/t/988.html)（支持 Windows、macOS、Linux）

## 📱 代理工具

- **Windows / macOS（Clash Verge Rev）：**[点击跳转](https://github.com/Clash-Verge-rev/clash-verge-rev/releases/latest)

- **v2rayN：** [GitHub Releases 下载最新版](https://github.com/2dust/v2rayN/releases/latest)

- **Android（NekoBox）：**[点击跳转](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases)

- **iOS / macOS（Shadowrocket）：**[点击跳转](https://apps.apple.com/us/app/shadowrocket/id932747118)

## 🔍 IP 工具

- **IP 检测工具：**
    - [Ping0](https://ping0.cc/)（查询当前网络 IP 地址类型）
    - [IP.NET](https://ip.net.coffee/)
    - [IPOK](https://ipok.io/)
    - [IPIPAI](https://ipipai.com/index-zh.html)

- **Speedtest 网络测速：**[点击测速](https://www.speedtest.net/)

- **顶级线路 VPS 推荐：**[点击跳转](https://lanyun122.github.io/blog/recommend/1-vps/)

### 日本、香港、美国常见宽带运营商 ASN

| 地区 | 运营商／网络 | ASN 示例 |
| --- | --- | --- |
| 日本 | OCN（NTT DOCOMO BUSINESS，原 NTT Communications） | `AS4713` |
| 日本 | KDDI | `AS2516` |
| 日本 | SoftBank | `AS17676` |
| 日本 | J:COM | `AS9824` |
| 香港 | HKT／Netvigator（网上行） | `AS4760` |
| 香港 | HKBN（香港宽频） | `AS9269`、`AS10103` |
| 香港 | HGC Global Communications（环球全域电讯） | `AS9304` |
| 美国 | Comcast／Xfinity | `AS7922` |
| 美国 | AT&T | `AS7018` |
| 美国 | Charter／Spectrum | `AS20115` |
| 美国 | Verizon | `AS701` |
| 美国 | Cox Communications | `AS22773` |

> 连上代理后，用 IPinfo 或 ping0.cc 查询实际出口 IP，再对照 ASN 和运营商名称。ASN 可以帮助识别这条 IP 的路由网络。是否属于家庭宽带出口，以及有没有风险记录，还要按具体 IP 核对。