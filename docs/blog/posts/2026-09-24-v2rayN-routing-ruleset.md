---
date: 2026-09-02
categories:
  - 工具视频教程
slug: clash-verge-rev
tags:
  - Clash Verge Rev
  - Mihomo
  - 网络工具
---

# 🎁 [Clash Verge Rev 完整教程] 

![封面图](../../assets/images/photomode_01082023_035351.jpg){ width="300" align=left style="border-radius: 8px; margin-right: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;" }

**本期要点：** [本期从订阅链接导入和节点选择开始，讲解规则、全局、直连模式以及系统代理与 TUN 的区别，并演示链式代理的配置方法和常见连接问题排查，适合从 Clash for Windows 迁移到 Clash Verge Rev 的新手参考。]。

<div style="margin-top: 25px; text-align: center;">
  <a href="[https://youtu.be/UvU213ebRQE?si=VoNFW8z99aY81oWC]" target="_blank" class="md-button md-button--neutral" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 24px; font-size: 0.85rem; border-radius: 20px; text-decoration: none; font-weight: bold; border: 1px solid rgba(0,0,0,0.1); transition: all 0.3s ease;">
    <svg viewBox="0 0 576 512" style="height: 1.1em; fill: #FF0000; margin: 0; display: block;"><path d="M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.781 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z"/></svg>
    立即观看完整视频
  </a>
</div>

<br clear="left">
<!-- more -->

# 🎁 [v2rayN 分流规则集完整搭建教程]

## ⬇️ v2rayN 客户端官方下载

