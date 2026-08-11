#!/usr/bin/env python3
"""Google OAuth 共享层(零依赖,纯 stdlib)。

gsc.py 与 ga4.py 共用**同一份**凭证和同一次授权——因为它们是同一个 GCP 项目
(`shark-gsc`)下的同一个 OAuth 客户端,只是 scope 里多带了 Analytics 一项。

凭证路径:~/.config/shark-agent/google.json(仓库外,权限 600,不进 git)
历史路径 gsc.json 仍可读,只为兼容旧安装;新授权一律写 google.json。
"""

import json
import os
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

CONFIG_DIR = os.path.expanduser("~/.config/shark-agent")
CONFIG_PATH = os.path.join(CONFIG_DIR, "google.json")
LEGACY_CONFIG_PATH = os.path.join(CONFIG_DIR, "gsc.json")

TOKEN_URL = "https://oauth2.googleapis.com/token"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

# 一次授权覆盖两个 API。加新 API 时往这里追加,然后重跑 `gsc.py auth`。
SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]


class AuthExpired(RuntimeError):
    """refresh_token 失效(测试模式 7 天过期 / 用户撤销授权 / 密钥轮换)。

    日报脚本捕获它来发「凭证过期」提醒,而不是静默失败。
    """


def config_path():
    if os.path.exists(CONFIG_PATH):
        return CONFIG_PATH
    if os.path.exists(LEGACY_CONFIG_PATH):
        return LEGACY_CONFIG_PATH
    return CONFIG_PATH


def load_config():
    path = config_path()
    if not os.path.exists(path):
        raise AuthExpired(
            f"没找到凭证 {CONFIG_PATH}\n"
            "先跑一次:python3 scripts/gsc.py auth --client-secret-file <下载的 json>"
        )
    with open(path) as f:
        return json.load(f)


def save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
    os.chmod(CONFIG_PATH, 0o600)


def post_form(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def access_token(cfg=None):
    """用 refresh_token 换一个短期 access_token。"""
    cfg = cfg or load_config()
    try:
        tok = post_form(TOKEN_URL, {
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "refresh_token": cfg["refresh_token"],
            "grant_type": "refresh_token",
        })
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        if e.code in (400, 401):
            raise AuthExpired(
                "refresh_token 已失效。重新授权:\n"
                "  python3 scripts/gsc.py auth --client-secret-file <下载的 json>\n"
                f"Google 返回:{detail}"
            )
        raise
    return tok["access_token"]


def api_call(token, url, payload=None, timeout=60):
    """带 Bearer 的 JSON 请求。payload 非 None 时走 POST。"""
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("Authorization", f"Bearer {token}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        if e.code == 403 and "accessNotConfigured" in detail:
            raise RuntimeError(
                f"API 没在 GCP 项目里启用。去控制台启用后重试。\n{detail}"
            )
        raise RuntimeError(f"HTTP {e.code} 从 {url}\n{detail}")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def run_oauth_flow(client_id, client_secret, scopes=None):
    """本地回环 OAuth,拿到长期 refresh_token 存盘。返回写入的 cfg。"""
    scopes = scopes or SCOPES
    port = free_port()
    redirect_uri = f"http://localhost:{port}"
    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
    })

    captured = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            qs = urllib.parse.urlparse(self.path).query
            captured.update(urllib.parse.parse_qs(qs))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = "授权成功,回到终端即可。" if "code" in captured else "授权失败,看终端输出。"
            self.wfile.write(f"<html><body><h2>{msg}</h2></body></html>".encode())

        def log_message(self, *a):
            pass

    server = HTTPServer(("127.0.0.1", port), Handler)
    print("在浏览器里完成授权(如果没自动打开,手动访问下面这个链接):\n")
    print(url + "\n")
    webbrowser.open(url)
    server.handle_request()
    server.server_close()

    if "code" not in captured:
        sys.exit(f"没拿到授权码:{captured}")

    tok = post_form(TOKEN_URL, {
        "code": captured["code"][0],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    })
    if "refresh_token" not in tok:
        sys.exit(
            "Google 没返回 refresh_token。通常是这个客户端之前授权过。\n"
            "去 https://myaccount.google.com/permissions 撤销后重跑。"
        )

    cfg = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": tok["refresh_token"],
        "scopes": scopes,
    }
    save_config(cfg)
    return cfg


def client_credentials_from_args(args):
    """从 --client-secret-file 或 --client-id/--client-secret 解析出客户端凭证。"""
    if args.client_id and args.client_secret:
        return args.client_id, args.client_secret
    if args.client_secret_file:
        with open(os.path.expanduser(args.client_secret_file)) as f:
            blob = json.load(f)
        node = blob.get("installed") or blob.get("web") or blob
        return node["client_id"], node["client_secret"]
    # 已授权过的话,客户端凭证本身就在配置里,重新授权不用再翻下载目录。
    if os.path.exists(config_path()):
        cfg = load_config()
        if cfg.get("client_id") and cfg.get("client_secret"):
            return cfg["client_id"], cfg["client_secret"]
    sys.exit(
        "需要 OAuth 客户端凭证。二选一:\n"
        "  --client-secret-file ~/Downloads/client_secret_xxx.json\n"
        "  --client-id ... --client-secret ...\n"
        "获取方式见 memory/sources/gsc.md「一次性配置」"
    )
