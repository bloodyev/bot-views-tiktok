import requests
import re
import time
import random
import uuid
import binascii
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import SignerPy
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "SignerPy"])
    import SignerPy

def load_sessions_from_file(file_path="hhh.txt"):
    sessions = []
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                sessions = [line.strip() for line in f if line.strip()]
            print(f"Loaded {len(sessions)} sessions from {file_path}")
        else:
            print(f"File {file_path} not found, loading from URL...")
            
    except Exception as e:
        print(f"Error loading sessions: {e}")
        sys.exit(1)
    
    return sessions

SESSIONS = load_sessions_from_file("hhh.txt")

def extract_from_short_url(short_url):
    try:
        if "vt.tiktok.com" in short_url or "vm.tiktok.com" in short_url:
            response = requests.get(
                short_url,
                allow_redirects=True,           
                timeout=30
            )
            final_url = response.url
        else:
            final_url = short_url
        
        aweme_match = re.search(r'/video/(\d+)', final_url)
        cid_match = re.search(r'(?:share_comment_id|commentId)=(\d+)', final_url)
        
        if not aweme_match or not cid_match:
            raise ValueError("Could not find aweme_id or cid in URL")
        
        aweme_id = aweme_match.group(1)
        cid = cid_match.group(1)
        return aweme_id, cid, final_url
    except Exception as e:
        print(f"Error extracting data from URL: {e}")
        sys.exit(1)

short_url = input("TikTok Link (vt.tiktok.com oder direkter Link): ").strip()
aweme_id, cid, full_url = extract_from_short_url(short_url)
print(f"Extracted data: aweme_id={aweme_id}, cid={cid}")
