# This is the 9apps Toolkit.

This toolkit contains some useful tools that are used mainly for configuring EC2 instances.

## Install
Login into your EC2 instance and checkout the toolkit as root user:

    $ sudo -i
    $ git clone https://github.com/9apps/9tk.git && cd 9tk

## Run it
    $ ./console.sh


# General Information

All the tools rely on IAM Role and User-Data.

That means that before being able to use them you need to configure the instance to use a IAM Role at creation time,
and to cofigure the User-Data before you launch it.

An example how to configure the instance User-Data can be found in ./config/userdata.txt