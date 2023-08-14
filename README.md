# Face-Detection-and-Recognition-Attendance-Script-With-Excel-Report
This is the third version of my OpenCV python program, I have combined scripts from my previous projects and made a single script that can allow users to train and recognize trained faces and automatic Roll Number marked excel sheet. 

- Edit this line with the png file path, before running the program: [line: 188]
- icon_image = Image.open(r"your logo/icon image path here")

# how to run the program?

- Make sure to install Python 3.7 or 3.8 | check the version using this command in cmd: "python --version"

### libraries and software components needed
       
- ******openpyxl library******
    - It helps read, write, and modify Excel spreadsheets.
    - In this program, it's used to save recognized roll numbers in an Excel file.
    - open cmd as admin>`py -m pip install openpyxl` use the code> type py and import openpyxl> if you do not get any errors, the library has installed perfectly.
    
- **CMake**
    - It helps developers build and organize their code on different types of computers without too much hassle. Downkiad and install latest version from https://cmake.org/download/
- **open-cv python library**
    - Helps with image and video processing, including tasks like loading images, editing, and detecting objects.
    - install this library using cmd, with this code: 
    **pip install opencv-python**
    - Verify using IDLE (can be found in startmenu) with this code: (output must be the version of the library):
    import cv2
    print(cv2.__version__)
- **Dlib**
    - It can find faces, figure out who they belong to, and even tell you where the eyes, nose, and mouth are on a face.
- **Visual Studio C++**
    - Go to [Visual Studio C++](https://visualstudio.microsoft.com/vs/features/cplusplus/) and download the installer, when installing check the development with C++ box and let it install.
    - It is required for creating a Dlib build without any errors
- **face_recognition library**
    - Specifically designed for face detection and recognition in images. It finds faces and can even identify who they belong to.
    - Install face_recognition lib using this command in cmd: pip install face_recognition
    - if you get any error make sure that CMake & Visual Studio C++ are both installed properly and also make sure python version is either 3.7 or 3.8 and no the latest version.

## Contributing
Contributions are welcome! If you'd like to contribute to the project, feel free to fork the repository and submit pull requests.

