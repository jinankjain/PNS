## Performance test:

- Number of clients:
	- Vary clients from n = 100 to 500 in step size of 50
	- Try to break the time into it's constituent function like genrating signature, generating diffs, network latency. 
- Vary Page Size:
   - Try to get different page size 5000 to 10000 in step size of 500
- Vary the diff size:
	- Change the diff size from 10% to 80% in step size of 10



- Get some estimates on performance of individual functions like signature verification, diff generation function, etc

Remove some warmup phase and cool down phase from the graph