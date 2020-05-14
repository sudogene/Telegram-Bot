from collections import deque

class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, text):
        with open(self.filename, 'a') as file:
            file.write(text + '\n')

    def print_info(self, n_last_lines=5):
        print('========= Debug log =========')
        print(f'File name: {self.filename}')
        print(f'Total lines: {sum(1 for line in open(self.filename))}')
        print(f'Printing last {n_last_lines} line(s)...')
        with open(self.filename) as file:
            lines = deque(file, n_last_lines)
        print(''.join(lines).strip())
        print('========= End of log =========')

if __name__ == '__main__':
    Logger('log.txt').print_info()