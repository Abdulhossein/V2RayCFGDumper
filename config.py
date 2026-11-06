import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import pytz
import jdatetime
import re

CONFIG_PROTOCOLS = ("vless://", "ss://", "vmess://", "trojan://")


def is_config(text):
    """Check if text contains a V2Ray config protocol."""
    return any(protocol in text for protocol in CONFIG_PROTOCOLS)


def remove_duplicates(input_list):
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def extract_codes_from_telegram(text):
    """Extract V2Ray config codes from Telegram page content.

    Telegram t.me links often contain config codes in various formats.
    This function looks for protocol patterns like vmess://, vless://, etc.
    """
    codes = []
    # Find protocol patterns in text
    for protocol in CONFIG_PROTOCOLS:
        # Match protocol followed by non-whitespace characters
        pattern = re.escape(protocol) + r'[^\s]+'
        matches = re.findall(pattern, text)
        codes.extend(matches)

    # Also look for obfuscated/encoded formats commonly found in Telegram
    # Pattern: protocol followed by base64-like or encoded content
    for protocol in CONFIG_PROTOCOLS:
        # Match protocol with potential URL encoding variations
        pattern = re.escape(protocol).replace('://', r'[:/]*') + r'[^\s&]+'
        matches = re.findall(pattern, text)
        codes.extend(matches)

    return codes


addresses = [
    "https://raw.githubusercontent.com/patterniha/Free-Configs/main/configs.txt",
    "https://telegram.me/s/filembad",
    "https://telegram.me/s/canfingV2rayNG",
    "https://telegram.me/s/Alpha_V2ray_Iran",
    "https://telegram.me/s/Farah_VPN",
    "https://telegram.me/s/vaddress",
    "https://telegram.me/s/v2ray_claim",
    "https://t.me/s/v2rayngvpn",
    "https://t.me/s/persianvpnhub",
    "https://telegram.me/s/FreakConfig",
    "https://telegram.me/s/BigSmoke_Config",
    # Add support for private Telegram links
    "https://t.me/+eSpH7AYS2FoxZmM8",
]

codes = []

for url in addresses:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Failed to fetch {url}: {error}")
        continue

    page = response.text
    content_type = response.headers.get("Content-Type", "").lower()
    url_codes = []

    if "text/html" in content_type or "<code" in page.lower():
        soup = BeautifulSoup(page, "html.parser")
        for code_tag in soup.find_all('code'):
            code_content = code_tag.text.strip()
            if is_config(code_content):
                url_codes.append(code_content)

    if not url_codes:
        for token in page.split():
            if is_config(token):
                url_codes.append(token)

    # Also use regex-based extraction for Telegram links
    url_codes.extend(extract_codes_from_telegram(page))

    codes.extend(url_codes)

codes = list(set(codes))  # Remove duplicates

processed_codes = []

current_date_time = jdatetime.datetime.now(pytz.timezone('Asia/Tehran'))
current_month = current_date_time.strftime("%b")
current_day = current_date_time.strftime("%d")
updated_hour = current_date_time.strftime("%H")
updated_minute = current_date_time.strftime("%M")
final_string = f"{current_month}-{current_day} | {updated_hour}:{updated_minute}"
final_others_string = f"{current_month}-{current_day}"
config_string = "#✅ " + str(final_string) + "-"

for code in codes:
    vmess_parts = code.split("vmess://")
    vless_parts = code.split("vless://")

    for part in vmess_parts + vless_parts:
        if "ss://" in part or "vmess://" in part or "vless://" in part or "trojan://" in part:
            service_name = part.split("serviceName=")[-1].split("&")[0]
            processed_part = part.split("#")[0]
            processed_codes.append(processed_part)

processed_codes = remove_duplicates(processed_codes)

new_processed_codes = []

for code in processed_codes:
    vmess_parts = code.split("vmess://")
    vless_parts = code.split("vless://")

    for part in vmess_parts + vless_parts:
        if "ss://" in part or "vmess://" in part or "vless://" in part or "trojan://" in part:
            service_name = part.split("serviceName=")[-1].split("&")[0]
            processed_part = part.split("#")[0]
            new_processed_codes.append(processed_part)

i = 0
with open("sub.txt", "w", encoding="utf-8") as file:
    for code in new_processed_codes:
        if i == 0:
            config_string = "#🌐 به روزرسانی شده در" + final_string
        else:
            config_string = "#🌐سرور " + \
                str(i) + " | " + str(final_others_string) + "| MTSRVRS"
        config_final = code + config_string
        file.write(config_final + "\n")
        i += 1
