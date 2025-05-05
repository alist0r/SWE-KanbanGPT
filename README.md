KanbanGPT
* Daniel Graff
* Norris Miller
* Abdulaziz Aladdad
* Aaron Rogers
* Benjamin Sparks

Steps to pull all required files: 
  1) Open a terminal and navigate to the directory you want to place it in.  
  2) perform a 'git clone https://github.com/alist0r/SWE-KanbanGPT.git' 
  3) perform a 'cd .\SWE-KanbanGPT\'
  4) if all required software is ready, and Docker Desktop is running, perform a '.\start.sh'
    ** if required software is not installed, please read the following:  **


REQUIRED SOFTWARE: 
  - Python 3.10
  - Docker Desktop
  - Node.js

Installation Instructions: 
  - Download and install Python from python.org/downloads
  - Ensure that Python is added to PATH during installation

  - Download and install Docker Desktop from https://www.docker.com/products/docker-desktop/
  - After installation, ensure that Docker Desktop is running

After Installation: 
  - Navigate to the SWE-KanbanGPT root directory, and click on 'start.sh'
    ** additional options to run the program include navigating to the directory in a terminal and running .\start.sh **
  - If on Windows, a 'GIT for Windows' terminal will pop up and start running the following: 
    1) Check for all required documents.  If any are missing, an error message stating which files are missing.
    2) Checks to see if Docker is actively running.  If not, an error message will appear stating that Docker is not active.
    3) Initiate the docker-compose file which will start the database and the back-end.  This process will also include installing any additional neccessary packages.
    4) Initiate starting up the front-end, including installing all necessary NPM packages.
    5) A browser tab should open up that will bring you to the front page of the application.

