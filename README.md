<br/>
  <h1 align="center">
    "I-me-coffee" Django based website <br>
     JobPlace - CoffeeBar
  </h1>
  <h4> Another work "CoffeeShopTest" is a mobile app that connects to it thru REST API. </h4>
<p> ordering, warehouse, booking, statement (later), </p>

# Installation guide:

- ## Create a virtualenv
```Shell
pip install virtualenv
```
```Shell
virtualenv venv
```

- ## Activate venv
- Linux - ``` source venv/bin/activate ```
- Windows - ``` venv\Scripts\activate ```

- ## Clone & Install
- ``` git clone https://github.com/Jupieter/I-me-coffee.git ```
- (venv) ``` pip install -r requirements.txt ```

- ## Migrate & User & Run
- (venv) ``` python manage.py migrate ```
- (venv) ``` python manage.py createsuperuser ```
- (venv) ``` python manage.py runserver ```

