import tkinter as tk
from tkinter import filedialog as fd
import YoutubeDownloader as Downloader

GRID_COL = 6
GRID_ROW = 9
TYPES = {'audio': 140, 'video': 22}  #


class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.iconbitmap('youtube_icon.ico')
        self.root.geometry('750x280')
        self.root.resizable(0, 0)
        self.file_path = ''
        self.link = ''
        self.mode = '1by1'
        self.type = TYPES['audio']
        self.messages = []

        # functional gadgets:
        self.mode_playlist = tk.Button(
            self.root, text='playlist', fg='black', bg='snow', width=35, height=1,
            activebackground='red', relief='raised', command=self.mode_playlist, state='normal'
        )
        self.mode_one_by_one = tk.Button(
            self.root, text='song by song', bg='snow', fg='black', width=35, height=1,
            activebackground='red', relief='sunken', command=self.mode_1by1, state='disabled'
        )
        self.video_button = tk.Button(
            self.root, text='Video', fg='black', bg='snow', width=35, height=1,
            activebackground='red', relief='raised', command=self.video, state='normal'
        )
        self.audio_button = tk.Button(
            self.root, text='Audio', fg='black', bg='snow', width=35, height=1,
            activebackground='red', relief='sunken', command=self.audio, state='disabled'
        )
        self.download_button = tk.Button(
            self.root, text='Download!', bg="orange", fg='black', width=10, height=1,
            activebackground='red', relief='groove', command=self.download
        )
        self.choose_file = tk.Button(
            self.root, text='choose', bg="black", fg='white',  width=10, height=1,
            activebackground='red', relief='groove', command=self.get_path
        )
        self.entry_link = tk.Entry(
            self.root, cursor='xterm', width=90, bg='white'
        )
        self.playlist_name = tk.Entry(
            self.root, cursor='X_cursor', width=90, state='disabled', bg='white'
        )
        self.board = tk.Label(text='', bg='turquoise3', width=103, height=8, relief='groove')
        self.directory_label = tk.Label(text='', width=77, height=1)

        # decoration labels:
        for i in range(GRID_COL):
            tk.Label(text='').grid(column=i, row=0)
            tk.Label(text='').grid(column=i, row=GRID_ROW)
        for i in range(GRID_ROW):
            tk.Label(text='').grid(column=0, row=i)
            tk.Label(text='').grid(column=GRID_COL, row=i)
        tk.Label(text='URL:').grid(column=1, row=5, columnspan=1)
        tk.Label(text='Directory:').grid(column=1, row=3, columnspan=1)
        tk.Label(text='Mode:').grid(column=1, row=1, columnspan=1)
        tk.Label(text='Playlist name:').grid(column=1, row=4, columnspan=1)
        tk.Label(text='Download type:').grid(column=1, row=2, columnspan=1)

        # functional placements:
        self.board.grid(column=1, row=6, columnspan=5, rowspan=2)
        self.directory_label.grid(column=2, row=3, columnspan=2)
        self.mode_playlist.grid(column=3, row=1)
        self.mode_one_by_one.grid(column=2, row=1)
        self.download_button.grid(column=4, row=5)
        self.choose_file.grid(column=4, row=3)
        self.entry_link.grid(column=2, row=5, padx=10, columnspan=2)
        self.playlist_name.grid(column=2, row=4, columnspan=2)
        self.video_button.grid(column=2, row=2)
        self.audio_button.grid(column=3, row=2)

    def update_board(self, line):
        """updates the log board with update messages"""
        if len(self.messages) > 7:
            del self.messages[0]
        self.messages.append(line)
        self.board['text'] = '\n'.join(self.messages)

    def get_path(self):
        """open a new windows in which the user can choose a path"""
        self.directory_label.configure(bg='white')
        self.file_path = fd.askdirectory()
        self.directory_label['text'] = self.file_path

    def download(self):
        """download a track or a playlist"""
        self.link = self.entry_link.get()
        name = self.playlist_name.get()
        self.reset()
        if self.link and self.file_path:
            if self.mode == 'playlist':
                self.download_playlist(name)
            elif self.mode == '1by1':
                self.download_track()
        else:
            if not self.file_path:
                self.update_board('Choose directory!')
                self.directory_label['bg'] = 'RosyBrown1'
            if self.mode == 'playlist' and not name:
                self.update_board('Insert playlist name!')
                self.playlist_name.configure(bg='light coral')
            if not self.link:
                self.update_board('Insert link!')
                self.entry_link.configure(bg='light coral')

    def download_playlist(self, name: str):
        """
        download a playlist.
        :param name: name of the playlist
        """
        if not name:
            self.playlist_name.configure(bg='light coral')
            self.update_board('Insert playlist name!')
        else:
            self.update_board('Trying to download...')
            try:
                Downloader.download_playlist(self.link, self.file_path + '//' + name)
                self.update_board('Download complete!')
                if self.type == TYPES['audio']:
                    self.update_board('Converting to audio...')
                    Downloader.convert(self.file_path + '//' + name)
                    self.update_board('Done!')
                self.entry_link.delete(0, 'end')
                self.playlist_name.delete(0, 'end')
            except:
                self.update_board('Error!')

    def download_track(self):
        """downloads a single track"""
        self.update_board('Trying to download...')
        try:
            Downloader.download_track(self.link, self.file_path, self.type)
            self.update_board('Download complete!')
            self.entry_link.delete(0, 'end')
        except:
            self.update_board('Error!')

    def mode_1by1(self):
        """user chose the mode "one by one" """
        self.mode = '1by1'
        self.playlist_name.delete(0, 'end')
        self.reset()
        self.mode_one_by_one.configure(relief='sunken', state='disabled')
        self.mode_playlist.configure(relief='raised', state='normal')
        self.playlist_name.configure(cursor='X_cursor', state='disabled')

    def mode_playlist(self):
        """user chose the mode "playlist" """
        self.mode = 'playlist'
        self.reset()
        self.mode_playlist.configure(relief='sunken', state='disabled')
        self.mode_one_by_one.configure(relief='raised', state='normal')
        self.playlist_name.configure(cursor='xterm', state='normal')

    def video(self):
        """user chose to download video"""
        self.type = TYPES['video']
        self.reset()
        self.audio_button.configure(state='normal', relief='raised')
        self.video_button.configure(state='disabled', relief='sunken')

    def audio(self):
        """user chose to download audio"""
        self.type = TYPES['audio']
        self.reset()
        self.audio_button.configure(state='disabled', relief='sunken')
        self.video_button.configure(state='normal', relief='raised')

    def reset(self):
        """reset the entry of link, name and directory"""
        self.entry_link.configure(bg='white')
        self.directory_label.configure(bg='white')
        self.playlist_name.configure(bg='white')


if __name__ == "__main__":
    window = tk.Tk()
    app = YoutubeDownloader(window)
    window.mainloop()
