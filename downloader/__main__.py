from downloader import Downloader

if __name__ == '__main__':
    try:
        dwl = Downloader()
        dwl.run()
    except Exception as e:
        print(f'Failed to download or process map with exception {type(e)}')
        print(e)

