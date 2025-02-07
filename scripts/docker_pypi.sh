docker run --rm \
		python:3.9-slim bash -c "\
			pip install pyhw -U > /dev/null && \
			echo 'pyhw version:' && \
			python -c 'import pyhw; print(pyhw.__version__)' && \
			pyhw"
