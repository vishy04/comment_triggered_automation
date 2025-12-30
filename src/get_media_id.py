import sys

def get_media_id(url):

    shortcode = url.rstrip('/').split('?')[0].split('/')[-1][:11]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    
    media_id = 0
    for char in shortcode:
        media_id = (media_id * 64) + alphabet.index(char)
    return media_id

if __name__ == "__main__":
    if len(sys.argv) > 1:
        media_id = get_media_id(sys.argv[1])
        print(f"MEDIA_ID={media_id}")
    else:
        print("Usage: python src/get_media_id.py <url>")
