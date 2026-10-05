---
date: 2026-09-24
categories:
  - 工具视频教程
slug: v2rayn-routing-ruleset
tags:
  - v2rayN
  - Xray
  - 分流规则
---

# 🎁 v2rayN 分流规则集完整搭建教程

![封面图](../../assets/images/2026-09-24-1.png){ style="display:block; width:900px; max-width:100%; height:auto; margin:24px auto 14px; border-radius:10px; box-shadow:0 6px 18px rgba(0,0,0,0.16);" }

<div style="margin: 0 0 25px; text-align: center;">
  <a href="[https://youtu.be/FxMdpwg5tNk?si=iSx3muaX5gT7vtkQ]" target="_blank" class="md-button md-button--neutral" style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 24px; font-size: 0.85rem; border-radius: 20px; text-decoration: none; font-weight: bold; border: 1px solid rgba(0,0,0,0.1); transition: all 0.3s ease;">
    <span aria-hidden="true" style="display: inline-flex; align-items: center; justify-content: center; width: 1.4em; height: 1em; background-color: #ff0000; border-radius: 0.3em; flex: 0 0 auto;">
      <span style="display: block; width: 0; height: 0; margin-left: 0.08em; border-top: 0.27em solid transparent; border-bottom: 0.27em solid transparent; border-left: 0.44em solid #ffffff;"></span>
    </span>
    <span>立即观看完整视频</span>
  </a>
</div>

---

**本期要点：** 从零搭建一套适合长期使用的 v2rayN 分流规则集，让局域网和国内流量直连，广告域名直接阻断，ChatGPT、Gemini 与流媒体统一使用美国住宅出口，交易所固定使用单独的香港节点，其余境外流量则交给当前代理节点。

<!-- more -->

## ⬇️ v2rayN 客户端官方下载

