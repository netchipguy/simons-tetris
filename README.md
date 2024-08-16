# simons-tetris

Recreating an old favorite game is like learning to play an old favorite song.

An homage as much as entertainment. 

I'm hosting this on GitHub not because I think it's super interesting to anyone else, but 
rather because I am tired of maintaining my own source control at home :) 

# Running on MacOS

## First time install

I was running a Homebrew python3/pip3 install, and didn't want to remember python venv to run a game.

Homebrew doesn't have a pygame package, but meanwhile warns about messing with it (see https://peps.python.org/pep-0668/)

We aren't going to be abusing pip3 to override versions of installed stuff, uninstall stuff, etc, so go ahead and:

pip3 install pygame --user --break-system-packages  # NB: ignore notices about updating pip, that's why the above issues exist

## Running

python3 tetris.py

# Running on Linux

## First time install

Assuming you have a sane distro:

pip3 install pygame --user

## Running

python3 tetris.py





