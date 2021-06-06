import os
import shutil
import plotly.express as px
import concurrent.futures


class Drive:
    def __init__(self, name, path, game_libraries=[]):
        self.name = name
        self.path = path
        self.game_libraries = game_libraries
        self.game_library_sizes = []
        self.game_sizes = []
        self.disk_usage = round(shutil.disk_usage(self.path).used/1024**3, 1)
        self.disk_size = round(shutil.disk_usage(self.path).total/1024**3, 1)
    
        self.get_library_sizes()

    def get_library_sizes(self):
        for library in [i[1] for i in self.game_libraries]:
            game_sizes = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                game_names = os.listdir(library)
                game_paths = [os.path.join(library, game) for game in game_names]
                results = executor.map(get_directory_size, game_paths)
                for i, result in enumerate(results):
                    game_sizes.append((game_names[i], result))
            self.game_sizes.append(game_sizes)
            self.game_library_sizes.append(round(sum([i[1] for i in game_sizes]), 1))

    def __str__(self):
        output = f'{self.name} ({self.path}) ({self.disk_usage} GB / {self.disk_size} GB):'
        output += f'\n{len(output)*"="}\n'
        for i, game_library in enumerate(self.game_libraries):
            library_title = f'  {game_library[0]} ({len(self.game_sizes[i])} games) ({self.game_library_sizes[i]} GB)'
            output += library_title + '\n  ' + (len(library_title) - 2) * '-' + '\n'
            for game in self.game_sizes[i]:
                output += f'    {game[0]} ({game[1]} GB)\n'
            output += '\n'
        return output


def get_directory_size(directory='.'):
    size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(directory) for filename in filenames)
    return round(size/1024**3, 1)


def plot(drive):
    # The drive itself
    sections = [drive.name]
    parents = ['']
    values = [drive.disk_size]
    
    # Game libraries on the drive
    #library_names = [f'{library[0]} ({len(drive.game_sizes[i])} games)' for i, library in enumerate(drive.game_libraries)]
    library_names = [library[0] for library in drive.game_libraries]
    sections.extend(library_names)
    parents.extend((len(library_names)) * [drive.name])
    values.extend(drive.game_library_sizes)

    # OS/other apps and free space
    sections.extend(['Other', 'Free Space'])
    parents.extend(2 * [drive.name])
    values.append(round(drive.disk_usage - sum(drive.game_library_sizes), 1))
    values.append(round(drive.disk_size - drive.disk_usage, 1))

    # Games
    for i, library_name in enumerate(library_names):
        for game in drive.game_sizes[i]:
            sections.append(game[0])
            parents.append(library_name)
            values.append(game[1])

    data = dict(sections=sections,
                parents=parents,
                values=values)
    fig = px.sunburst(data, names='sections', parents='parents', values='values', branchvalues='total')
    fig.show()



if __name__ == '__main__':
    drives = [Drive('SSD', 'C:\\', [('Steam', 'C:/Program Files (x86)/Steam/steamapps/common'),
                                    ('Steam (Downloading)', 'C:/Program Files (x86)/Steam/steamapps/downloading'),
                                    ('Epic Games', 'C:/Program Files (x86)/Epic Games'),
                                    ('Ubisoft', 'C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/games')]),
            Drive('HDD', 'E:\\', [('Steam', 'E:/SteamLibrary/steamapps/common'),
                                  ('Steam (Downloading)', 'E:/SteamLibrary/steamapps/downloading'),
                                  ('Epic Games', 'E:/EpicGames')])]
    print('\n\n')
    for drive in drives:
        print(drive)
        plot(drive)
