# GeneticAvoidance
An AI that plays Dodge Game

## About The Project
Avoid enemies using genetic algorithm and neural network.

**Neural Network**
- Inputs : [Enemy's relative distance, Enemy's direction vector]
- Construction : 4 * 6 * 6 * 8
- Outputs : Directions that player Can Move (Up, Down, Left, Right, Diagonals)
- Activation Function : Softmax

## Prerequisites
- pygame
- matplotlib
- numpy
``` Bash
python3 -m pip install -U pygame --user # install pygame
python -m pip install -U matplotlib # install matplotlib
pip install numpy # install numpy
```

## Installation & Usage
``` Bash
git clone https://github.com/minjune8506/GeneticAvoidance
cd ./GeneticAvoidance
python3 game.py
```
## Contributors
- @minjune8506   
- @kpeel5839   
- @SOLokill   
- @mingyeong00

## License
Distributed under the MIT License.
