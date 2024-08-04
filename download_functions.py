from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import zipfile
import os
import requests



def download_file(url):
  """
    Downloads a file from the specified URL and saves it to the local disk.
    Uses ThreadPoolExecutor to start multiple tasks and download data chunks concurrently for more download speed.

    Args:
        url (str): The URL of the file to download.
    Returns:
        None
  """

  
  def download_chunk(url, start, end, filename, pbar):
    """
    Downloads a chunk of data from the given URL and writes it to the specified file.

    Args:
      url (str): The URL to download the chunk from.
      start (int): The starting byte position of the chunk.
      end (int): The ending byte position of the chunk.
      filename (str): The name of the file to write the chunk to.
      pbar (ProgressBar): The progress bar to update after downloading the chunk.
    """
    response = requests.get(url, headers={'Range': f'bytes={start}-{end}'})
    # open file in binary mode for reading and writting
    with open(filename, 'r+b') as fob:
        # set start point at file object
        fob.seek(start)
        # write chunk at file object
        fob.write(response.content)
    # update progress bar after downloading chunk
    pbar.update(end-start)


  # get header of server
  response = requests.head(url)
  # file size specified in header
  file_size = int(response.headers['content-length'])

  chunk_size = 1024 * 1024 * 2 # 2^10 Bytes = 1048576 = 1024 *1024 = 1 MB
  filename = url.split('/')[-1]

  # Create an empty file with file size containing null bites
  with open(filename, 'wb') as fob:
      fob.write(b'\0' * file_size)

  # Download each chunk of the file in a separate thread
  #createprogress bat
  with tqdm(total=file_size, unit='B', unit_scale=True, desc=filename) as pbar:
    # multi-threaded (parallel) execution of tasks with ThreadPoolExecutor
      with ThreadPoolExecutor(max_workers=30) as executor:
          futures = []# list of tasks; future is a referall to task
          #iterate over file with spacing chunk_size
          for start in range(0, file_size, chunk_size):
              end = min(start + chunk_size - 1, file_size - 1) # end byte chunk, shouldnt exceed file_size
              #submit task to executer, download chunk, append to future list showing task has sumbitted
              futures.append(executor.submit(download_chunk, url, start, end, filename, pbar))
              #checking futures
          for future in futures:
              future.result()

  # unzip, save and remove file
  with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall('gip_data')
  os.remove(filename)