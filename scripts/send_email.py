#!/usr/bin/env python3
"""通用邮件发送脚本（QQ邮箱 SMTP SSL）。

用法:
    python3 scripts/send_email.py --subject "主题" --body-file body.txt
    python3 scripts/send_email.py --subject "主题" --body "正文文本"
    可选 --html 表示正文为 HTML 格式。

配置读取自 config/email.json（相对项目根目录）。
"""
import argparse
import json
import smtplib
import sys
from email.header import Header
from email.mime.text import MIMEText
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "email.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Send email via QQ SMTP")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", default=None)
    parser.add_argument("--body-file", default=None)
    parser.add_argument("--html", action="store_true", help="body is HTML")
    args = parser.parse_args()

    if not CONFIG_PATH.exists():
        print(f"配置文件不存在: {CONFIG_PATH}", file=sys.stderr)
        return 1
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    elif args.body is not None:
        body = args.body
    else:
        print("必须提供 --body 或 --body-file", file=sys.stderr)
        return 1

    subtype = "html" if args.html else "plain"
    msg = MIMEText(body, subtype, "utf-8")
    msg["Subject"] = Header(args.subject, "utf-8")
    msg["From"] = cfg["sender_email"]
    msg["To"] = cfg["recipient_email"]

    try:
        with smtplib.SMTP_SSL(cfg["smtp_server"], cfg["smtp_port"], timeout=30) as server:
            server.login(cfg["sender_email"], cfg["sender_auth_code"])
            server.sendmail(cfg["sender_email"], [cfg["recipient_email"]], msg.as_string())
    except Exception as exc:  # noqa: BLE001
        print(f"发送失败: {exc}", file=sys.stderr)
        return 2

    print("发送成功")
    return 0


if __name__ == "__main__":
    sys.exit(main())
