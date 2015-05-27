
### Power up the entire cluster:
At first, unpack the UCC_2015 archive to src, so the Schemas will be in src/UCC_2015/xml/.
```sh
cd src/
python -m iocluster.master -p 2121
Open another tab:
python -m iocluster.slave -t TM -p 2121
Open another tab:
python -m iocluster.slave -p 2121
Open another tab:
python -m iocluster.client.send
Open another tab:
python -m iocluster.master -b --primary_address localhost --primary_port 2121 -p 2134
python -m iocluster.client.ask 0 [-p 2134]
```
