
### Power up the entire cluster:
```sh
cd src/
python -m iocluster.master -p 2121
Open another tab:
python -m iocluster.slave -t TM -p 2121
Open another tab:
python -m iocluster.slave -p 2121
Open another tab:
python -m iocluster.client.send
```
