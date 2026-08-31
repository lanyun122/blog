import base64
import concurrent.futures
import hashlib
import html
import ipaddress
import json
import os
import re
import socket
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass, field
from datetime import datetime

try:
    import yaml
except ImportError:  # 本地只运行脚本、尚未安装 MkDocs 依赖时仍可处理 URI/Base64 源
    yaml = None

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
MAX_NODES = 40
MIN_NODES = 10
MAX_SOURCE_BYTES = 8 * 1024 * 1024
MAX_NODES_PER_SOURCE = 180
MAX_PROBE_CANDIDATES = 600
FETCH_WORKERS = 6
PROBE_WORKERS = 48
PROBE_TIMEOUT_SECONDS = 3.0
PROBE_ATTEMPTS = 2

URI_SCHEMES = ("vmess", "vless", "trojan", "ss", "hysteria2", "hy2")
TCP_SCHEMES = {"vmess", "vless", "trojan", "ss"}
URI_PATTERN = re.compile(
    rf"(?i)(?:{'|'.join(URI_SCHEMES)})://[^\s<>\"']+"
)
TRUTHY_VALUES = {"1", "true", "yes", "on"}
LEGACY_SS_CIPHERS = {
    "aes-128-cfb", "aes-192-cfb", "aes-256-cfb", "aes-128-ctr",
    "aes-192-ctr", "aes-256-ctr", "rc4-md5", "chacha20", "salsa20",
}


@dataclass
class FetchResult:
    index: int
    source_url: str
    content: str = ""
    used_url: str = ""
    errors: list[str] = field(default_factory=list)


@dataclass
class NodeCandidate:
    uri: str
    scheme: str
    host: str
    port: int
    identity: str
    signature: str
    sources: set[str] = field(default_factory=set)
    successful_probes: int = 0
    latency_ms: float = float("inf")
    resolved_ip: str = ""
    probe_error: str = ""

    @property
    def dedupe_key(self):
        return self.scheme, self.host.lower(), self.port, self.identity, self.signature

def get_today_password(date_str):
    """读取当天密码，如果没预设，默认用 MMDD"""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
            pwd_dict = json.load(f)
            return pwd_dict.get(date_str, date_str[5:].replace("-", ""))
    return date_str[5:].replace("-", "")

def _decode_base64_bytes(value):
    value = re.sub(r"\s+", "", value)
    if not value:
        raise ValueError("empty base64 value")
    value += "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value.encode("ascii"))


def _decode_base64_text(value):
    return _decode_base64_bytes(value).decode("utf-8-sig")


def _format_host(host):
    return f"[{host}]" if ":" in host and not host.startswith("[") else host


def _github_raw_fallbacks(url):
    """生成 raw.githubusercontent.com 的可用备用地址。"""
    urls = [url]
    parsed = urllib.parse.urlsplit(url)
    if parsed.hostname != "raw.githubusercontent.com":
        return urls

    parts = parsed.path.lstrip("/").split("/")
    if len(parts) >= 4:
        owner, repo, ref = parts[:3]
        file_path = "/".join(parts[3:])
        jsdelivr = (
            "https://fastly.jsdelivr.net/gh/"
            f"{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}@"
            f"{urllib.parse.quote(ref)}/{urllib.parse.quote(file_path, safe='/')}"
        )
        urls.append(jsdelivr)
    urls.append(f"https://ghproxy.net/{url}")
    return urls


