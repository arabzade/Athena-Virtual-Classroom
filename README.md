### To enhance the online learning experience, we developed a video conferencing desktop application with a virtual classroom background for a real classroom like experience. 
.
### We came across BodyPix model for detecting and extracting a person in the frame for a smooth virtual backround:
![BodyPix](https://i.imgur.com/bPaWQOd.gif)

### By having same custom background for all the participants, we were able to create an illusion of a single classroom like so:
![Custom background](https://i.imgur.com/vW5ssr2.png)

### Then we decided to have a single image as the background and sent just the person cut out from client:
![Single background](https://i.imgur.com/icmY5F8.gif)


# Steps:

## Clone branch Develop-phase2
```bash
git clone https://github.com/ankitd3/Athena-Virtual-Classroom.git
```

## To create and activate virtual environment
```bash
python3 -m venv athena_env
```

```bash
source athena_env/bin/activate
```

## Install requirements

```bash
brew install portaudio
```

```bash
python3 -m pip install -r requirements.txt
```

## Run the program!

```bash
python3 View/HomePageView.py
```
