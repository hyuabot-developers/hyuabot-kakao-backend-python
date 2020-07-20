# HYUABOT ![](https://img.shields.io/static/v1?label=release&message=v20.07.20&color=blue) ![](https://img.shields.io/static/v1?label=Framework&message=python3-django&color=skyblue) ![](https://img.shields.io/static/v1?label=author&message=Jeongin%20Lee&color=green) ![](https://github.com/jil8885/hyuabot-mainline/workflows/Deploy/badge.svg)

Chatbot that provides several information for Hanyang Univ. ERICA Campus

## Getting Started

These instructions about how to clone this project for developing and testing purposes. See deployment to know how to deploy the project on a release channel

## Prerequisites
```
python3
```

### Installing
```
$ sudo apt install python3 python3-pip // Install required packages
$ git clone https://github.com/jil8885/django_mainline // Clone django mainline project
$ pip3 install --user -r requirements.txt // Install required python modules
$ git submodule update --init --recursive // Clone submodule projects
```

### How to Run
```
$ python3 manage.py runserver <port>
```
And, you must connect server with chat bot on [Kakao-i Open Builder](https://i.kakao.com/openbuilder)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Jeongin Lee** - *Hyuabot Developer* - [jil8885](https://github.com/jil8885)

See also the list of [contributors](https://github.com/jil8885/hyuabot_app_hyuabot/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details