- **v2rayN：** [GitHub Releases 下载最新版](https://github.com/2dust/v2rayN/releases/latest)

## 🔗 本期相关服务推荐

### ⚡ 极速Cloud 机场推荐

这是我少有见到的精品线路机场。据商家线路说明，提供电信 **CN2 GIA**、联通 **AS9929/10099**、移动 **CMIN2** 等优化线路，在我的使用环境中整体表现不错。

它的套餐覆盖年付、季付、月付和新人体验套餐，价格也比较实惠。中秋活动期间还有 **8.8 折优惠**，具体优惠码为：`zqth`，适用套餐和有效期请以商家公告及结算页面为准。

邀请码：`zwTTkkF7`

👉 **[点击注册极速Cloud](https://191.101.132.80/#/register?code=yMetD7Ux)**



### 💻 搬瓦工 VPS 推荐

如果你更倾向于自己搭建节点，希望拥有独立服务器和更高的配置自由度，也可以选择搬瓦工 VPS。

[点击查看搬瓦工 VPS](https://bandwagonhost.com/aff.php?aff=82013)

### 🏳️ 静态住宅 IP

- 👉 **本期视频同款静态 IP（Webshare）：** [点击跳转](https://www.webshare.io/?referral_code=lq6qy4n0ui6c)

> 部分服务链接可能包含推广信息。是否购买请根据自己的实际需求决定，使用网络代理工具时也请遵守所在地法律法规及相关服务条款。

---

## 🆓 免费导入本期分流规则

本期使用的 v2rayN 分流规则集已经免费开源到 GitHub，项目主页提供规则地址及导入说明：

👉 **[点击进入 v2rayN Smart Routing 项目](https://github.com/lanyun122/v2rayN-Smart-Routing)**

进入项目后复制规则地址，在 v2rayN 的路由设置中通过订阅 URL 导入即可。

> ⭐ 这套规则可以直接免费使用，点亮 Star 并不是使用条件。如果项目确实帮助到了你，我想真诚地邀请你为项目点亮一个 **Star**。我希望参与 Codex 后续面向 GitHub 创作者的相关活动，你的支持对我非常重要；我也会继续免费维护和分享实用内容，期待和大家互相帮助、共同成长。

---

## 📌 本期教程要实现什么效果？

这期教程不是简单地让 v2rayN“能够联网”，而是搭建一套结构清晰、便于维护的分流规则集。

最终效果如下：

- 路由器、打印机、NAS 等局域网设备保持直连
- 常见广告和跟踪域名直接阻断
- ChatGPT 与 Gemini 使用美国策略组，并通过固定的美国住宅 IP 出口访问
- YouTube、Netflix、Disney+、HBO、Prime Video、Spotify、Twitch 等流媒体使用同一个美国策略组
- 交易所固定使用一个稳定的香港节点，避免出口 IP 频繁变化
- 国内域名和国内 IP 自动直连
- 其他没有命中特殊规则的流量，交给当前活动代理节点

整套流量路径可以简单理解为：

```text
局域网设备                 → direct
广告域名                   → block
ChatGPT / Gemini           → 美国策略组 → 美国住宅落地
YouTube / Netflix 等流媒体 → 美国策略组 → 美国住宅落地
交易所                     → 固定香港节点
国内网站和国内 IP          → direct
其他未分类流量             → proxy（当前活动节点）
```

本文以 v2rayN 7.x 为基础演示。不同小版本的按钮名称和界面位置可能略有差异，但规则的匹配逻辑基本相同。

---

# 第一部分：先理解规则的基本逻辑

## 一、`outboundTag` 是什么？

`outboundTag` 决定一条规则命中以后，流量应该从哪里出去。

### `direct`：直连

不经过代理节点，直接使用本地网络访问，适合国内网站、路由器后台、打印机、NAS 和其他局域网设备。

### `proxy`：当前代理

交给 v2rayN 主界面当前选中的活动节点，适合作为最后的兜底出口。切换主界面的活动节点以后，命中 `proxy` 的普通流量也会随之切换。

### `block`：阻断

直接拒绝对应请求，适合广告、跟踪域名以及明确不希望访问的目标。

需要注意，`block` 只能阻断相应网络请求，不能像浏览器广告扩展一样自动清理网页里的广告框、空白区域和弹窗。

### 指定节点或策略组

除了 `direct`、`proxy` 和 `block`，还可以点击“选择配置”，把流量交给某个固定节点或策略组。

本教程会使用：

```text
美国策略组   → ChatGPT、Gemini、流媒体
固定香港节点 → 交易所
```

---

## 二、Geosite 和 GeoIP 有什么区别？

Geosite 按照域名分类，例如：

```text
geosite:cn
geosite:private
geosite:openai
geosite:category-ads-all
```

GeoIP 按照目标 IP 分类，例如：

```text
geoip:cn
geoip:private
```

两者并不重复。例如打印机既可能通过 `printer.local` 访问，也可能直接通过 `192.168.1.100` 访问，因此局域网规则需要同时覆盖域名和 IP。

在 v2rayN 的同一个规则编辑窗口中，可以同时填写 Domain 和 IP。保存时 v2rayN 会生成对应的域名规则和 IP 规则，不需要在界面上手动拆成两条。

---

## 三、创建新的规则集

1. 打开 v2rayN 的“设置”。
2. 进入“路由设置”。
3. 新建一份规则集，或者复制一份现有规则集后再修改。
4. 建议命名为：

```text
V4-完整智能分流
```

5. 如果使用 Xray Core，将顶部“域名解析策略”设置为：

```text
IPIfNonMatch
```

它表示域名规则没有匹配时，再把域名解析为 IP，继续尝试 `geoip:cn` 等 IP 规则。

不要删除自带的默认规则集，出现问题时可以快速恢复。

---

## 四、规则顺序为什么重要？

v2rayN 会从上到下检查规则，命中第一条符合条件的规则后就停止继续匹配。

本教程最终采用下面的顺序：

| 排序 | 规则 | 出站方式 |
|---:|---|---|
| 1 | 局域网直连 | `direct` |
| 2 | UDP 443 阻断（可选） | `block` |
| 3 | 广告过滤 | `block` |
| 4 | GPT | 美国策略组 |
| 5 | Gemini | 美国策略组 |
| 6 | 流媒体 | 美国策略组 |
| 7 | 交易所 | 固定香港节点 |
| 8 | 国内直连 | `direct` |
| 9 | 最终代理 | `proxy` |

核心原则是：局域网优先保护，特殊服务使用指定出口，国内流量保持直连，最终代理必须放在最后。

---

# 第二部分：准备专用出口

## 五、准备美国策略组和住宅落地

ChatGPT、Gemini 和流媒体共用一个美国策略组，不需要创建三个重复的策略组。

推荐路径是：

```text
应用程序
  → 美国策略组自动选择一个可用的美国入口节点
  → 固定美国住宅落地节点
  → 目标网站
```

### 1. 准备住宅落地节点

先确保美国住宅代理已经作为可选择的配置存在，并设置一个唯一且容易识别的别名：

```text
美国住宅落地
```

### 2. 为美国入口节点设置落地代理

在用于 AI 和流媒体的订阅分组或配置分组中，将“落地代理别名”设置为：

```text
美国住宅落地
```

不同版本的 v2rayN 入口位置可能略有差异。如果看不到“落地代理别名”，请先确认当前 Core 和节点协议支持代理链。

### 3. 创建美国策略组

进入策略组设置后添加：

```text
别名：美国策略组
策略类型：最稳定 或 最低延迟
```

通过订阅别名或正则表达式筛选美国入口节点，例如：

```text
美国
```

“最低延迟”切换更积极；“最稳定”更适合希望减少入口变化的用户。无论选择哪个美国入口，最终都应通过固定的美国住宅落地访问目标网站。

> 仅把普通美国机房节点放进策略组，并不会自动变成住宅 IP。必须正确配置住宅落地，最终出口才会显示为住宅 IP。

---

## 六、准备固定香港交易所节点

交易所不建议使用会自动切换出口的最低延迟策略组。

频繁更换 IP、运营商或地区，可能触发异地登录提醒、二次验证、临时限制登录或交易、提现安全审核，以及 API IP 白名单失效。

因此建议选择一个长期稳定、出口位置一致的香港节点，并设置清晰别名：

```text
香港交易所专用
```

后面的交易所规则直接选择这个固定节点，而不是会自动切换的香港策略组。

> 固定节点只能减少出口变化，不能保证不会触发平台风控。登录、交易和提现前仍应核对出口 IP，并遵守交易所服务条款和当地规定。

---

# 第三部分：按照顺序逐条添加规则

除了特别说明的字段，其余 `port`、`protocol`、`inboundTag`、`network`、IP 和进程栏均保持空白。

## 七、规则 1：局域网直连

```text
别名：局域网直连
outboundTag：direct
```

Domain：

```text
geosite:private,domain:local,domain:lan
```

IP 或 IP CIDR：

```text
geoip:private,224.0.0.0/4,255.255.255.255/32,ff00::/8
```

这一个界面规则即可覆盖局域网域名、私有 IP、广播和组播流量，避免路由器、打印机、NAS 和设备发现请求绕到代理服务器。

---

## 八、规则 2：UDP 443 阻断（可选）

```text
别名：UDP 443阻断
outboundTag：block
port：443
network：udp
```

浏览器可能通过 UDP 443 使用 QUIC/HTTP/3。阻断后，浏览器通常会回退到 TCP 443，更容易按照普通代理规则处理。

这条规则不是所有用户都必须开启：

- 普通系统代理以及常见 TCP、VLESS、VMess、Trojan 场景，可以先保持开启。
- 如果开启 TUN，并且需要 QUIC、Hysteria2、TUIC 或其他 UDP 功能，应关闭后对比测试。
- 如果语音、视频、游戏或网页出现异常，也可以先临时关闭它排查。

如果决定启用，就应放在局域网直连之后、其他互联网规则之前；否则前面的流媒体域名规则可能会先命中，使 UDP 443 阻断失去作用。

---

## 九、规则 3：广告过滤

```text
别名：广告过滤
outboundTag：block
Domain：geosite:category-ads-all
```

这条规则主要用于阻断独立广告域名和跟踪域名。如果广告与网页正文共用一个域名，或者网站自己提供广告内容，单靠 v2rayN 无法精确删除广告元素。想清理网页中的广告框、空白区域和弹窗，仍建议搭配浏览器广告拦截扩展。

---

## 十、规则 4：GPT 使用美国策略组

```text
别名：GPT
outboundTag：选择配置 → 美国策略组
Domain：geosite:openai
```

不要把 `outboundTag` 误选成某个普通美国直连节点，否则它不会经过住宅落地。

---

## 十一、规则 5：Gemini 使用美国策略组

```text
别名：Gemini
outboundTag：选择配置 → 美国策略组
Domain：geosite:google-gemini
```

GPT 和 Gemini 虽然共用美国策略组，但保留两条独立规则更便于以后分别修改、暂停和排查。

---

## 十二、规则 6：流媒体使用美国策略组

```text
别名：流媒体
outboundTag：选择配置 → 美国策略组
```

Domain：

```text
geosite:youtube,geosite:netflix,geosite:disney,geosite:hbo,geosite:primevideo,geosite:spotify,geosite:twitch
```

输入框会把这些内容显示成一整段并自动换行，这是正常现象。只要使用英文逗号 `,` 分隔即可，不要改成中文逗号。

这条规则已经包含 YouTube，因此不需要再创建单独的“YouTube 专用”策略组和路由规则。

---

## 十三、规则 7：交易所固定使用香港节点

```text
别名：交易所
outboundTag：选择配置 → 香港交易所专用
Domain：geosite:category-cryptocurrency
```

`geosite:category-cryptocurrency` 是较宽泛的加密货币服务分类，除了交易所，也可能包含行情、钱包和其他相关网站。

如果只希望少数交易所走香港节点，可以改为手动填写对应域名，例如：

```text
domain:example-exchange.com,domain:example-exchange-cdn.com
```

不要为交易所选择自动切换的最低延迟策略组。固定香港节点能够尽量保持出口地区和 IP 稳定，降低因频繁变动触发安全验证的概率。

---

## 十四、规则 8：国内直连

```text
别名：国内直连
outboundTag：direct
```

Domain：

```text
geosite:cn
```

IP 或 IP CIDR：

```text
geoip:cn
```

域名和 IP 可以填写在同一个界面规则中，不需要拆成“国内域名直连”和“国内 IP 直连”两条。

由于 GPT、Gemini、流媒体和交易所都排在国内直连前面，即使某些服务使用了特殊 CDN，也会优先尝试命中相应的专用规则。

---

## 十五、规则 9：最终代理

```text
别名：最终代理
outboundTag：proxy
network：tcp,udp
```

Domain、IP、端口、协议、`inboundTag` 和进程全部留空。

“最终代理”是一条兜底规则：前面所有规则都没有命中时，剩余流量统一交给 v2rayN 主界面当前选中的活动节点。

例如 X、GitHub 或其他未单独分类的境外网站，通常会落到这条规则。它必须放在整个列表的最后，否则会提前接管流量，导致后面的规则失效。

---

## 十六、最终规则顺序核对

```text
1. 局域网直连     → direct
2. UDP 443阻断    → block（可选）
3. 广告过滤       → block
4. GPT            → 美国策略组
5. Gemini         → 美国策略组
6. 流媒体         → 美国策略组
7. 交易所         → 固定香港节点
8. 国内直连       → direct
9. 最终代理       → proxy
```

---

# 第四部分：应用并验证分流结果

## 十七、启用规则集

1. 保存内层规则和外层规则集。
2. 返回 v2rayN 主界面。
3. 将当前路由规则切换为 `V4-完整智能分流`。
4. 重启 v2rayN 服务。
5. 重新开启系统代理；只有确实需要全局接管时再使用 TUN。

普通系统代理只接管遵循 Windows 系统代理设置的软件。TUN 会接管更多 TCP 和 UDP 流量，但也更容易与游戏加速器、其他 VPN 和虚拟网卡发生冲突。

---

## 十八、最简单的出口验证方法

仅看到网站能够打开，并不能证明它使用了正确出口。可以通过临时添加 IP 查询网站的方法验证。

### 验证美国住宅出口

1. 在主界面选中一个非美国节点，例如日本节点。
2. 临时在 GPT 规则的 Domain 末尾添加：

```text
domain:ipinfo.io
```

3. 打开 `https://ipinfo.io`。
4. 页面应显示美国住宅出口，而不是主界面当前选择的日本节点。
5. 验证后删除 `domain:ipinfo.io`，避免以后查询出口时造成误判。

### 验证固定香港交易所出口

1. 临时在交易所规则的 Domain 末尾添加：

```text
domain:ip.sb
```

2. 打开 `https://ip.sb`。
3. 页面应显示固定香港节点的出口 IP。
4. 多次重启服务并复查，出口 IP 应保持一致。
5. 验证后删除临时测试域名。

访问另一个没有加入特殊规则的 IP 查询网站时，结果应显示主界面当前活动节点的出口，这说明“最终代理”正在生效。

---

## 十九、通过日志检查匹配结果

| 测试目标 | 预期出口 |
|---|---|
| 路由器、打印机、NAS | `direct` |
| 广告测试域名 | `block` |
| ChatGPT | 美国策略组 |
| Gemini | 美国策略组 |
| YouTube、Netflix 等 | 美国策略组 |
| 交易所 | 固定香港节点 |
| 国内网站 | `direct` |
| 普通境外网站 | `proxy` |

如果日志出现 `non existing outTag`、`existing tag` 等错误，通常说明规则引用的节点或策略组别名不存在、重复或已被修改。

---

# 第五部分：常见问题

## 1. GPT 或流媒体仍然显示机房 IP

这通常说明规则虽然选择了美国入口节点，但代理链没有正确连接到美国住宅落地。

重点检查：

- `outboundTag` 是否选择了“美国策略组”
- 美国入口节点所在分组是否设置了正确的“落地代理别名”
- 住宅落地节点别名是否唯一且仍然存在
- 住宅代理是否能够独立连接

## 2. 交易所出口 IP 会变化

检查交易所规则是否误选了策略组、负载均衡组或会自动切换的配置。

交易所规则应直接指向一个固定香港节点。节点发生故障时，建议先手动确认新节点的地区和出口 IP，再修改规则，不要让程序在多个出口之间自动跳转。

## 3. 国内网站仍然走代理

可能原因包括：

- “最终代理”排在国内直连之前
- 顶部域名解析策略没有设置为 `IPIfNonMatch`
- 网站使用了未收录的境外 CDN
- 当前请求没有经过这套 v2rayN 规则
- Geosite 或 GeoIP 数据无法读取

可以先查看日志，再决定是否需要手动补充具体域名。

## 4. 广告过滤后网站打不开

可以暂时关闭“广告过滤”进行对比，查看日志中的被阻断域名，再为误伤的正常域名单独创建一条更靠前的 `direct` 或指定代理规则。

## 5. 网页仍显示广告框或弹窗

v2rayN 只负责阻断网络请求，不负责修改网页布局。如果广告内容与正文共用域名，或者广告框已经写在网页 HTML 中，路由规则无法把它从页面上删除，需要配合浏览器广告拦截扩展处理。

## 6. 与游戏加速器发生冲突

普通“系统代理”模式下，大多数游戏不会经过 v2rayN，通常可以与游戏加速器共存。

如果同时开启 v2rayN TUN 和游戏加速器，两者可能争抢路由或虚拟网卡，导致重复代理、延迟升高、掉线或语音异常。最简单的处理方式是：

```text
v2rayN：保持系统代理开启
v2rayN TUN：关闭
游戏流量：交给游戏加速器
```

## 7. 修改规则后没有变化

依次检查：

1. 是否保存了内层规则和外层规则集。
2. 主界面是否选中了正确的规则集。
3. 是否重启了 v2rayN 服务。
4. 浏览器是否仍然复用了旧连接。
5. 规则引用的节点和策略组别名是否存在。
6. 日志中是否存在 Geosite、GeoIP 或 Core 配置错误。

---

## 📚 官方参考文档

- [v2rayN GitHub 项目](https://github.com/2dust/v2rayN)
- [v2rayN 官方 Wiki](https://github.com/2dust/v2rayN/wiki)
- [v2rayN 自定义路由规则说明](https://github.com/2dust/v2rayN/wiki/Description-of-custom-routing-rules)
- [v2rayN 代理链说明](https://github.com/2dust/v2rayN/wiki/Description-of-proxy-chain)
- [Xray 路由规则说明](https://xtls.github.io/config/routing.html)
- [Domain List Community](https://github.com/v2fly/domain-list-community)
- [GeoIP for V2Ray](https://github.com/v2fly/geoip)

---

## ✅ 总结

这套规则的重点不是数量多，而是职责清晰：

```text
局域网流量优先直连
广告域名直接阻断
AI 和流媒体共用美国策略组及住宅落地
交易所固定使用单独香港节点
国内流量保持直连
其余流量由最终代理兜底
```

配置完成后，应当通过日志和临时 IP 查询规则分别验证每一种出口。尤其是交易所，不要把“延迟最低”等同于“最适合长期使用”，出口稳定性通常比自动切换更重要。

## ⚠️ 免责声明

本文内容仅供技术交流，请遵守当地法律法规及相关服务条款。涉及账户、交易和资金安全时，请自行核对节点出口、平台政策与风险。
