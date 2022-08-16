FROM python:3.10-alpine3.16 as base
WORKDIR /workdir

FROM base AS python-deps
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime
COPY --from=python-deps /workdir/.venv /workdir/.venv
ENV PATH="/workdir/.venv/bin:$PATH"
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
