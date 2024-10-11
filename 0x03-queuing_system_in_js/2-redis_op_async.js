#!/usr/bin/node
import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log(` Redis client connected to the server`));

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, print);
}

const getAsync = promisify(client.get).bind(client);

const displaySchoolValue = async (schoolName) => {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.log(err);
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
