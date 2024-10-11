#!/usr/bin/node
import { promisify } from 'util';
import express from 'express';
import { createClient } from 'redis';
import { createQueue } from 'kue';

const queue = createQueue();
const client = createClient();
const app = express();
let reservationEnabled = true;

app.use(express.json());

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);
const PORT = 1245;

const reserveSeat = async (number) => {
    await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    return await getAsync('available_seats');
};

app.get("/available_seats", async(req, res) => {
    try {
        const seats = await getCurrentAvailableSeats();
        res.json({ numberOfAvailableSeats: seats });
    } catch (err) {
        res.status(500).json({ error: err.message || err.toString() });
    }
});

app.get("/reserve_seat", async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ "status": "Reservation are blocked" });
    }
    const job = queue.create('reserve_seat');
    job
    .on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (err) => {
        console.log(`Seat reservation job ${job.id} failed: ${err.message || err.toString()}`);
    })
    .save((err) => {
        if (!err) {
            return res.json({ "status": "Reservation in process" });
        }
        return res.json({ "status": "Reservation failed" });
    });
});

app.get('/process', (req, res) => {
    res.json({ "status": "Queue processing" });
    queue.process('reserve_seat', async(job, done) => {
        try {
            let availableSeats = await getCurrentAvailableSeats();
            availableSeats = availableSeats - 1;
            reserveSeat(availableSeats);

            if (availableSeats >= 0) {
                if (availableSeats === 0) reservationEnabled = false;
                done();
            } else {
                done(new Error('Not enough seats available'));
            }
        } catch (err) {
            done(err);
        }
    });
});

app.listen(PORT, async () => {
    await reserveSeat(50);
    reservationEnabled = true;
    console.log(`App listening on port ${PORT}`);
});
