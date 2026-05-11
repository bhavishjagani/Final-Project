Description
A full playable chess game built in Python using Pygame. Two players take turns on a local machine, moving pieces according to normal chess rules. The game has multiple game modes (human vs human, human vs AI), a choice of board themes, move highlighting, check/checkmate detection, and game state saving so players can continue a match later. The AI opponent uses a minimax algorithm with alpha-beta p`runing to play at the appropriate difficulty level.

Technology 
Python and Pygame, Pygame controls the graphics, event loop, and input easily for a 2D board game. No other languages are required, except maybe json for saving states.

Sketches

<img width="1260" height="428" alt="Screenshot 2026-04-29 103620" src="https://github.com/user-attachments/assets/5b93ea37-ed92-4678-a697-f73320fae0f5" />



Features
(P1) Must Have:
Rendered 8×8 board with pieces
Click to select & move pieces
Legal move validation for all pieces
Turn alternation (white / black)
Check & checkmate detection
Highlight selected piece + valid moves
Human vs Human (local 2-player) 
Win / checkmate screen 
(P2) Should Have:
Captured pieces sidebar
Move history/notation log
Stalemate and draw detection
Pawn promotion dialog
Human vs AI (minimax + alpha-beta)
AI difficulty detector (1-4 levels)
Main menu scene
Settings scene (board theme)
Save game state to file
Load saved game from menu
(P3) Nice to Have:
En passant and castling
Per-player countdown timer
Move sounds
AI vs AI demo mode
Undo last move button
Multiple save slots
Board themes (classic, green, blue)

Version Plan

V1 - Playable core
Rendered board with all pieces
Click to select & move
Legal move validation
Turn alternation
Check & checkmate detection
Move highlighting
Win screen
V2 - Full experience
Main menu scene
Human vs AI mode
AI difficulty selector
Save & load game
Captured pieces display
Move notation log
Pawn promotion dialog
Stalemate detection
V3 - Polish
En passant & castling
Per-player timer
Board theme selector
Move sounds
Undo button
Multiple save slots
AI vs AI demo mode

