#!/usr/bin/env python3
"""
Proxy List Updater
Fetches latest proxy lists from TheSpeedX/PROXY-List repository
"""

import requests
import os
import sys
from datetime import datetime

# Base URL for raw files from TheSpeedX/PROXY-List repository
BASE_URL = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master"

# Files to download
PROXY_FILES = {
    "http.txt": f"{BASE_URL}/http.txt",
    "socks4.txt": f"{BASE_URL}/socks4.txt", 
    "socks5.txt": f"{BASE_URL}/socks5.txt"
}

def download_file(url, filename):
    """Download a file from URL and save it locally"""
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Write content to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        # Count lines (proxies)
        lines = len(response.text.strip().split('\n'))
        print(f"✓ {filename} updated successfully ({lines} proxies)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error saving {filename}: {e}")
        return False

def create_readme():
    """Create or update README with proxy information"""
    try:
        readme_content = f"""# Proxy Lists

Auto-updated proxy lists fetched from [TheSpeedX/PROXY-List](https://github.com/TheSpeedX/PROXY-List)

## Files

- `http.txt` - HTTP/HTTPS proxies
- `socks4.txt` - SOCKS4 proxies  
- `socks5.txt` - SOCKS5 proxies

## Stats

"""
        
        for filename in PROXY_FILES.keys():
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = len([line for line in f if line.strip()])
                readme_content += f"- **{filename}**: {lines} proxies\n"
        
        readme_content += f"""
## Last Updated

{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Usage

Each file contains one proxy per line in the format:
- HTTP: `ip:port`
- SOCKS4: `ip:port`
- SOCKS5: `ip:port`

## Disclaimer

These proxies are collected from public sources. Use responsibly and verify their reliability before use.
"""
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        print("✓ README.md updated")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create README: {e}")
        return False

def main():
    """Main function to download all proxy files"""
    print("🔄 Starting proxy list update...")
    print(f"Source: {BASE_URL}")
    print("-" * 50)
    
    success_count = 0
    total_files = len(PROXY_FILES)
    
    # Download each proxy file
    for filename, url in PROXY_FILES.items():
        if download_file(url, filename):
            success_count += 1
    
    print("-" * 50)
    print(f"📊 Results: {success_count}/{total_files} files updated successfully")
    
    # Create README
    create_readme()
    
    if success_count == total_files:
        print("✅ All proxy lists updated successfully!")
        sys.exit(0)
    else:
        print("⚠️ Some files failed to update")
        sys.exit(1)

if __name__ == "__main__":
    main()
