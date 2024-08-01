<h1 align="center">
Alassane WADE Tree C# Script
</h1>  

<h2 align="center">
                                       "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣷⣶⣥⣴⣿ "
</h2>         

Tree C#
A Python script that enables you to see dependencies of a C# solution with a tree display.

## Open a terminal in full screen.
- Clone this github repository in the path of your choice: 
```bash
git clone https://github.com/alassane8/TreeCSharp.git
```
- Go to the BattleShip folder :
```bash
cd TreeCSharp/code
```
- Run the script: 
```bash
python script.py
```
## How to use the Script
You are now ready to use the script ! The goal is to enter the path to your .sln 
file which is the solution file that registers all the projects dependences of your 
C# solution.
From there, different files will be created where you placed 'script.py'.

## All_Projects.txt
Gather all the projects in the solution that allow at least one dependency (Mother projects) 
or at least one project that depends on them (Child projects) .
This file indicates for each project :

- GUID (Project ID)
- Framework
- Path
- Child and Mother projects that he owns

## Independent_Projects.txt
Brings together all the projects in the solution which have no dependencies and for which no 
project in the solution depends on them. 
This file indicates for each project :

- Name
- GUID
- Framework
- Path

## Tree.txt
Visualization of dependencies between projects as well as the Frameworks linked to these projects
This file indicates for each project :

- Name
- Framework

## Area for improvement
Here, you can find the features I am currently working on in this repository.
This allows you to be aware of the changes that are to come and see what needs to be improve. 