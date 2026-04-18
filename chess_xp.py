import configparser

#this is a vibe coded project, if you find errors, problems, or suggestions, please email me at cyrusjaimes7@gmail.com

#Variables
CONFIG_FILE = 'config.ini'

# 1. Initialize the parser
config = configparser.ConfigParser()

# 2. Read the file
config.read('config.ini')

# 3. Access the specific variable
streak = config['SETTINGS']['streak']
level = config['SETTINGS']['level']
streak = int(streak)
level = int(level)

print(f"Loaded streak: {streak}")



#credits to Mojang AB for the leveling inspirations!
if level <= 15 and not level <= 0:
    needed = 2 * level + 7
    print(needed)
elif level >= 16 and level <=30:
    needed = 5 * level - 38
    print(needed)
elif level >= 31:
    needed = 9 * level - 158
    print(needed)
else:
    input("there is no level attribute or its level is modified to 0 or less in your config.ini file, please make an issue in the github and include what your specs is and what you did before this, wanna make a new level in your config.ini? Y/N ")
    config.set('SETTINGS', 'level', "1")
    with open(CONFIG_FILE, 'w') as f: 
        config.write(f)

