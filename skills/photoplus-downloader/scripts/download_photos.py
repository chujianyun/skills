import os
import hashlib
import requests
import argparse
import time
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

SALT = 'laxiaoheiwu'
COUNT = 9999

def obj_key_sort(obj):
    sorted_keys = sorted(obj.keys())
    new_obj = []
    for key in sorted_keys:
        if obj[key] is not None:
            value = str(obj[key])
            new_obj.append(f"{key}={value}")
    return '&'.join(new_obj)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_image(url, dir):
    filename = url.split('/')[-1].split('#')[0].split('?')[0]
    filename = sanitize_filename(filename)
    image_path = os.path.join(dir, filename)

    if os.path.exists(image_path):
        return

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

def download_all_images(list, dir):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for item in list:
            url = f"https:{item['origin_img']}"
            futures.append(executor.submit(download_image, url, dir))
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading images"):
            future.result()

def get_all_images(id, count):
    t = int(time.time() * 1000)  # Current timestamp in milliseconds
    dir = f"./dist/{id}"
    
    data = {
        "activityNo": id,
        "isNew": False,
        "count": count,
        "page": 1,
        "ppSign": "live",
        "picUpIndex": "",
        "_t": t
    }
    
    data_sort = obj_key_sort(data)
    sign = hashlib.md5((data_sort + SALT).encode()).hexdigest()
    
    params = {
        **data,
        "_s": sign,
        "ppSign": "live",
        "picUpIndex": "",
    }
    
    response = requests.get('https://live.photoplus.cn/pic/pics', params=params)
    result = response.json()['result']
    
    print(f"Total photos: {result['pics_total']}, download: {count}")
    
    os.makedirs(dir, exist_ok=True)
    download_all_images(result['pics_array'], dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download photos from PhotoPlus")
    parser.add_argument("--id", type=int, help="PhotoPlus ID (e.g., 87654321)", required=True)
    parser.add_argument("--count", type=int, default=COUNT, help="Number of photos to download")
    
    args = parser.parse_args()
    
    if args.id:
        get_all_images(args.id, args.count)
    else:
        print("Wrong ID")
