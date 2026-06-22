#!/usr/bin/env python3
"""
Email Hunter - Free CLI tool to find business emails from websites.
Scrapes contact pages for mailto: links and displayed emails.

Need a custom version? $49 one-time at:
https://buy.stripe.com/dRmbJ1964cXW8nn2QPb3q00
"""
import sys, re, urllib.request, urllib.error, ssl
from html.parser import HTMLParser

class EmailExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.emails = set()
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and 'mailto:' in value:
                email = value.replace('mailto:', '').split('?')[0].strip().lower()
                if '@' in email and '.' in email.split('@')[-1]:
                    self.emails.add(email)

def extract_from_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx, timeout=15).read().decode('utf-8', errors='ignore')
        parser = EmailExtractor()
        parser.feed(html)
        found = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html))
        parser.emails.update(found)
        return sorted(parser.emails)
    except Exception:
        return []

if __name__ == '__main__':
    urls = sys.argv[1:] if len(sys.argv) > 1 else []
    if not urls:
        print("Email Hunter - Find business emails from websites")
        print("Usage: python3 find_emails.py <url1> [url2 ...]")
        print("Example: python3 find_emails.py https://example.com/contact")
        print()
        print("Need a custom scraper or bot? $49 one-time:")
        print("https://buy.stripe.com/dRmbJ1964cXW8nn2QPb3q00")
        sys.exit(0)
    for url in urls:
        emails = extract_from_url(url)
        if emails:
            print(f"\n{url}:")
            for e in emails:
                print(f"  {e}")
        else:
            print(f"\n{url}: No emails found")
