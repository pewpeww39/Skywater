# skywaterJL
Skywater_Project_Fall_2021

---How To install miniconda to run with jupyter---
---skip if not already installed--- 
---this is to save time if not installed correctly i.e. if conda-forge isnt added prior to other packages--- 
        backup envs
        uninstall miniconda
---start here for new install---
        install/reinstall miniconda for all users
        run conda in admin
        conda config --add channels conda-forge
        conda config --set channel_priority strict
        install python==3.9 in base env
---Could try starting here---
        --option A
        create env --name exampleName python==3.6.5
        activate env exampleName
        install -c anaconda ipykernel
        ipython kernel install --user --name ex --display-name "skywater_env"
        --option B
        create env from yml