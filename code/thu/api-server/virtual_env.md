### Create a virtual environment in Python
In Terminal/ Command Prompt, type in:
```
python -m venv <name-of-env>
```
To activate the environment:
```
cd <dir-of-env>
source name-of-env/bin/activate
```
To deactivate:
```
deactivate
```

### Create a virtual environment in Anaconda
In Anaconda Prompt, type in: 
```
conda create --name <name-of-env>
```
To activate the environment:
```
conda activate <name-of-env>
```
To deactivate:
```
conda deactivate
```

### Organize and execute Flask application 
- In Flask, all `HTML` pages have to be stored under a folder named `templates`. This folder is usually placed directly under the app root folder where the main program e.g. `app.py` or `run.py` are.  
- All styling sheets, e.g. `CSS` and all `JS` scripts have to be stored under (directly under or in other sub-folders of) a folder named `static`. The `static` folder is directly under the app root folder. 
- Routing of the pages are configured in a Python script, usually named `views.py` and saved in the app root folder. 
- In summary, the project structure can look like follows:
```
. / #app root folder
---- static/
---- ---- styles.css
---- ---- script.js
---- templates/
---- ---- index.html
---- app.py
---- views.py
```
- To deploy the app on a specific port, say port 5001, in the app root folder run the command:
```
flask run -p <custom-port-number>
```

When no port number is given explicitly, the default port number 5000 will be used to host the website content. 
Access the web server at `127.0.0.1:<custom-port-number>`
