__author__ = 'vlad'

if __name__ == '__main__':
    number = 2
    if not number:
        global number
        number = input('Which lab to launch => ')
    filename = 'lab_{0}/main.py'.format(number)
    with open(filename,'r') as f:
        code = compile(f.read(), filename, 'exec')
        exec(code)