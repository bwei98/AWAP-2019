# AWAP
Welcome to Algorithms with a Purpose! You and three of your friends really want to get some internships, but the job fairs get worse and worse every year! All you usually get is a bit of swag that you never touch after a while. Feeling down because of some disappointing results at the last job fair, everyone decides to pool all of their efforts together so that at least one person gets the gift of enlightenment - the summer internship. Armed with an unlimited data plan, you prepare to set out to your latest battlefield to see if you can use the additional information of three friends to your advantage. 

### The battlefield
You and your friends decided to do some reconnaisance on the battlefield to help you create a battle plan, only to notice that the situation is quite different than you previously remember - everything seems much more tile-y. After some exploration, you discover that the entire laws of physics have changed in this realm! Feeling curious, you figure out that

* Instead of being continuous, time is now discrete (this is a turn-based game).
* The world is separated into square tiles that can hold multiple people on a tile.
* The moves you can make are very limited; at each turn, you can move in one of the cardinal directions, enter a line, stay still, or have a team bot switch positions with another team bot.
* Movement seems to take longer when moving into tiles with more people on them.
* If a movement takes longer than a single turn, you can cancel the movement by either staying still or moving in a different direction. If you want to continue the movement, you have to keep walking in the same direction.
* Because of the crowd, you can only see a radius of 2 tiles around you. (By "radius" we mean if you on a tile, you have vision in the 5x5 square that has your current tile in the center.)
* Once you are in a line, you have to stay still and let the line move you; if you make any movements, the people behind you will push you out.

Although these rules are very different to you, you change your plans to accomodate to the new circumstances.

### Victory conditions

During one of your reconnaisance runs, you notice another set of four friends doing exactly the same thing you were doing! You realize that another group of friends had the same idea as you, and so in order to realize your dreams, you need to have a better chance of getting a job than your rivals.

Putting that information at the back of your mind, since you don't know if they will actually show up on the day of, you direct your attention towards more important things. While examining the situation further, you also notice that some companies seem to be more enthusiastic than other companies about hiring new recruits. However, you notice that they are all vigilant about something; they seem to be on to your strategy! Being wary of their vigilance, you decide to use some disguises to make sure that everyone looks similar to increase your chances of getting an internship. However, this comes at a cost; your friends won't have as much success at talking with recruiters as much as you will.

Furthermore, their vigilance means that they put more effort into remembering the people they talk to! Although you and your friends could talk to the same recruiter multiple times, it seems to leave less of an impact on the recruiter every single time. You note that it might be better to visit some other booths.

After having come up with some general guidelines, it's now your time to implement them! Find the best way and fastest way to navigate through the crowded career fair to maximize your chances of getting a job!

## Installation

Before installation, make sure that you have Python 3.7.1 and pip. Clone this repository into your working directory, then run
```
cd awap
pip install awap2019
```
All of your code should go into the file `team.py`, and testing your code can be done by running `python run.py` in the base directory. Running the visualizer should be done by running `python visualizer.py`. Possible command line arguments are listed in the wiki.

If you have any problems installing, please ping us on Slack.

### Notes
We suggest using a virtual environment such as Anaconda/Miniconda to do most of your work. We have not tested how our module interacts with other Python modules (especially ones that aid in reading command line arguments). If you need would like to set up a virtual environment and require help, please ping us on Slack.

We are currently having troubles getting the visualizer to work with older Python versions. Thus, we suggest that you use Python 3.7.1.

## Documentation/Reference
Please refer to the wiki for information regarding the classes in the `awap2019` module.
