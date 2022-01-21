# cRPG
Game used "arcade" framework for simple 2D game creating. Changed game engine a lil bit and put it in the separate file.
--------

21.01.2022 - 1:14
1. Changed movement type. Now using mouse only. Click on the enemy to attack or on the field to move.
2. Added enemies (two sprites)
3. Creating files and parser to load settings for enemies and player - should be fixed
4. Added GUI and player info after "TAB" key pressing
5. Added hurting and dying animations for enemies
6. Added hurting animation for player
7. Enemy when dies, adds exp for player. Player is able to lvl up
8. Health of the enemy is presented, when mouse is hover on it, on the top of the screen
9. Modified physic engine for stop player when colliding with walls and entities - it should be tested and verified
10. Added another engine for enemies colliding with other enemies - should be tested and verified
11. Enemies are randomly patroling area radius and attacking player when in radius
12. Added 3D illusion, sprites are drawn in order to Y coord. The higher coord Y is, then sprite is drawn as a first. 

Next steps:

    *Fully fixing player and enemies interactions
    *Adding item drop
    *Adding GUI for item handling
    *Enabling debug console
    *Code cleaning - many lines are commented, variables not used etc.
    *Adding docstring for methods, functions and comments

--------

05.01.2022 - 1:20
1. Added character idle animation and walking animation
2. Found a way to reduce amount of graphic files to put few frames into one sequence image
3. Move all movement into PlayerCharacter class
4. Added function for textures loading and frames counting
5. Finally walking speed is fixed same as idle.


Next steps: 

    *Adding attack ability for player character
    *Adding GUI and printing character stats
    *Adding and refactor enemy.py file



---------

04.01.2022 - 18:40
1. Full code rewriting
2. Move main map code to the separate file - preparing for more than one map
3. Map files sorted to the specific directories
4. Code refactoring - moved variables to dictonary
5. Added main menu at the game start. Wrote settings and possibility to window size change:

Resolutions:

    *800x600
    *1024x786
    *1920x1080



Game is started as expected
