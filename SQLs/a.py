
git checkout branch-name
rm -rf .git
git init
git remote add origin https://github.com/your-user/your-repo.git
git add .
git commit -m "Reset branch-name to latest state"
git branch -M branch-name
git push --force origin branch-name
