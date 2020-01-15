---------------------
Git
---------------------

----------------------------

echo "# mensa-online" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/franciscosuca/mensa-online.git
git push -u origin master

---------------------
Step 1: From your project repository, bring in the changes and test.

git fetch origin
git checkout -b admin origin/admin
git merge master

Step 2: Merge the changes and update on GitHub.

git checkout master
git merge --no-ff admin
git push origin master

---------------------

##Commit states:
1. modified
2. staging
3. committed

##check git version
git --version

##create user
git config --global user.name [user_name]
git config --global user.email [email]

##initialize Git repository
git init

##staging area
git add [file_name] --> adding it
git rm --cached [file_name] --> removing it
git rm -f [file_name] --> force removal

git add . --> add to the staging area all the modified files

##committing area
git commit -m "message that you want to convey"

##Check the modifications
git log
git log --oneline --> check the modifications with fewer details

----------------------

##Undoing the modifications


###Checkout commit

**use to go to a specific commit in the history**
git checkout [commit_code]
**go back to the last commit performed**
git checkout master

###Revert commit

**works better when you want to delete some file**
git revert [commit_code]

###reset commit
**Delete the commit(s) after [commit_code] but the code remains as the one in the last commit
**
git reset [commit_code] 
**delete the commit(s) after [commit_code] and the code returns to version in [commit_code]**
git reset [commit_code] --hard 

----------------------

##branching


**create a new branch**
git branch [branch_name] 
git branch -b [branch_name] 

**display all the branches**
git branch -a 

**change from current branch to [branch_name]**
git checkout [branch_name] 

**delete unmerged branches**
git branch -D [branch_name]

**merge branches**
git merge [branch_name]

---------------------
Github
---------------------
---------------------

**Download the project folder from github**
git clone [Repository_URL] 

**Upload the project folder to github**
git push [Repository_URL] master

**Using an alias instead of the [Repository_URL]**
git remote add [alias_name] [Repository_URL] 

**Display data about the repository**
git remote -v

**Display the changes made in the branch**
git pull origin master

