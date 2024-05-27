FROM python:3.9
ENV ASYNC_DB_DRIVER=postgresql+asyncpg SYNC_DB_DRIVER=postgresql DB_PASSWORD=123456
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "12510"]