def fetch_from_url(index, url):
    """限量下载单个来源；直连失败后尝试正确格式的 GitHub CDN 地址。"""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ChrisTalkNodeBuilder/2.0)",
        "Accept": "text/plain, application/yaml, */*",
        "Accept-Encoding": "identity",
    }
    result = FetchResult(index=index, source_url=url)

    for candidate_url in _github_raw_fallbacks(url):
        for attempt in range(2):
            try:
                req = urllib.request.Request(candidate_url, headers=headers)
                with urllib.request.urlopen(req, timeout=12) as response:
                    payload = response.read(MAX_SOURCE_BYTES + 1)
                if len(payload) > MAX_SOURCE_BYTES:
                    raise ValueError(f"响应超过 {MAX_SOURCE_BYTES // 1024 // 1024} MiB 限制")
                if not payload.strip():
                    raise ValueError("响应为空")
                try:
                    result.content = payload.decode("utf-8-sig")
                except UnicodeDecodeError:
                    result.content = payload.decode("utf-8", errors="replace")
                result.used_url = candidate_url
                return result
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, ValueError) as exc:
                result.errors.append(f"{candidate_url}: {type(exc).__name__}: {str(exc)[:160]}")
                if attempt == 0:
                    time.sleep(0.25)
    return result


def _transport_query(proxy):
    params = {}
    network = str(proxy.get("network") or "tcp").lower()
    params["type"] = network

    server_name = proxy.get("servername") or proxy.get("sni")
    if server_name:
        params["sni"] = str(server_name)
    if proxy.get("client-fingerprint"):
        params["fp"] = str(proxy["client-fingerprint"])
    if proxy.get("flow"):
        params["flow"] = str(proxy["flow"])

    reality = proxy.get("reality-opts") or {}
    if reality:
        params["security"] = "reality"
        if reality.get("public-key"):
            params["pbk"] = str(reality["public-key"])
        if reality.get("short-id"):
            params["sid"] = str(reality["short-id"])
    elif proxy.get("tls"):
        params["security"] = "tls"
    else:
        params["security"] = "none"

    if proxy.get("skip-cert-verify"):
        params["insecure"] = "1"

    if network == "ws":
        ws_opts = proxy.get("ws-opts") or {}
        if ws_opts.get("path"):
            params["path"] = str(ws_opts["path"])
        headers = ws_opts.get("headers") or {}
        host_header = headers.get("Host") or headers.get("host")
        if host_header:
            params["host"] = str(host_header)
    elif network == "grpc":
        grpc_opts = proxy.get("grpc-opts") or {}
        service_name = grpc_opts.get("grpc-service-name") or grpc_opts.get("service-name")
        if service_name:
            params["serviceName"] = str(service_name)
    elif network == "http":
        http_opts = proxy.get("http-opts") or {}
        if http_opts.get("path"):
            path_value = http_opts["path"]
            params["path"] = str(path_value[0] if isinstance(path_value, list) else path_value)

    return params


