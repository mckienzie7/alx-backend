#!/usr/bin/node
import { createClient, print } from 'redis';

const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log(` Redis client connected to the server`));

client
.multi()
.hset('HolbertonSchools', 'Portland', 50, print)
.hset('HolbertonSchools', 'Seattle', 80, print)
.hset('HolbertonSchools', 'New York', 20, print)
.hset('HolbertonSchools', 'Bogota', 20, print)
.hset('HolbertonSchools', 'Cali', 40, print)
.hset('HolbertonSchools', 'Paris', 2, print)
.exec()

client.
hgetall('HolbertonSchools', (err, resp) => {
  if (err) {
    console.log(err);
  } else {
    console.log(resp);
  }
}
)
