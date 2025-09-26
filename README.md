# pyCatcher
<p align="justify">
pyCatcher is a small but powerfull tool designed to capture and analyze HTTP requests in real-time, allowing users to inspect and modify response parameters. It also enables storing custom payloads—such as HTML forms, JavaScript snippets, and XSS vectors—for targeted web penetration testing or CTFs. From a security perspective, pyCatcher is especially useful for identifying vulnerabilities like SSRF, XSS, etc. by testing how web applications handle injected inputs and manipulated requests, helping security professionals streamline testing and documentation of potential attack vectors.
</p>

## Install
```
git clone https://github.com/sp34rh34d/pyCatcher.git
cd pyCatcher
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x pyCatcher.py
```

## One line installation
```
git clone https://github.com/sp34rh34d/pyCatcher.git && cd pyCatcher && python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt && chmod +x pyCatcher.py && python3 pyCatcher.py
```

## Args
```
            --== options ==--
    exit                  ->  close this app
    list                  ->  show all custom routes
    add                   ->  add new flask route
       ├──  --path        ->  specify a name for the new route
       └──  --header      ->  set a custom header for every http response, you can add multiple headers
                              (--header ContentType:text/html --header test2:test2)
                              if you need add (space) on header value just add ++ 
                              (--header X-Custom-Header:This++is++a++test)
    load                  ->  load all registered custom routes from custom_routes.ini file
    save                  ->  save custom routes on custom_routes.ini file
    del --id <path id>    ->  delete specific path
    run                   ->  start http server
       ├──  --port        ->  specify http port (default 8080)
       ├──  --interface   ->  specify listen interface (default 0.0.0.0)
       ├──  --serveo      ->  expose local flask app to the public internet via ssh port forward via serveo.net
       ├──  --ssl         ->  enable ssl context
       ├──  --key         ->  set private key (.key/.pem)
       └──  --pub         ->  set public key (.crt/.pem)
    help                  ->  show this menu
```

## Fetch pyCatcher on local network
Starting pyCatcher on port `1337`, allow internal network only (using a local web instance for testing)

<img width="1664" height="961" alt="Screenshot 2025-09-26 at 8 22 16 AM" src="https://github.com/user-attachments/assets/c9be5afd-2df3-48b4-b2f3-dcfee4c7a78a" />
<br>

## Fetch pyCatcher via internet
Sometimes you need to fetch your request catcher over internet (bugBounty/CTFs/pentesting), to expose your pyCatcher over internet, you can use a free [AWS EC2](https://aws.amazon.com/es/ec2/?trk=02bd2428-3348-4251-8b76-83ffa306f0f1&sc_channel=ps&ef_id=CjwKCAjw89jGBhB0EiwA2o1On8sv-Lp0963ncIsL-IVsaw-DsyBYpD8YT7UWJoWMhlqK8RxYmlvSEhoCVNkQAvD_BwE:G:s&s_kwcid=AL!4422!3!647999789403!e!!g!!aws%20ec2!19685287168!143348659342&gad_campaignid=19685287168&gbraid=0AAAAADjHtp8RYoaYTiZTBI93z1pldSMDl&gclid=CjwKCAjw89jGBhB0EiwA2o1On8sv-Lp0963ncIsL-IVsaw-DsyBYpD8YT7UWJoWMhlqK8RxYmlvSEhoCVNkQAvD_BwE) or using a port forward service like [lhr](https://localhost.run) / [serveo](https://serveo.net).\
Serveo is available on pyCatcher using the arg `--serveo`.
<br>

<img width="1658" height="686" alt="Screenshot 2025-09-26 at 8 24 32 AM" src="https://github.com/user-attachments/assets/c5278451-9f62-4c43-8b5a-fef1521fcae1" />