def _clash_proxy_to_uri(proxy):
    """把常见 Clash 节点安全转换为分享 URI；未知或依赖插件的类型直接跳过。"""
    if not isinstance(proxy, dict):
        return None
    scheme = str(proxy.get("type") or "").lower()
    server = str(proxy.get("server") or "").strip()
    name = str(proxy.get("name") or scheme or "node")
    try:
        port = int(proxy.get("port"))
    except (TypeError, ValueError):
        return None
    if not server or not (1 <= port <= 65535):
        return None

    endpoint = f"{_format_host(server)}:{port}"
    fragment = urllib.parse.quote(name, safe="")

    if scheme == "vmess":
        ws_opts = proxy.get("ws-opts") or {}
        grpc_opts = proxy.get("grpc-opts") or {}
        headers = ws_opts.get("headers") or {}
        config = {
            "v": "2",
            "ps": name,
            "add": server,
            "port": str(port),
            "id": str(proxy.get("uuid") or ""),
            "aid": str(proxy.get("alterId") or 0),
            "scy": str(proxy.get("cipher") or "auto"),
            "net": str(proxy.get("network") or "tcp"),
            "type": "none",
            "host": str(headers.get("Host") or headers.get("host") or ""),
            "path": str(
                ws_opts.get("path")
                or grpc_opts.get("grpc-service-name")
                or grpc_opts.get("service-name")
                or ""
            ),
            "tls": "tls" if proxy.get("tls") else "",
            "sni": str(proxy.get("servername") or proxy.get("sni") or ""),
            "fp": str(proxy.get("client-fingerprint") or ""),
            "allowInsecure": "1" if proxy.get("skip-cert-verify") else "0",
        }
        encoded = base64.b64encode(
            json.dumps(config, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).decode("ascii")
        return f"vmess://{encoded}"

    if scheme == "vless":
        user_id = str(proxy.get("uuid") or "").strip()
        params = {"encryption": "none", **_transport_query(proxy)}
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return f"vless://{urllib.parse.quote(user_id, safe='')}@{endpoint}?{query}#{fragment}"

    if scheme == "trojan":
        password = str(proxy.get("password") or "")
        params = _transport_query(proxy)
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return f"trojan://{urllib.parse.quote(password, safe='')}@{endpoint}?{query}#{fragment}"

    if scheme == "ss" and not proxy.get("plugin"):
        method = str(proxy.get("cipher") or "")
        password = str(proxy.get("password") or "")
        user_info = base64.urlsafe_b64encode(f"{method}:{password}".encode("utf-8")).decode("ascii").rstrip("=")
        return f"ss://{user_info}@{endpoint}#{fragment}"

    if scheme in {"hysteria2", "hy2"}:
        password = str(proxy.get("password") or proxy.get("auth") or "")
        params = {}
        if proxy.get("sni"):
            params["sni"] = str(proxy["sni"])
        if proxy.get("skip-cert-verify"):
            params["insecure"] = "1"
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        suffix = f"?{query}" if query else ""
        return f"hysteria2://{urllib.parse.quote(password, safe='')}@{endpoint}{suffix}#{fragment}"

    return None


def extract_node_uris(content):
    """同时识别明文分享链接、整体 Base64 订阅和 Clash YAML。"""
    found = [match.group(0).rstrip(",;") for match in URI_PATTERN.finditer(content)]

    compact = re.sub(r"\s+", "", content.strip())
    if not found and len(compact) >= 32 and re.fullmatch(r"[A-Za-z0-9_+/=-]+", compact):
        try:
            decoded = _decode_base64_text(compact)
            if len(decoded.encode("utf-8")) <= MAX_SOURCE_BYTES:
                found.extend(match.group(0).rstrip(",;") for match in URI_PATTERN.finditer(decoded))
        except (ValueError, UnicodeDecodeError, UnicodeEncodeError):
            pass

    if yaml is not None and re.search(r"(?m)^proxies\s*:\s*$", content):
        try:
            document = yaml.safe_load(content)
            proxies = document.get("proxies", []) if isinstance(document, dict) else []
            for proxy in proxies:
                uri = _clash_proxy_to_uri(proxy)
                if uri:
                    found.append(uri)
        except yaml.YAMLError as exc:
            print(f"    ⚠️ Clash YAML 解析失败: {str(exc).splitlines()[0][:160]}")

    # 保留上游顺序，同时去掉同一来源中的逐字重复项。
    return list(dict.fromkeys(found))


def _valid_public_host(host):
    if not host or len(host) > 253 or re.search(r"[\s<>\x00-\x1f]", host):
        return False
    normalized = host.rstrip(".").lower()
    if normalized == "localhost" or normalized.endswith(".local"):
        return False
    try:
        return ipaddress.ip_address(normalized).is_global
    except ValueError:
        try:
            normalized.encode("idna")
        except UnicodeError:
            return False
        return "." in normalized and all(normalized.split("."))


def _query_dict(query):
    return {
        key.lower(): value
        for key, value in urllib.parse.parse_qsl(query, keep_blank_values=True)
    }


def _contains_insecure_flag(values):
    return any(
        values.get(key, "").strip().lower() in TRUTHY_VALUES
        for key in ("insecure", "allowinsecure", "skip-cert-verify")
    )


def _parse_ss_uri(uri):
    main = uri[5:].split("#", 1)[0]
    main, _, query = main.partition("?")
    if "plugin=" in query.lower():
        return None

    try:
        if "@" in main:
            user_part, endpoint = main.rsplit("@", 1)
            try:
                credentials = _decode_base64_text(user_part)
            except (ValueError, UnicodeDecodeError, UnicodeEncodeError):
                credentials = urllib.parse.unquote(user_part)
        else:
            decoded = _decode_base64_text(main)
            credentials, endpoint = decoded.rsplit("@", 1)

        if ":" not in credentials:
            return None
        method, password = credentials.split(":", 1)
        endpoint_parts = urllib.parse.urlsplit(f"//{endpoint}")
        host = endpoint_parts.hostname or ""
        port = endpoint_parts.port
    except (ValueError, UnicodeDecodeError, UnicodeEncodeError):
        return None

    method = method.lower().strip()
    if (
        not password
        or method in LEGACY_SS_CIPHERS
        or not port
        or not (1 <= port <= 65535)
        or not _valid_public_host(host)
    ):
        return None
    signature = json.dumps({"method": method, "query": _query_dict(query)}, sort_keys=True)
    return NodeCandidate(uri, "ss", host, port, f"{method}:{password}", signature)


def parse_node_uri(uri):
    """解析并执行结构、安全性校验；不信任节点备注和上游标签。"""
    uri = uri.strip()
    scheme = uri.split(":", 1)[0].lower()
    if scheme == "ss":
        return _parse_ss_uri(uri)

    if scheme == "vmess":
        try:
            payload = uri[len("vmess://"):].split("#", 1)[0]
            config = json.loads(_decode_base64_text(payload))
            host = str(config.get("add") or "").strip()
            port = int(config.get("port"))
            user_id = str(config.get("id") or "").strip()
            uuid.UUID(user_id)
        except (ValueError, TypeError, json.JSONDecodeError, UnicodeDecodeError, UnicodeEncodeError):
            return None
        if not _valid_public_host(host) or not (1 <= port <= 65535):
            return None
        if str(config.get("allowInsecure", "")).lower() in TRUTHY_VALUES:
            return None
        normalized = {key: value for key, value in config.items() if key != "ps"}
        signature = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return NodeCandidate(uri, scheme, host, port, user_id, signature)

    if scheme not in {"vless", "trojan", "hysteria2", "hy2"}:
        return None
    try:
        parsed = urllib.parse.urlsplit(uri)
        host = parsed.hostname or ""
        port = parsed.port
    except ValueError:
        return None
    if not port or not (1 <= port <= 65535) or not _valid_public_host(host):
        return None

    query = _query_dict(parsed.query)
    if _contains_insecure_flag(query):
        return None

    if scheme == "vless":
        identity = urllib.parse.unquote(parsed.username or "")
        try:
            uuid.UUID(identity)
        except ValueError:
            return None
        security = query.get("security", "none").lower()
        if query.get("pbk") and security != "reality":
            return None
        if security == "reality" and (not query.get("pbk") or not query.get("sni")):
            return None
    elif scheme == "trojan":
        identity = urllib.parse.unquote(parsed.username or "")
        if not identity:
            return None
    else:
        identity = urllib.parse.unquote(parsed.username or "")
        if parsed.password:
            identity += f":{urllib.parse.unquote(parsed.password)}"
        if not identity:
            return None

    signature = urllib.parse.urlencode(sorted(query.items()), quote_via=urllib.parse.quote)
    return NodeCandidate(uri, scheme, host, port, identity, signature)


def _resolve_public_endpoints(host, port):
    results = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    endpoints = []
    seen = set()
    for family, socktype, proto, _, sockaddr in results:
        ip_text = sockaddr[0].split("%", 1)[0]
        ip_value = ipaddress.ip_address(ip_text)
        # 任何私网/环回/保留地址都拒绝，避免不可信来源借测速探测运行器内网。
        if not ip_value.is_global:
            return []
        key = family, sockaddr
        if key not in seen:
            seen.add(key)
            endpoints.append((family, socktype, proto, sockaddr, ip_text))
    return endpoints


def probe_candidate(candidate):
    if candidate.scheme not in TCP_SCHEMES:
        candidate.probe_error = "该协议需要真实客户端进行 UDP/协议级检测"
        return candidate

    latencies = []
    last_error = "连接失败"
    try:
        endpoints = _resolve_public_endpoints(candidate.host, candidate.port)
        if not endpoints:
            candidate.probe_error = "DNS 返回了非公网地址"
            return candidate
    except (OSError, ValueError) as exc:
        candidate.probe_error = f"DNS 失败: {type(exc).__name__}"
        return candidate

    for _ in range(PROBE_ATTEMPTS):
        connected = False
        for family, socktype, proto, sockaddr, ip_text in endpoints:
            started = time.perf_counter()
            try:
                with socket.socket(family, socktype, proto) as sock:
                    sock.settimeout(PROBE_TIMEOUT_SECONDS)
                    sock.connect(sockaddr)
                latencies.append((time.perf_counter() - started) * 1000)
                candidate.resolved_ip = ip_text
                connected = True
                break
            except OSError as exc:
                last_error = type(exc).__name__
        if not connected:
            continue

    candidate.successful_probes = len(latencies)
    if latencies:
        candidate.latency_ms = statistics.median(latencies)
    else:
        candidate.probe_error = last_error
    return candidate


def _stable_tiebreaker(candidate):
    return hashlib.sha256(candidate.uri.encode("utf-8")).hexdigest()


def _network_bucket(candidate):
    if not candidate.resolved_ip:
        return candidate.host.lower()
    ip_value = ipaddress.ip_address(candidate.resolved_ip)
    prefix = 24 if ip_value.version == 4 else 48
    return str(ipaddress.ip_network(f"{ip_value}/{prefix}", strict=False))


def _select_diverse_nodes(candidates):
    ordered = sorted(
        candidates,
        key=lambda item: (
            -item.successful_probes,
            item.latency_ms,
            -len(item.sources),
            _stable_tiebreaker(item),
        ),
    )
    selected = []
    host_counts = {}
    network_counts = {}
    scheme_counts = {}
    scheme_limit = max(8, MAX_NODES // 2)

    for enforce_scheme_limit in (True, False):
        for candidate in ordered:
            if candidate in selected:
                continue
            host_key = candidate.host.lower()
            network_key = _network_bucket(candidate)
            if host_counts.get(host_key, 0) >= 2 or network_counts.get(network_key, 0) >= 3:
                continue
            if enforce_scheme_limit and scheme_counts.get(candidate.scheme, 0) >= scheme_limit:
                continue
            selected.append(candidate)
            host_counts[host_key] = host_counts.get(host_key, 0) + 1
            network_counts[network_key] = network_counts.get(network_key, 0) + 1
            scheme_counts[candidate.scheme] = scheme_counts.get(candidate.scheme, 0) + 1
            if len(selected) >= MAX_NODES:
                return selected
    return selected


def fetch_and_clean_nodes():
    """抓取、解码、严格解析、规范去重，并进行基础公网 TCP 连通性预筛选。"""
    print(f"⏳ 正在并发抓取 {len(NODE_SOURCES)} 个公开节点源...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=FETCH_WORKERS) as executor:
        futures = [
            executor.submit(fetch_from_url, index, url)
            for index, url in enumerate(NODE_SOURCES)
        ]
        fetch_results = [future.result() for future in concurrent.futures.as_completed(futures)]
    fetch_results.sort(key=lambda item: item.index)

    parsed_by_key = {}
    extracted_total = 0
    successful_sources = 0

    for result in fetch_results:
        source_name = urllib.parse.urlsplit(result.source_url).path.strip("/").split("/")[0]
        if not result.content:
            last_error = result.errors[-1] if result.errors else "未知错误"
            print(f"  ❌ {source_name}: 抓取失败；{last_error}")
            continue
        successful_sources += 1
        uris = extract_node_uris(result.content)
        extracted_total += len(uris)
        print(
            f"  ✅ {source_name}: 提取 {len(uris)} 条"
            + ("（经备用地址）" if result.used_url != result.source_url else "")
        )

        for uri in uris[:MAX_NODES_PER_SOURCE]:
            candidate = parse_node_uri(uri)
            if not candidate:
                continue
            existing = parsed_by_key.get(candidate.dedupe_key)
            if existing:
                existing.sources.add(result.source_url)
            else:
                candidate.sources.add(result.source_url)
                parsed_by_key[candidate.dedupe_key] = candidate

    if successful_sources == 0:
        raise RuntimeError("所有节点源均抓取失败，已停止发布，避免生成错误文章")

    candidates = list(parsed_by_key.values())
    candidates.sort(key=lambda item: (-len(item.sources), _stable_tiebreaker(item)))
    candidates = candidates[:MAX_PROBE_CANDIDATES]
    print(
        f"📦 共提取 {extracted_total} 条；严格解析和规范去重后 "
        f"{len(parsed_by_key)} 条，本次最多检测 {len(candidates)} 条。"
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=PROBE_WORKERS) as executor:
        checked = list(executor.map(probe_candidate, candidates))

    stable = [item for item in checked if item.successful_probes == PROBE_ATTEMPTS]
    intermittent = [item for item in checked if 0 < item.successful_probes < PROBE_ATTEMPTS]
    probe_pool = stable if len(stable) >= MIN_NODES else stable + intermittent
    selected = _select_diverse_nodes(probe_pool)

    print(
        f"🔎 TCP 预检：稳定通过 {len(stable)} 条，间歇通过 {len(intermittent)} 条；"
        f"按延迟和网络段去重后选出 {len(selected)} 条。"
    )
    if len(selected) < MIN_NODES:
        raise RuntimeError(
            f"仅有 {len(selected)} 条节点通过最低标准（要求至少 {MIN_NODES} 条），"
            "已停止发布并保留上一期文章"
        )
    return "\n".join(item.uri for item in selected)

def generate_markdown():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    today_cn = now.strftime("%Y年%m月%d日")
    
    password = str(get_today_password(today_str))
    nodes_text = fetch_and_clean_nodes()
    # 节点来自不受信任的第三方，必须转义后才能嵌入 textarea，避免闭合标签注入脚本。
    nodes_html = html.escape(nodes_text, quote=False)
    # 使用 JSON 字符串字面量，避免密码中的引号或反斜杠破坏 JavaScript。
    password_js = json.dumps(password, ensure_ascii=False)
    
    # 确保保存文章的路径存在
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    # 构建高转化 Markdown 文章模板
    md_content = f"""---
date: {today_str}
categories:
  - 免费节点
---

# 【免费节点】{today_cn}自动预筛选节点分享 | 每日更新密码解锁

> **⚠️ 使用须知与重要提醒：**
> 为防止爬虫批量抓取、保障真正粉丝的节点使用体验与速度，本站**不提供长期订阅链接**。
> 所有免费节点均为**独立单节点**，已经过格式、安全性与基础端口连通性预筛选，但仍可能随时失效。请务必观看**今日 YouTube 视频**获取专属查看口令！

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
  <h3 style="color: #ffffff; margin-top: 0;">今日免费节点口令验证</h3>
  <p style="color: #aaa; margin-bottom: 20px; font-size: 0.9rem;">输入今日 YouTube 视频中的专属口令，即可查看经过自动预筛选的节点：</p>
  
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

  <textarea id="node-list" readonly style="width: 100%; height: 280px; background: #000000; color: #00e676; padding: 15px; border-radius: 6px; border: 1px solid #333; font-family: monospace; font-size: 0.85rem; line-height: 1.5; resize: vertical; outline: none;">{nodes_html}</textarea>
</div>

<script>
function checkPwd() {{
  var inputPwd = document.getElementById('node-pwd').value.trim();
  var correctPwd = {password_js};
  
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