- **v2rayN：** [GitHub Releases 下载最新版](https://github.com/2dust/v2rayN/releases/latest)

## ⬇️ Clash Verge Rev 与 Shadowrocket 官方下载

- **Clash Verge：** [GitHub Releases 下载最新版](https://github.com/clash-verge-rev/clash-verge-rev/releases/latest)
- **Shadowrocket：** [Apple App Store 官方下载](https://apps.apple.com/us/app/shadowrocket/id932747118)

## 🔗 本期相关服务推荐

### 🚀 视频同款良心云机场

博主折腾互联网和各类网络工具多年，这款是我实际体验过的同类型机场中，目前价格最低的一档，同时节点速度表现也相当不错，比较适合预算有限、流量需求较大的用户。

邀请码：`zwTTkkF7`

[点击查看视频同款机场](https://xn--9kqz23b19z.com/#/register?code=zwTTkkF7)

### 💻 搬瓦工 VPS 推荐

如果你更倾向于自己搭建节点，希望拥有独立服务器和更高的配置自由度，也可以选择搬瓦工 VPS。

[点击查看搬瓦工 VPS](https://bandwagonhost.com/aff.php?aff=82013)

### 🏳️ 静态住宅 IP

- 👉 **本期视频同款静态 IP（Webshare）：** [点击跳转](https://www.webshare.io/?referral_code=lq6qy4n0ui6c)

> 部分服务链接可能包含推广信息。是否购买请根据自己的实际需求决定，使用网络代理工具时也请遵守所在地法律法规及相关服务条款。

---

## 📌 本期教程要实现什么效果？

这期教程不只是让 v2rayN 简单地“能联网”，而是搭建一套相对完整、可以长期使用的分流规则集。

最终实现的基础分流架构包括：

- 国内网站和国内 IP 自动直连
- 国外网站默认通过代理节点访问
- 常见广告域名直接拦截
- 局域网设备和私有地址保持直连
- AI 网站使用单独的专用节点
- YouTube、Netflix 等流媒体使用指定节点
- 支持策略组、最低延迟和故障切换
- 支持通过 GitHub 地址一键导入整套规则

<!-- 将下面的图片路径替换成第一张“基础架构与定制规则”图片的实际路径 -->

![v2rayN 分流规则集架构](../../assets/images/v2rayn-routing-overview.png)

本文以 v2rayN 7.x 为基础进行演示。不同小版本的按钮名称和界面位置可能略有区别，但规则的搭建逻辑基本相同。

---

# 第一部分：搭建基础分流架构

## 一、先理解 v2rayN 的三个出站方式

在创建路由规则时，最重要的设置是 `outboundTag`，也就是匹配到这条规则以后，流量应该从哪里出去。

### `direct`：直连

流量不经过代理节点，直接使用本地网络访问。

适合：

- 国内网站
- 国内 IP
- 局域网设备
- 路由器后台
- 打印机、NAS 等本地设备

### `proxy`：代理

流量交给当前选择的代理节点或策略组处理。

适合：

- 国外网站
- Google、YouTube
- AI 工具
- 境外流媒体服务

### `block`：阻断

匹配到的网络请求会被直接拒绝，不再连接目标服务器。

适合：

- 广告域名
- 跟踪域名
- 明确不希望联网的程序或网站

需要注意，`block` 只能阻止对应域名或 IP 的网络请求，并不等于浏览器广告插件。

如果广告和网页正文使用同一个域名，或者广告直接由网站自己的服务器提供，那么单纯依靠路由规则可能无法拦截。

---

## 二、Geosite 和 GeoIP 是什么？

如果国内直连规则需要手动填写几千个网站，肯定会出现遗漏，所以实际搭建时通常不会逐个填写网站。

v2rayN 可以使用两类规则数据库：

### Geosite

按照域名进行分类。

例如：

```text
geosite:cn
geosite:private
geosite:category-ads-all
```

其中：

- `geosite:cn`：常见中国大陆域名集合
- `geosite:private`：局域网和私有域名
- `geosite:category-ads-all`：广告和跟踪域名集合

### GeoIP

按照目标服务器的 IP 地址进行分类。

例如：

```text
geoip:cn
geoip:private
```

其中：

- `geoip:cn`：中国大陆 IP 地址段
- `geoip:private`：局域网和私有 IP 地址段

域名规则和 IP 规则配合使用，可以明显减少国内网站被错误分配到代理节点的情况。

---

## 三、更新规则数据库

开始创建规则前，建议先在 v2rayN 中检查更新：

1. 打开 v2rayN。
2. 找到“检查更新”。
3. 更新 `Geo files`、`Geosite`、`GeoIP` 或相关规则文件。
4. 更新完成后重启 v2rayN 服务。

如果这些文件长期没有更新，一些新网站、新域名和新 IP 地址段可能无法被正确识别。

---

## 四、进入路由设置

在 v2rayN 主界面中：

1. 打开“设置”。
2. 进入“路由设置”。
3. 建议先复制一份现有规则集。
4. 将新规则集命名为：

```text
V4-完整分流
```

不要直接删除默认规则集。保留一份默认配置，出现问题时更容易恢复。

---

## 五、规则顺序非常重要

v2rayN 的路由规则按照从上到下的顺序匹配。

一旦前面的规则成功匹配，后面的规则就不会继续执行。

推荐顺序如下：

| 排序 | 规则 | 出站方式 |
|---:|---|---|
| 1 | 自定义专用规则 | 指定策略组 |
| 2 | 广告拦截 | `block` |
| 3 | 局域网域名 | `direct` |
| 4 | 局域网 IP | `direct` |
| 5 | 中国大陆域名 | `direct` |
| 6 | 中国大陆 IP | `direct` |
| 7 | 最终兜底规则 | `proxy` |

专用的 AI、YouTube 和流媒体规则应该放在国内直连及最终代理规则之前。

---

## 六、创建广告拦截规则

点击“添加规则”，填写：

```text
别名：广告拦截
outboundTag：block
Domain：geosite:category-ads-all
```

其他项目保持为空，然后保存。

这条规则会阻止规则数据库中收录的广告和跟踪域名联网。

### 为什么有些广告依然会显示？

常见原因包括：

- 广告域名没有被规则集收录
- 广告与网页正文使用同一个域名
- 广告内容已经被浏览器缓存
- 浏览器使用了独立代理或加密 DNS
- 网站使用第一方广告接口
- 当前请求没有经过 v2rayN

因此，v2rayN 的广告规则更适合拦截独立广告域名。如果希望清理网页中的广告框、空白区域和弹窗，建议同时安装浏览器广告拦截扩展。

---

## 七、创建局域网直连规则

### 1. 局域网域名直连

```text
别名：绕过局域网域名
outboundTag：direct
Domain：geosite:private
```

### 2. 局域网 IP 直连

```text
别名：绕过局域网IP
outboundTag：direct
IP 或 IP CIDR：geoip:private
```

这两条规则可以避免访问以下设备时绕到代理服务器：

- 路由器后台
- NAS
- 局域网共享文件
- 打印机
- 家庭服务器
- 本地开发环境

如果存在特殊局域网网段，也可以手动补充：

```text
192.168.0.0/16
10.0.0.0/8
172.16.0.0/12
127.0.0.0/8
```

---

## 八、创建国内直连规则

### 1. 中国大陆域名直连

```text
别名：国内域名直连
outboundTag：direct
Domain：geosite:cn
```

### 2. 中国大陆 IP 直连

```text
别名：中国大陆IP直连
outboundTag：direct
IP 或 IP CIDR：geoip:cn
```

这两条规则搭配使用，可以覆盖绝大部分国内网站和国内服务器。

如果个别国内网站仍然走代理，可以在日志中找到它实际访问的域名，然后手动添加：

```text
domain:example.com
```

`domain:` 会匹配该域名及其子域名。

---

## 九、创建国外代理兜底规则

最后添加一条兜底规则：

```text
别名：最终代理
outboundTag：proxy
port：0-65535
```

不要填写 Domain 和 IP。

这条规则的含义是：前面的规则全部没有匹配时，剩余流量统一通过代理节点访问。

必须把它放在整个规则列表的最下面。

如果把“最终代理”放到前面，它会提前接管所有流量，后面的国内直连规则将不再生效。

---

# 第二部分：定制策略组和专用分流规则

基础规则解决的是“国内直连、国外代理”，但实际使用中，我们通常还希望不同网站使用不同节点。

例如：

- ChatGPT、Claude 使用美国节点
- YouTube 使用高速节点
- Netflix 使用已经解锁流媒体的节点
- 普通国外网站继续使用当前默认节点

这就需要将“策略组”和“路由规则”组合起来。

---

## 十、创建 AI 专用策略组

进入 v2rayN 的策略组设置，点击“添加”。

建议填写：

```text
别名：AI专用
策略类型：最低延迟或最稳定
```

然后通过以下两种方式添加节点：

### 方法一：使用订阅别名筛选

如果订阅中的节点名称比较规范，可以填写正则表达式筛选美国节点：

```text
(?i)(美国|美國|US|USA|United States)
```

`(?i)` 表示忽略英文字母大小写。

### 方法二：手动选择节点

也可以在“子配置项”中手动选择几个稳定的美国节点。

建议至少选择两个节点，避免单一节点失效后整个 AI 策略组无法使用。

需要注意：

- Xray 和 sing-box 支持的策略组类型存在区别。
- 策略组内的节点需要被当前使用的 Core 支持。
- 频繁切换国家、地区或网络类型，可能触发部分 AI 服务的安全验证。
- 专用节点只能改善出口一致性，不能保证绕过服务商的风控或地区限制。

---

## 十一、创建 AI 专用分流规则

返回路由设置，添加一条新规则：

```text
别名：AI专用
outboundTag：选择配置 → AI专用
```

在 Domain 中填写：

```text
domain:openai.com,
domain:chatgpt.com,
domain:oaistatic.com,
domain:oaiusercontent.com,
domain:anthropic.com,
domain:claude.ai,
domain:gemini.google.com,
domain:generativelanguage.googleapis.com,
domain:perplexity.ai
```

保存以后，将这条规则移动到“国内直连”和“最终代理”之前。

如果某个 AI 服务登录时仍然没有使用 AI 专用节点，可以打开 v2rayN 日志，查看实际连接的域名，再补充到这条规则中。

---

## 十二、创建 YouTube 专用策略组

添加第二个策略组：

```text
别名：油管专用
策略类型：最低延迟
```

可以筛选香港、日本、新加坡或美国节点：

```text
(?i)(香港|HK|日本|JP|新加坡|SG|美国|US)
```

具体使用哪个地区，需要根据节点速度、YouTube 解锁情况以及实际观看内容决定。

然后创建路由规则：

```text
别名：YouTube专用
outboundTag：选择配置 → 油管专用
Domain：geosite:youtube
```

如果当前 Geosite 数据库没有对应分类，可以使用域名规则：

```text
domain:youtube.com,
domain:youtu.be,
domain:googlevideo.com,
domain:ytimg.com,
domain:youtubei.googleapis.com
```

---

## 十三、创建流媒体专用策略组

继续添加策略组：

```text
别名：流媒体专用
策略类型：最低延迟或最稳定
```

选择已经解锁 Netflix、Disney+、Spotify 等服务的节点。

然后添加路由规则：

```text
别名：流媒体专用
outboundTag：选择配置 → 流媒体专用
```

Domain 可以填写：

```text
geosite:netflix,
geosite:disney,
geosite:spotify
```

如果想将 YouTube 也并入这个策略组，可以额外加入：

```text
geosite:youtube
```

如果已经单独创建了“油管专用”规则，就不要在这里重复添加 YouTube，以免发生规则冲突。

---

## 十四、最终推荐排序

完整规则集建议按照下面的顺序排列：

```text
1. AI专用
2. YouTube专用
3. 流媒体专用
4. 广告拦截
5. 绕过局域网域名
6. 绕过局域网IP
7. 国内域名直连
8. 中国大陆IP直连
9. 最终代理
```

核心原则是：

```text
越具体的规则越靠前
越宽泛的规则越靠后
最终兜底规则必须放在最后
```

---

# 第三部分：应用规则并检查是否生效

## 十五、选择刚刚创建的规则集

保存路由设置以后：

1. 返回 v2rayN 主界面。
2. 将当前路由规则切换为 `V4-完整分流`。
3. 重新启动服务。
4. 重新开启系统代理或 TUN 模式。

如果使用普通系统代理，只有遵循系统代理设置的软件会进入 v2rayN。

如果希望游戏客户端、Microsoft Store 应用以及不读取系统代理的软件也参与分流，可以考虑使用 TUN 模式。

---

## 十六、通过日志检查实际出口

不要只通过“网页能不能打开”判断规则是否生效。

建议打开 v2rayN 的实时日志，然后依次测试：

### 国内网站

打开国内网站，日志中应该匹配：

```text
direct
```

### 国外网站

打开普通国外网站，日志中应该匹配：

```text
proxy
```

### AI 服务

打开 ChatGPT、Claude 或 Gemini，日志中应该匹配：

```text
AI专用
```

### YouTube

播放一段 YouTube 视频，日志中应该匹配：

```text
油管专用
```

### 局域网设备

打开路由器或 NAS 后台，日志中应该匹配：

```text
direct
```

---

## 十七、常见问题

### 1. 国内网站仍然走代理

可能原因：

- `geosite:cn` 和 `geoip:cn` 没有更新
- “最终代理”排在国内规则前面
- 网站实际使用了未收录的境外 CDN 域名
- 浏览器没有经过当前 v2rayN 实例
- DNS 解析结果与预期不一致

可以先查看日志，再把实际域名添加到“国内域名直连”规则中。

### 2. 国外网站被错误直连

检查是否存在范围过大的 `direct` 规则，尤其是：

- 过于宽泛的域名关键字
- 错误填写的 IP CIDR
- 国内直连规则排序过高或内容不正确

### 3. 修改规则后没有变化

尝试：

1. 保存规则集。
2. 确认已经选中正确的规则集。
3. 重启 v2rayN 服务。
4. 关闭浏览器后重新打开。
5. 清除 DNS 缓存。
6. 再次查看实时日志。

如果使用已经生成的策略组或负载均衡配置，修改路由规则后，可能还需要重新生成对应配置，才能读取最新规则。

### 4. 广告拦截后网站打不开

说明网站的正常接口可能被广告规则误伤。

可以：

- 暂时关闭“广告拦截”规则进行对比
- 查看日志中的被阻断域名
- 给正常域名单独添加一条更靠前的 `direct` 或 `proxy` 规则
- 将误伤情况反馈给对应规则集维护者

---

# 第四部分：一键导入我的 GitHub 分流规则集

如果你不想按照上面的步骤逐条创建规则，也可以直接使用我整理好的 v2rayN 分流规则集。

这套规则已经包含：

- 国内域名和 IP 直连
- 国外流量默认代理
- 广告域名拦截
- 局域网地址直连
- AI 服务专用分流
- YouTube 和流媒体分流
- 最终代理兜底规则

## 📦 GitHub 项目地址

> 请将下面的地址替换成你的真实 GitHub 仓库。

[点击查看我的 v2rayN 分流规则集](https://github.com/你的GitHub用户名/你的仓库名)

## 🔗 规则订阅地址

```text
https://raw.githubusercontent.com/你的GitHub用户名/你的仓库名/main/v2rayN-routing.json
```

## ⚡ 从订阅 URL 一键导入

1. 复制上面的规则订阅地址。
2. 打开 v2rayN。
3. 进入“设置” → “路由设置”。
4. 点击“从订阅 URL 导入规则”。
5. 粘贴规则订阅地址。
6. 等待规则下载完成。
7. 保存并选择新导入的规则集。
8. 重启 v2rayN 服务。

## 📋 从剪贴板导入

如果 GitHub Raw 地址暂时无法访问，也可以：

1. 打开 GitHub 中的规则文件。
2. 点击 `Raw（查看原始文件）`。
3. 复制全部 JSON 内容。
4. 回到 v2rayN 路由设置。
5. 点击“从剪贴板导入规则”。
6. 保存并启用导入的规则集。

## 📁 从文件导入

还可以下载规则文件，然后在路由设置中选择：

```text
从文件中导入规则
```

选择下载好的 JSON 文件即可。

> 导入前建议保留原来的默认规则集。不同用户使用的节点名称和策略组别名可能不同，导入后请重点检查 `AI专用`、`油管专用`和`流媒体专用`对应的配置是否存在。

---

## 📚 官方参考文档

- [v2rayN GitHub 项目](https://github.com/2dust/v2rayN)
- [v2rayN 官方 Wiki](https://github.com/2dust/v2rayN/wiki)
- [v2rayN 自定义路由规则说明](https://github.com/2dust/v2rayN/wiki/Description-of-custom-routing-rules)
- [Xray 路由规则说明](https://xtls.github.io/config/routing.html)
- [Domain List Community](https://github.com/v2fly/domain-list-community)
- [GeoIP for V2Ray](https://github.com/v2fly/geoip)

---

## ✅ 总结

一套实用的 v2rayN 分流规则并不需要手动收集成千上万个网站。

只要正确组合：

```text
Geosite 域名分类
+
GeoIP 地址分类
+
自定义专用域名
+
策略组
+
正确的规则顺序
```

就可以实现国内直连、国外代理、广告拦截、局域网直连，以及 AI、YouTube、流媒体分别使用专用节点。

搭建完成后，最重要的不是“规则越多越好”，而是定期查看日志、更新规则数据库，并根据自己的实际使用情况补充和调整。


## ⚠️ 免责声明
* 本文内容仅供技术交流，请遵守当地法律法规。