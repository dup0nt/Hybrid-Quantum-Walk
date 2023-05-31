import os
from datetime import datetime

now = datetime.now()
formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')

directory = ''  # Replace with your desired directory path

with open(os.path.join(directory, 'hello_world.txt'), 'w') as file:
    file.write('Hello World @ '+ str(formatted_now))
