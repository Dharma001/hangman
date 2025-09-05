PRT582 – Software Unit Testing Report
Assessment 1 – Hangman Game
Student Name: Dharma Bahadur Budhathoki
Student ID: S395172
Campus: Sydney
Course Code: PRT582
Lecturer: Muhammad Rana
Submission Date: 10 August 2025

---------------------------------------
Project Contents
---------------------------------------
1. PRT582_Software Unit Testing Report_S395172_Dharma_Bahadur_Budhathoki
   - Full report including introduction, process (TDD, unit testing), test cases,
     screenshots, and conclusion.
   - GitHub repository link included.

2. hangman.py
   - Main Hangman game implementation in Python.
   - Includes Basic (random word) and Intermediate (random phrase) levels.
   - Features timer (15 seconds per guess), life deduction, win/lose detection.

3. test_hangman.py
   - Automated unit test cases written using Python unittest framework.
   - Tests cover:
     • Initial display
     • Correct and incorrect guesses
     • Timer-based life deduction
     • Win and lose conditions
     • Random word/phrase selection

---------------------------------------
GitHub Repository
---------------------------------------
You can find the complete project (code + report) at:
👉 https://github.com/Dharma001/hangman

---------------------------------------
How to Run the Program
---------------------------------------
1. Ensure Python 3.11 (or above) is installed.
2. Install required libraries:
   pip install pygame pillow

3. Run the game:
   python hangman.py

4. Run the unit tests:
   python -m unittest test_hangman.py

---------------------------------------
End of README
---------------------------------------