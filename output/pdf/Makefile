#!/usr/bin/make -f

test: env_install_stamp
	. env/bin/activate; ./emit.py

env:
	which pyvenv || { echo "Install python3-venv and python3-dev"; exit 1; }
	pyvenv "$@"
	test -f "env/bin/pip" || { echo "This python pyvenv is too new. Must be 3.4+."; exit 1; }


env_install_stamp: env
	echo "If this fails on 'fatal error: Python.h: No such file or directory' you need python3-dev package."
	. "env/bin/activate"; pip install -r "requirements.txt"
	touch "$@"

clean:
	rm -rf env env_install_stamp
