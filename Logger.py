from collections import deque

class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, text):
        with open(self.filename, 'a') as file:
            file.write(text + '\n')

    def print_log(self, n_last_lines=5):
        print('========= Debug log =========')
        print(f'File name: {self.filename}')
        print(f'Total lines: {sum(1 for line in open(self.filename))}')
        print(f'Printing last {n_last_lines} line(s)...')
        with open(self.filename) as file:
            lines = deque(file, n_last_lines)
        print(''.join(lines).strip())
        print('========= End of log =========')

    def wipe_log(self):
        print('========= Wiping log =========')
        print(f'File name: {self.filename}')
        open(self.filename, 'w').close()
        print("File wiped.")
        print('========= End of wipe =========')


if __name__ == '__main__':
    use = input('Debug or Wipe?\nD / W : ')
    while use not in ('D', 'W', 'd', 'w'):
        use = input('Debug or Wipe?\nD / W : ')

    if use.upper() == 'D':
        Logger('log.txt').print_log()
    elif use.upper() == 'W':
        Logger('log.txt').wipe_log()
