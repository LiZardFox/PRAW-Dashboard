from populate_db import update
from datetime import datetime 

def main():
    print('daily script called', datetime.now().strftime('%a %d %b %Y, %I:%M%p'))
    update()

if __name__ == "__main__":
    main()
