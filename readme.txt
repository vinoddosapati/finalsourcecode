For Testing:

Step 1. 
Install Python 3.7+ and pip

Step 2.
Inside /soucecode folder, open command prompt or terminal create a virtual enviroment and activate
Create virtual enviroment command : "python3 -m venv tutorial-env"
Activate virtual enviroment:
On Windows, run: "tutorial-env\Scripts\activate.bat"
On Unix or MacOS, run: "source tutorial-env/bin/activate"

Step 3.
Run requirments.txt(installs all the required python packages)
"pip install -r requirements.txt"

Step 4.
Run the main pyhton file
"python api.py"

Step 5.
Open localhost


For future developments:
for frontend
1. Inside /sourcecode/frontend
2. node 15.10.0, npm 7.6.0, cli 11.2.2
3. npm install
4. ng build
5. ng serve -o

for backend:
1.Install Python 3.7+ and pip
2.Step 2.
Inside /soucecode folder, open command prompt or terminal create a virtual enviroment and activate
Create virtual enviroment command : "python3 -m venv tutorial-env"
Activate virtual enviroment:
On Windows, run: "tutorial-env\Scripts\activate.bat"
On Unix or MacOS, run: "source tutorial-env/bin/activate"
3.pip install -r requirements.txt
4. Inside /sourcecode folder
2. /extracted_images is the dataset
3. /savedata is the train and test split of dataset
4. If required to train and test split of an UPDATED dataset, the run command "python normilize.py" else skip this step.
5. If required to train a the model or "/seq_model_new.model" folder doesnt exists, then run command "python seqcnn.py", else skip.
6. Run the main pyhton file "python api.py"

Final step: Open angular localhost (default is localhost:4200)