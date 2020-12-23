平台为Windows，首先确保系统内Python与pip的安装

在cmd中输入

python --version

检测路径是否配置正确，并查看当前python版本

在克隆的目录下运行如下指令

pip install virtualenv

virtualenv venv

cd venv\Scripts

activate

cd ..\\..

pip install django

python manage.py makemigrations

python manage.py migrate

在models中使用了JOSNField

若出现错误，参考网站：https://stackoverflow.com/questions/62637458/django-3-1-fields-e180-sqlite-does-not-support-jsonfields

之后通过使用

python manage.py runserver

启动服务器