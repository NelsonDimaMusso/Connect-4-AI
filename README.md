# Connect-4-AI
An AI who can play the connect 4 game


## Description  
This project offers an advanced implementation of Connect Four (6x12 grid) with multiple modes:  
- **YOU_VS_AI**: Play against a strong AI using optimized alpha-beta search.  
- **AI_VS_AI**: Watch two modular, hot-reloadable AIs face off to observe their strategies.  
- **AI**: Standalone AI code for testing, modification, or custom integration.

The project emphasizes code quality, modularity, and experimentation with different AIs.

---

## Mode 1: YOU_VS_AI (Human vs AI)

### Rules  
- Board size: 6 rows x 12 columns  
- Goal: connect 4 tokens vertically, horizontally, or diagonally  
- Players:  
  - AI (Red tokens ‘R’)  
  - Human (Yellow tokens ‘Y’)  
- Choose who starts first (AI or Human)

### How it works  
The AI uses an alpha-beta pruning algorithm with adaptive depth and a time limit (~10 seconds).  
It evaluates board positions by scanning 4-cell windows to anticipate offensive and defensive moves.

### Run the mode  
    python you_vs_ai.py

### Code snippet  
    game = ConnectFour()
    while not is_terminal(game.board):
        if game.player == -1:
            # Human input
        else:
            # AI computes its move

---

## Mode 2: AI_VS_AI (AI vs AI match)

### Description  
Two distinct AIs (AI A and AI B) automatically compete against each other.  
AI modules are reloaded each game to allow hot updates.  
The board is displayed every turn with full game rule enforcement.

### Run the mode  
    python ai_vs_ai.py

### Code snippet  
    referee = Referee()
    referee.run_match()

---

## Mode 3: AI (Standalone AI module)

### Purpose  
Provide a clean standalone version of the AI functions (`ai_decision` and related).  
Ideal for:  
- Easily modifying AI logic  
- Testing AI on arbitrary board positions  
- Integrating AI into other projects

---

## Screenshots / Visuals  

*(Insert here images, GIFs, or videos showing gameplay, the board, or AI in action)*

---

## Installation & Dependencies

- Python 3.x  
- No external packages required (standard library only)

---

## License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for full details.
