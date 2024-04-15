# 0x03. User authentication service

Back-endAuthentification

-  By: Emmanuel Turlay, Staff Software Engineer at Cruise
-  Weight: 1
-  Project over - took place from Jan 22, 2024 6:00 AM to Jan 26, 2024 6:00 AM
-  An auto review will be launched at the deadline

#### In a nutshell…

- **Auto QA review:** 0.0/89 mandatory & 0.0/4 optional
- **Altogether:**  **0.0%**
  - Mandatory: 0.0%
  - Optional: 0.0%
  - Calculation:  0.0% + (0.0% * 0.0%)  == **0.0%**

![](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2019/12/4cb3c8c607afc1d1582d.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240225%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240225T200040Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=26020581a4d7c042fb8b5ca562fba9418d926b8b399af5a9799a8ebdefd5dd25)

In the industry, you should **not** implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-User](https://intranet.alxswe.com/rltoken/9nVfotMI_1zpEzihMzBeTA "Flask-User")). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

## Resources

**Read or watch:**

- [Flask documentation](https://intranet.alxswe.com/rltoken/lKExyvivrrW4eh0eI8UV6A "Flask documentation")
- [Requests module](https://intranet.alxswe.com/rltoken/py7LuuD1u2MUwcaf8wnDzQ "Requests module")
- [HTTP status codes](https://intranet.alxswe.com/rltoken/cj-mc5ZHp_KyXn1yikHC0A "HTTP status codes")

## Learning Objectives

At the end of this project, you are expected to be able to [explain to anyone](https://intranet.alxswe.com/rltoken/oAqmZmipBdjCcfI5QqyFXA "explain to anyone"), **without the help of Google**:

- How to declare API routes in a Flask app
- How to get and set cookies
- How to retrieve request form data
- How to return various HTTP status codes

## Requirements

- Allowed editors: `vi`, `vim`, `emacs`
- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using `python3` (version 3.7)
- All your files should end with a new line
- The first line of all your files should be exactly `#!/usr/bin/env python3`
- A `README.md` file, at the root of the folder of the project, is mandatory
- Your code should use the `pycodestyle` style (version 2.5)
- You should use `SQLAlchemy` 1.3.x
- All your files must be executable
- The length of your files will be tested using `wc`
- All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
- A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
- All your functions should be type annotated
- The flask app should only interact with `Auth` and never with `DB` directly.
- Only public methods of `Auth` and `DB` should be used outside these classes

## Setup

You will need to install `bcrypt`

```
pip3 install bcrypt
```
