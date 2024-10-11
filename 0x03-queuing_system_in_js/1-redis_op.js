#!/usr/bin/node
import { createClient, print } from 'redis';

const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log(` Redis client connected to the server`));

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, print);
}

const displaySchoolValue = (schoolName) => {
  client.get(schoolName, (err, resp) => {
    if (err) {
      console.log(err);
    } else {
      console.log(resp);
    }
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
