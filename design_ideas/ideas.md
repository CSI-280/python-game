# Design Ideas

Here is a list of a bunch of ideas that I came up with for our game. If anyone has more ideas feel free to add them.

# Overview
  * This will be some type of game written in python. It will be a rogue-like game and is highly influenced from the original rogue game. It will have a main character which is controlled by the current player. They will be put in a 2d ASCII designed world were they will have to navigate through different rooms. Throughout the different rooms there will be enemies which they must defeat and puzzle that they must complete in order to win the end of the game. The goal and theme of the game is yet to be decided but this is the basic layout that will make up the game.

## Core Systems

1. Puzzles
   * Environmental
     * Look for clues to solve a riddle
     * Do something in one room and it affects another
   * Problem Solving
     * Move something to somewhere else
     * The grain chicken fox problem
     * Math
   * Item based
     * Find a certain item to unlock a door
     * Feed carrot to horse to solve puzzle
   * Reward at end of puzzle
     * gold/items
     * something to make it worth doing a puzzle
   * Time Based?
     * Puzzles could also have a timed aspect to add to the challenge of them.
     * Player would have to figure out the challenge or riddle in a given amount of time.

2. Movement
   * WASD
   * Potential for alternative movement options?
     * Jumping
     * Running
     * Teleporting

3. Player Character
   * Inventory
     * Armor
     * Weapons
     * Healing Items?
     * Potions?
     * Player Accessories
   * Stats/levels?
   * Could have levels which increment and give player bonuses.
     * Increased health, attack, movement, etc.

4. Combat
   * HP
   * Melee, ranged, or both?
   * Upgrades/different weapons
   * Enemies
     * Design multiple difficulty tiers of enemies
     * Potential for scaling enemies

5. Style of Gameplay
   * Turn-based gameplay
   * Player and enemies alternate turns
   * Only applies when there is enemy in room, otherwise the player move on their own time.
   * Could also include other key binds in the game for certain things like jumping and teleporting
     * Other key binds could be used for things like moving through text conversations/messages.

6. Level Generation
   * Random or Psuedo-random generation
   * Build "buckets" of rooms to add to floor
     * Buckets would hold things like dungeons and arenas that have a set layout
   * Floor themes
     * Could have a forest floor or an ice floor etc. and enemies/puzzles are based upon the theme.

## Additional features/topics

1. Goal
   * What is the player trying to do?
   * Find a magic item?
   * Save a village?
   * Ascend to godhood?
   * Worth discussing end goal/motivation for player
   - (This category closely aligns with the theme of the game which we have yet to determine.)

2. Graphics
   * Stick to only ASCII?
   - Using ASCII would be the simplest option, therefore, I think we should solely use it unless anybody else has any ideas.
     * Different color options besides plain white?
     - We could decide on different colors for different characters like orange for the wall colors as seen in the online rogue game.
   * Maybe add some simple sprites?
   - We could create some sprites for the player and enemies but we probably do not need many.
