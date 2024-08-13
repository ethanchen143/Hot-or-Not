import time
import urllib.parse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import yt_dlp

# Set up Spotify API credentials
client_id = 'id'
client_secret = 'secret'

def get_tracks(playlist_id):
    # Authenticate with Spotify
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    # Fetch the playlist tracks
    results = sp.playlist_tracks(playlist_id)

    # Extract artist names and track names
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    search_terms = []
    
    # Artist names and track names
    for item in tracks:
        track = item['track']
        # CONDITIONAL ON PLAYLIST
        if track['popularity']>80:
            # Hit Songs
            print(track['name'])
            continue
        
        artist_names = ', '.join([artist['name'] for artist in track['artists']])
        track_name = track['name']
        search_terms.append(f"{track_name} {artist_names}")
    
    return search_terms

def get_youtube_url(search_term, retries=3):
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    path = '/Users/ethanchen/chromedriver-mac-arm64/chromedriver'
    
    for attempt in range(retries):
        driver = webdriver.Chrome(service=Service(path), options=options)
        
        try:
            # Encode the search term
            query = urllib.parse.quote(search_term)
            url = f"https://www.youtube.com/results?search_query={query}"
            
            # Open the YouTube search results page
            driver.get(url)
            
            # Wait for the video title element to be present
            wait = WebDriverWait(driver, 10)
            video = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]')))
            
            video_url = video.get_attribute('href')
            return video_url
        
        except Exception as e:
            print(f"An error occurred on attempt {attempt + 1}: {e}")
            time.sleep(5)  # Wait before retrying
            
        finally:
            driver.quit()
    
    return None

def download_audio(youtube_url, download_path, name):
    try:
        # Set up the options for yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_path}/{name}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        print(f"Downloaded MP3: {download_path}/{name}.mp3")
    except Exception as e:
        print(f"Failed to download audio from {youtube_url}: {e}")


def process_track(term, download_path):
    url = get_youtube_url(term)
    if url:
        download_audio(url, download_path, term)

if __name__ == '__main__':
    playlist_id = '0XmxpRWYyVG3Emj5XbJtqf'
    download_path = './not_audio'
    terms = get_tracks(playlist_id)
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(process_track, term, download_path) for term in terms]
        for future in as_completed(futures):
            future.result()  # Retrieve and handle exceptions

    print("All tracks processed.")