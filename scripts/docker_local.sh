docker run --rm \
		-v $(pwd)/dist:/app/dist \
		python:3.9-slim bash -c "\
			pip install /app/dist/*.whl > /dev/null && \
			echo 'pyhw version:' && \
			python -c 'import pyhw; print(pyhw.__version__)' && \
			pyhw"