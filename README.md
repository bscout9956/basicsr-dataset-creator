# Image-Tiler
A set of scripts that split images into squares for BasicSR model training.

## Requirements:
  - An NVIDIA GPU + CUDA 9 or 10 installed: https://developer.nvidia.com/cuda-toolkit
  - Python 3.7 or newer (64-bits): https://www.python.org/downloads/
    - Make sure you are running python3 by typing `python --version` or `python3 --version`
  - A clone of the BasicSR or any forks of it
    - **Observation**: rlaPHOENiX's fork of BasicSR is preffered, but this should work with the original repo as well.
      - PHOENiX's: https://github.com/rlaPHOENiX/BasicSR
      - xinntao: https://github.com/xinntao/BasicSR
  - PyTorch for Python 3 according to your environment of choice: https://pytorch.org/
  - Python packages: `pip install numpy opencv-python lmdb pyyaml tensorboard` 
    - You may need to use `pip3` instead...
  - **Linux users refer to the package manager and settings in your distro**.
    - CUDA usually comes with the driver, and the proprietary one is preferred.
  
## Instructions for installing and training BasicSR:
  1. Install the requirements
  2. Clone this repo by using `git clone https://github.com/bscout9956/image-tiler` or by download the zip from GitHub.
  3. Pick a random assortment of images to be tiled
  4. Create a folder at the root of the repo directory called "input"
    - i.e: ../image-tiler/input
  5. Place your pictures inside the input folder
  6. Run on CMD or Terminal (Linux):
    `python prepareDataset.py`
      - You may need to use python3 instead...
      - You may also want to open the script in a software like Notepad++ to edit its settings...
  7. Check for the results inside the datasets folder once the script finishes running...
  8. Go to the root of your clone BasicSR folder
  9. Head to ../BasicSR/codes/options/train/
      - Pick a YML file as a template and edit its settings according to your dataset
      - Rename your model accordingly, put a creative and relevant name on it, preferrably with the scale before it
        - e.g: 4x_ScaleTreesGames, 8x_WaterCups, 2x_RandomAnimals
      - Match the scale according to the dataset, the default for this script is 4
      - Check the datasets indications inside the YML (for both val and train) and if you are a Windows user change all forward slashes (/) to double backslashes (\\).
        - The paths are case-sensitive on Linux. Make sure the LR and HR folders inside your datasets folder are correctly cased.
      - Make sure the HR Size is what you have set from the prepare_dataset.py script. Default is 128.
      - Under the `path` tree, set the root of the BasicSR to where you have cloned the BasicSR repo
        - Comment out pretrain if you are not planning on using a pretrained model
        - Comment out the resume state if you are starting a new model, uncomment if you are resuming and change the directions accordingly.
      - Depending on the BasicSR fork you will have to switch `discriminator_vgg_128` to `discriminator_vgg`, make sure it matches the HR size, if it still doesn't work do `discriminator_vgg`.
      - Under the train tree you can set some additional weights, I recommend uncommenting LPIPS on Phoenix's fork.
        - You may also change the validation frequency, it's in scientific notation. 1e3 = 1000 iters.
      - Under the logger tree you can change the tensorboard logger parameters or disable it
  10. After you are done with your YML file: 
      - Copy the datasets folder from the root of your image-tiler folder to the root of your BasicSR clone
        - i.e: ../image-tiler/datasets to ../BasicSR/datasets
      - Open CMD or Terminal and make sure the root path is BasicSR.  
        - You can do that on both Linux and Windows by copying the path to the folder and doing:
          `cd ..\BasicSR\codes` (Windows) or cd `../BasicSR/codes` (Linux, **Case-Sensitive**)
      - Run `python train.py -opt options\train\yourymlfilehere.yml`
      - In Linux, forward-slashes and maybe python3, your environment dictates.
  11. If everything goes right, your model will begin training and it should take some time (6h~) until it generates proper results.
      - You may check for the BasicSR/experiments/model_name folder for validation images, the models, its training states and logs.
      - You can also run tensorboard **if installed** *pip package*, to check for the stats on your web-browser.
  11. Once you feel like not running the model anymore or are satisfied with the results just close the Terminal/CMD, or press Ctrl+C to stop the BasicSR.
  
## Observations and Troubleshooting:
  - **You may submit Pull Requests as my code can be pretty wonky.**
  - ../path just represents that whatever is before the / is unknown to me and varies wherever you put the clones of each repo.
  - It's mandatory to use Python 3 64-Bits so you can install PyTorch. It won't run on 32-Bit machines nor Python 2.
  - If you cannot run PyTorch or install, reinstall Python 3 and all the needed packages.
  - The HR tiles resolution, LR tiles resolution and scale must relate to each other:
    i.e: 128x128 / scale (4) = 32x32.
      - HR: 128
      - LR: 32
      - Scale: 4
  - The mostly used versions of BasicSR are forks based on the old arch, which has no practical difference on the results.
  - xinntao's code uses a new model architecture, models created with his fork are not compatible and must be converted with a script provided on his fork.
  - You may run out of memory while training. Here are workarounds or solutions to that problem. In order of "less intrusive" to "more intrusive": 
    - Close applications that may be using your GPU VRAM.
    - Lower the batch_size, it may cause training to be slower however.
    - Lower the HR resolution **dataset change required**.
    - Other solutions for advanced users below.    
  - Training 1x Models are possible but only on the old arch.
  - Dataset Name and Validation Name in the YML are irrelevant.
  - PSNR is good when higher (25-30 avg). LPIPS is good when lower (<0.1 avg). SSIM is good when higher. (depends) 
  - You can find additional help on Reddit at https://www.reddit.com/r/GameUpscale/ and its Discord Server (I'm there ;)).
  - There is also a wiki with additional steps, help and a model database: https://upscale.wiki/wiki/Main_Page
  - Feel free to submit bug reports, however I can't guarantee anyone an immediate fix or answer.
  - You'll be better off looking for help on that wiki or in the Discord Server. 
  ### Advanced Users Only:
  - **I don't take responsibility for any damage, loss, corruption of files, explosion or whatever possible for following theseinstructions.**
    1. If you're low on memory, try this:
      - If you're on Linux, **log off**, go to a TTY (Ctrl+Alt+F2-?F12?). 
      - Log-in, check with `nvidia-smi` *if installed* which applications are using VRAM... 
      - You may want to kill or stop the Display Manager. *This can be reverted by starting it again* and run the script from there.
      - SSH is great for remote management of model training. Just make sure to use (RSA or better) keyrings and not passwords ;)
    2. You can find additional scripts in the extras folder, they have been used by me for some of the models I've trained.
      - I guarantee nothing about them working and the code is terrible.
